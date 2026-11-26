"""Tests recorder functionality."""
import sys
from types import ModuleType
from unittest.mock import MagicMock, patch, call

import pytest


# Stub pynput before importing bot.recorder so the Linux runner never imports real pynput
pynput_stub = ModuleType("pynput")
pynput_stub.mouse = ModuleType("pynput.mouse")
pynput_stub.mouse.Listener = MagicMock(name="pynput.mouse.Listener")
pynput_stub.keyboard = ModuleType("pynput.keyboard")
pynput_stub.keyboard.Listener = MagicMock(name="pynput.keyboard.Listener")
sys.modules["pynput"] = pynput_stub
sys.modules["pynput.mouse"] = pynput_stub.mouse
sys.modules["pynput.keyboard"] = pynput_stub.keyboard

import bot.recorder as recorder


@pytest.fixture(autouse=True)
def _reset_click_data(tmp_path):
    """Clear click_data and patch FILENAME to a temp CSV before each test."""
    recorder.click_data.clear()
    recorder.FILENAME = str(tmp_path / "mouse_clicks.csv")
    yield


class TestOnClick:
    """Test the on_click callback."""

    @patch("bot.recorder.time.time", return_value=123.5)
    def test_on_click_pressed_appends_row(self, mock_time):
        """Pressed click appends [timestamp, x, y, button]."""
        recorder.on_click(10, 20, "left", True)

        assert recorder.click_data == [[123.5, 10, 20, "left"]]

    @patch("bot.recorder.time.time", return_value=123.5)
    def test_on_click_not_pressed_appends_nothing(self, mock_time):
        """Released click appends nothing."""
        recorder.on_click(10, 20, "left", False)

        assert recorder.click_data == []


class TestOnPress:
    """Test the on_press callback."""

    def test_on_press_q_returns_false(self):
        """Key 'q' returns False to stop listener."""
        key = MagicMock()
        key.char = "q"

        result = recorder.on_press(key)

        assert result is False

    def test_on_press_other_char_returns_none(self):
        """Other char keys return None (continue)."""
        key = MagicMock()
        key.char = "a"

        result = recorder.on_press(key)

        assert result is None

    def test_on_press_no_char_does_not_raise(self):
        """Key without .char (e.g., Shift) does not raise."""
        key = MagicMock(spec=[])  # No .char attribute

        result = recorder.on_press(key)

        assert result is None


class TestSaveClicks:
    """Test the save_clicks function."""

    def test_save_clicks_writes_header_and_rows(self, tmp_path):
        """Recorded rows are written with header."""
        recorder.click_data.extend([
            [123.5, 10, 20, "left"],
            [124.0, 30, 40, "right"],
        ])

        recorder.save_clicks()

        import csv
        with open(recorder.FILENAME, newline="") as f:
            rows = list(csv.reader(f))

        assert rows[0] == ["Timestamp", "X", "Y", "Button"]
        assert rows[1] == ["123.5", "10", "20", "left"]
        assert rows[2] == ["124.0", "30", "40", "right"]

    def test_save_clicks_empty_writes_header_only(self, tmp_path):
        """Empty click data writes only the header."""
        recorder.save_clicks()

        import csv
        with open(recorder.FILENAME, newline="") as f:
            rows = list(csv.reader(f))

        assert rows == [["Timestamp", "X", "Y", "Button"]]

    def test_save_clicks_prints_filename(self, tmp_path, capsys):
        """Save prints the filename."""
        recorder.save_clicks()

        captured = capsys.readouterr()
        assert recorder.FILENAME in captured.out


class TestRecordMouseClicks:
    """Test the record_mouse_clicks main function."""

    @patch("bot.recorder.save_clicks")
    def test_record_mouse_clicks_starts_listeners_and_saves(self, mock_save):
        """Starts both listeners, joins each, then calls save_clicks once."""
        mock_mouse_listener = MagicMock()
        mock_keyboard_listener = MagicMock()

        # Context managers return the listener mocks
        recorder.mouse.Listener.return_value.__enter__.return_value = mock_mouse_listener
        recorder.keyboard.Listener.return_value.__enter__.return_value = mock_keyboard_listener

        recorder.record_mouse_clicks()

        # Both Listener context managers entered
        recorder.mouse.Listener.assert_called_once_with(on_click=recorder.on_click)
        recorder.keyboard.Listener.assert_called_once_with(on_press=recorder.on_press)

        # Both listeners joined
        mock_mouse_listener.join.assert_called_once()
        mock_keyboard_listener.join.assert_called_once()

        # save_clicks called exactly once after listeners exit
        mock_save.assert_called_once()
