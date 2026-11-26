"""Tests for bot.skills.actions (click helper, thieving and fishing actions)."""
import configparser
import importlib
import sys
from unittest.mock import MagicMock, patch

import pytest


def _config() -> configparser.ConfigParser:
    cfg = configparser.ConfigParser()
    cfg.read_dict(
        {
            "coordinates": {
                "inventory_slot_1": "10,20",
                "inventory_slot_2": "30,40",
                "stall_position": "100,200",
                "fish_spot_1": "300,400",
            }
        }
    )
    return cfg


@pytest.fixture
def actions():
    """Import bot.skills.actions with a patched config and a stubbed winsound."""
    sys.modules.setdefault("winsound", MagicMock(name="winsound"))
    sys.modules.pop("bot.skills.actions", None)
    with patch("bot.config.load_config", return_value=_config()):
        module = importlib.import_module("bot.skills.actions")
    with patch.object(module.time, "sleep"), patch.object(module.pyautogui, "click") as click, \
            patch.object(module.pyautogui, "typewrite") as typewrite, \
            patch.object(module.pyautogui, "press") as press:
        module.click_mock = click
        module.typewrite_mock = typewrite
        module.press_mock = press
        yield module
    sys.modules.pop("bot.skills.actions", None)


class TestClickWithVariance:
    def test_zero_variance_clicks_exact_coordinates(self, actions):
        actions.click_with_variance(50, 60, variance=0)
        actions.click_mock.assert_called_once_with(50, 60)

    def test_offset_is_applied_to_both_axes(self, actions):
        with patch.object(actions.random, "randint", return_value=3):
            actions.click_with_variance(50, 60, variance=5)
        actions.click_mock.assert_called_once_with(53, 63)


class TestThieveFromStall:
    def test_normal_click_increments_counter(self, actions):
        assert actions.thieve_from_stall("nothing special", 4) == 5
        actions.click_mock.assert_called_once()
        assert actions.click_mock.call_args.args[0] in range(95, 106)

    def test_coin_pouch_at_16_clicks_slot_twice_and_resets(self, actions):
        assert actions.thieve_from_stall("You should empty your coin pouch", 16) == 0
        assert actions.click_mock.call_count == 2
        for call in actions.click_mock.call_args_list:
            assert call.args == (10, 20)

    def test_coin_pouch_at_15_keeps_thieving(self, actions):
        assert actions.thieve_from_stall("You should empty your coin pouch", 15) == 16
        assert actions.click_mock.call_count == 1

    def test_inventory_full_at_16_empties_and_resets(self, actions):
        assert actions.thieve_from_stall("Your inventory is full", 16) == 0
        actions.typewrite_mock.assert_called_once_with("::empty")
        actions.press_mock.assert_called_once_with("enter")
        actions.click_mock.assert_not_called()

    def test_inventory_full_at_15_keeps_thieving(self, actions):
        assert actions.thieve_from_stall("Your inventory is full", 15) == 16
        actions.typewrite_mock.assert_not_called()

    def test_onyx_at_16_beeps_prompts_and_resets(self, actions):
        with patch.object(actions.winsound, "Beep") as beep, \
                patch("builtins.input", return_value="") as prompt:
            assert actions.thieve_from_stall("You found an onyx", 16) == 0
        beep.assert_called_once_with(1000, 500)
        prompt.assert_called_once()
        actions.click_mock.assert_not_called()

    def test_onyx_at_15_keeps_thieving(self, actions):
        with patch.object(actions.winsound, "Beep") as beep, patch("builtins.input") as prompt:
            assert actions.thieve_from_stall("You found an onyx", 15) == 16
        beep.assert_not_called()
        prompt.assert_not_called()


class TestFishFromSpot:
    def test_normal_click_increments_counter(self, actions):
        assert actions.fish_from_spot("fishing...", 2) == 3
        actions.click_mock.assert_called_once()
        assert actions.click_mock.call_args.args[0] in range(295, 306)

    def test_inventory_at_16_empties_and_resets(self, actions):
        assert actions.fish_from_spot("Your inventory is full", 16) == 0
        actions.typewrite_mock.assert_called_once_with("::empty")
        actions.press_mock.assert_called_once_with("enter")
        actions.click_mock.assert_not_called()

    def test_inventory_at_5_keeps_fishing(self, actions):
        assert actions.fish_from_spot("Your inventory is full", 5) == 6
        actions.typewrite_mock.assert_not_called()
        assert actions.click_mock.call_count == 1
