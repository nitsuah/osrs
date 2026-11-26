"""Tests for the bot.skills.fishing loop (Fish) and its pause key handler."""
import configparser
import importlib
import sys
from unittest.mock import MagicMock, patch

import pytest

CHAT_IMAGE = object()


def _config() -> configparser.ConfigParser:
    cfg = configparser.ConfigParser()
    cfg.read_dict(
        {
            "coordinates": {
                "chat_region": "0,0,100,50",
                "inventory_slot_1": "10,20",
                "inventory_slot_2": "30,40",
                "stall_position": "100,200",
                "fish_spot_1": "300,400",
            }
        }
    )
    return cfg


@pytest.fixture
def fishing():
    """Import bot.skills.fishing with platform modules stubbed and collaborators mocked."""
    for name in ("winsound", "keyboard", "pynput", "pynput.mouse", "pynput.keyboard"):
        sys.modules.setdefault(name, MagicMock(name=name))
    for name in ("bot.skills.fishing", "bot.skills.actions"):
        sys.modules.pop(name, None)
    with patch("bot.config.load_config", return_value=_config()):
        module = importlib.import_module("bot.skills.fishing")

    module.real_handle_user_input = module.handle_user_input
    saved = (module.RUNNING, module.PAUSE_FISHING, module.CLICK_COUNTER)

    module.health_monitor = MagicMock(name="health_monitor")
    module.health_monitor.is_stuck.return_value = False
    module.checkpoint_logger = MagicMock(name="checkpoint_logger")
    module.capture_screen = MagicMock(name="capture_screen", return_value=object())
    module.capture_and_process_chat = MagicMock(
        name="capture_and_process_chat", return_value=("chat text", CHAT_IMAGE, True)
    )
    module.fish_from_spot = MagicMock(name="fish_from_spot", return_value=7)
    module.respond_to_question = MagicMock(name="respond_to_question")
    module.handle_user_input = MagicMock(name="handle_user_input")

    module.RUNNING = True
    module.PAUSE_FISHING = False
    module.CLICK_COUNTER = 0

    def stop_after_one_iteration(_seconds):
        module.RUNNING = False

    sleep = MagicMock(side_effect=stop_after_one_iteration)
    with patch.object(module.time, "sleep", sleep):
        module.sleep_mock = sleep
        yield module

    module.RUNNING, module.PAUSE_FISHING, module.CLICK_COUNTER = saved
    for name in ("bot.skills.fishing", "bot.skills.actions"):
        sys.modules.pop(name, None)


def test_stuck_monitor_recovers_and_skips_capture(fishing):
    fishing.health_monitor.is_stuck.return_value = True
    fishing.Fish()
    fishing.health_monitor.recover.assert_called_once_with(corrective_action=fishing._recenter_camera)
    fishing.capture_screen.assert_not_called()


def test_missing_screen_records_capture_failure(fishing):
    fishing.capture_screen.return_value = None
    fishing.Fish()
    fishing.health_monitor.record_capture_failure.assert_called_once_with()
    fishing.fish_from_spot.assert_not_called()


def test_failed_ocr_records_capture_failure(fishing):
    fishing.capture_and_process_chat.return_value = ("text", CHAT_IMAGE, False)
    fishing.Fish()
    fishing.health_monitor.record_capture_failure.assert_called_once_with()
    fishing.fish_from_spot.assert_not_called()


def test_normal_chat_fishes_and_sleeps_a_minute(fishing):
    fishing.capture_and_process_chat.return_value = ("You catch a shrimp", CHAT_IMAGE, True)
    fishing.Fish()
    fishing.fish_from_spot.assert_called_once_with("You catch a shrimp", 0)
    assert fishing.CLICK_COUNTER == 7
    fishing.checkpoint_logger.record_action.assert_called_once_with("fish_from_spot")
    fishing.health_monitor.record_activity.assert_called_once_with(verified=False)
    fishing.sleep_mock.assert_called_once_with(60)


def test_teleport_question_is_answered_with_text_after_colon(fishing):
    fishing.capture_and_process_chat.return_value = (
        "You have been teleported: What is 2+2?",
        CHAT_IMAGE,
        True,
    )
    fishing.Fish()
    fishing.respond_to_question.assert_called_once_with("What is 2+2?", CHAT_IMAGE)
    fishing.health_monitor.record_activity.assert_called_once_with(verified=True)
    fishing.fish_from_spot.assert_not_called()


def test_teleport_without_colon_passes_whole_stripped_text(fishing):
    fishing.capture_and_process_chat.return_value = ("  You were teleported  ", CHAT_IMAGE, True)
    fishing.Fish()
    fishing.respond_to_question.assert_called_once_with("You were teleported", CHAT_IMAGE)
    fishing.fish_from_spot.assert_not_called()


def test_paused_loop_sleeps_and_never_captures(fishing):
    fishing.PAUSE_FISHING = True
    fishing.Fish()
    fishing.sleep_mock.assert_called_once_with(1)
    fishing.handle_user_input.assert_called_once_with()
    fishing.capture_screen.assert_not_called()


def test_capture_exception_is_summarized_and_reraised(fishing):
    boom = RuntimeError("capture exploded")
    fishing.capture_screen.side_effect = boom
    with pytest.raises(RuntimeError, match="capture exploded"):
        fishing.Fish()
    fishing.checkpoint_logger.summarize_failure.assert_called_once_with(boom, fishing.health_monitor)


def test_handle_user_input_toggles_pause_and_beeps_on_f1(fishing):
    with patch.object(fishing.keyboard, "is_pressed", return_value=True), \
            patch.object(fishing.winsound, "Beep") as beep:
        fishing.real_handle_user_input()
        assert fishing.PAUSE_FISHING is True
        beep.assert_called_once_with(1000, 500)
        fishing.real_handle_user_input()
        assert fishing.PAUSE_FISHING is False


def test_handle_user_input_does_nothing_without_f1(fishing):
    with patch.object(fishing.keyboard, "is_pressed", return_value=False), \
            patch.object(fishing.winsound, "Beep") as beep:
        fishing.real_handle_user_input()
    assert fishing.PAUSE_FISHING is False
    beep.assert_not_called()
    fishing.sleep_mock.assert_not_called()
