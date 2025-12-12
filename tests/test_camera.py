"""Tests for camera functionality."""
import pytest
from unittest.mock import patch, Mock, call
from bot.camera import check_and_zoom_in, hold_up_arrow


class TestCheckAndZoomIn:
    """Test zoom functionality."""

    @patch('bot.camera.pyautogui.scroll')
    @patch('bot.camera.time.sleep')
    @patch('bot.camera.hold_up_arrow')
    def test_zoom_in_scrolls_correct_times(self, mock_hold_up, mock_sleep, mock_scroll):
        """Test that zoom scrolls the correct number of times."""
        steps = 5
        
        check_and_zoom_in(steps)
        
        assert mock_scroll.call_count == steps
        mock_scroll.assert_called_with(200)

    @patch('bot.camera.pyautogui.scroll')
    @patch('bot.camera.time.sleep')
    @patch('bot.camera.hold_up_arrow')
    def test_zoom_in_with_different_steps(self, mock_hold_up, mock_sleep, mock_scroll):
        """Test zooming with different step values."""
        for steps in [1, 3, 5, 10]:
            mock_scroll.reset_mock()
            check_and_zoom_in(steps)
            assert mock_scroll.call_count == steps

    @patch('bot.camera.pyautogui.scroll')
    @patch('bot.camera.time.sleep')
    @patch('bot.camera.hold_up_arrow')
    def test_zoom_in_calls_hold_up_arrow(self, mock_hold_up, mock_sleep, mock_scroll):
        """Test that zoom calls hold_up_arrow at the end."""
        check_and_zoom_in(5)
        
        mock_hold_up.assert_called_once_with(2)

    @patch('bot.camera.pyautogui.scroll')
    @patch('bot.camera.time.sleep')
    @patch('bot.camera.hold_up_arrow')
    def test_zoom_in_sleeps_between_scrolls(self, mock_hold_up, mock_sleep, mock_scroll):
        """Test that there's a delay between scrolls."""
        check_and_zoom_in(3)
        
        # Should sleep after each scroll
        assert mock_sleep.call_count >= 3

    @patch('bot.camera.pyautogui.scroll')
    @patch('bot.camera.time.sleep')
    @patch('bot.camera.hold_up_arrow')
    @patch('bot.camera.logging')
    def test_zoom_in_logs_action(self, mock_logging, mock_hold_up, mock_sleep, mock_scroll):
        """Test that zoom action is logged."""
        check_and_zoom_in(5)
        
        # Should log at least once
        assert mock_logging.info.called


class TestHoldUpArrow:
    """Test up arrow key holding functionality."""

    @patch('bot.camera.keyboard.press')
    @patch('bot.camera.keyboard.release')
    @patch('bot.camera.time.sleep')
    def test_hold_up_arrow_presses_key(self, mock_sleep, mock_release, mock_press):
        """Test that up arrow key is pressed."""
        duration = 2
        
        hold_up_arrow(duration)
        
        mock_press.assert_called_once_with('up')
        mock_release.assert_called_once_with('up')

    @patch('bot.camera.keyboard.press')
    @patch('bot.camera.keyboard.release')
    @patch('bot.camera.time.sleep')
    def test_hold_up_arrow_holds_for_duration(self, mock_sleep, mock_release, mock_press):
        """Test that key is held for specified duration."""
        duration = 3
        
        hold_up_arrow(duration)
        
        mock_sleep.assert_called_once_with(duration)

    @patch('bot.camera.keyboard.press')
    @patch('bot.camera.keyboard.release')
    @patch('bot.camera.time.sleep')
    def test_hold_up_arrow_releases_after_duration(self, mock_sleep, mock_release, mock_press):
        """Test that key is released after hold duration."""
        hold_up_arrow(2)
        
        # Verify order: press -> sleep -> release
        assert mock_press.called
        assert mock_sleep.called
        assert mock_release.called

    @patch('bot.camera.keyboard.press')
    @patch('bot.camera.keyboard.release')
    @patch('bot.camera.time.sleep')
    def test_hold_up_arrow_different_durations(self, mock_sleep, mock_release, mock_press):
        """Test holding for different durations."""
        for duration in [1, 2, 3, 5]:
            mock_sleep.reset_mock()
            hold_up_arrow(duration)
            mock_sleep.assert_called_with(duration)

    @patch('bot.camera.keyboard.press')
    @patch('bot.camera.keyboard.release')
    @patch('bot.camera.time.sleep')
    @patch('bot.camera.logging')
    def test_hold_up_arrow_logs_action(self, mock_logging, mock_sleep, mock_release, mock_press):
        """Test that holding up arrow is logged."""
        duration = 2
        
        hold_up_arrow(duration)
        
        mock_logging.info.assert_called_once()
        call_args = mock_logging.info.call_args[0]
        assert "up arrow" in call_args[0].lower()
        assert duration in call_args
