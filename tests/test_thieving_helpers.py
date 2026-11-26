"""Tests for the helper functions in bot.skills.thieving."""
import configparser
import importlib
import sys
from unittest.mock import MagicMock, patch

import pytest


def _config() -> configparser.ConfigParser:
    cfg = configparser.ConfigParser(inline_comment_prefixes=None)
    cfg.read_dict(
        {
            "coordinates": {
                "chat_region": "0,0,100,50  # comment",
                "inventory_slot_1": "10,20",
                "inventory_slot_2": "30,40",
                "stall_position": "100,200",
                "fish_spot_1": "300,400",
            }
        }
    )
    return cfg


@pytest.fixture
def thieving():
    """Import bot.skills.thieving with platform modules stubbed and config patched."""
    for name in ("winsound", "keyboard", "pynput", "pynput.mouse", "pynput.keyboard"):
        sys.modules.setdefault(name, MagicMock(name=name))
    for name in ("bot.skills.thieving", "bot.skills.actions"):
        sys.modules.pop(name, None)
    question_handler = importlib.import_module("bot.skills.question_handler")
    with patch("bot.config.load_config", return_value=_config()), \
            patch.object(question_handler, "load_question_responses", return_value={}):
        module = importlib.import_module("bot.skills.thieving")

    saved = module.PAUSE_THIEVING
    module.PAUSE_THIEVING = False
    with patch.object(module.time, "sleep"), \
            patch.object(module.pyautogui, "press") as press, \
            patch.object(module.pyautogui, "typewrite") as typewrite, \
            patch.object(module.winsound, "Beep") as beep:
        module.press_mock = press
        module.typewrite_mock = typewrite
        module.beep_mock = beep
        yield module
    module.PAUSE_THIEVING = saved
    for name in ("bot.skills.thieving", "bot.skills.actions"):
        sys.modules.pop(name, None)


def test_chat_region_strips_the_inline_comment(thieving):
    assert thieving.chat_region == (0, 0, 100, 50)


def test_respond_to_question_types_the_known_answer(thieving):
    with patch.object(thieving, "lookup_response", return_value="42"), \
            patch.object(thieving, "save_screenshot") as shot:
        thieving.respond_to_question("What is 6*7?", object())
    thieving.press_mock.assert_any_call("space")
    thieving.typewrite_mock.assert_called_once_with("42")
    thieving.press_mock.assert_called_with("enter")
    shot.assert_not_called()
    thieving.beep_mock.assert_not_called()


def test_respond_to_question_default_beeps_saves_and_waits(thieving):
    image = object()
    with patch.object(thieving, "lookup_response", return_value=thieving.DEFAULT_RESPONSE), \
            patch.object(thieving, "save_screenshot") as shot, \
            patch("builtins.input", return_value="") as prompt:
        thieving.respond_to_question("unknown?", image)
    thieving.beep_mock.assert_called_once_with(500, 500)
    shot.assert_called_once_with(image)
    prompt.assert_called_once()
    thieving.typewrite_mock.assert_not_called()
    thieving.press_mock.assert_not_called()


def test_f1_toggles_pause_and_beeps(thieving):
    with patch.object(thieving.keyboard, "is_pressed", return_value=True):
        thieving.handle_user_input()
        assert thieving.PAUSE_THIEVING is True
        thieving.beep_mock.assert_called_once_with(1000, 500)
        thieving.handle_user_input()
        assert thieving.PAUSE_THIEVING is False


def test_unpressed_f1_leaves_pause_unchanged(thieving):
    with patch.object(thieving.keyboard, "is_pressed", return_value=False):
        thieving.handle_user_input()
    assert thieving.PAUSE_THIEVING is False
    thieving.beep_mock.assert_not_called()


def test_recenter_camera_zooms_in_five_steps(thieving):
    with patch.object(thieving, "check_and_zoom_in") as zoom:
        thieving._recenter_camera()
    zoom.assert_called_once_with(5)
