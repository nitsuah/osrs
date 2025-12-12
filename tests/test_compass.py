"""Tests for compass functionality."""
import pytest
from unittest.mock import patch, Mock
from bot.compass import click_compass


class TestClickCompass:
    """Test compass clicking functionality."""

    @patch('bot.compass.pyautogui.click')
    @patch('bot.compass.time.sleep')
    def test_click_compass_calls_pyautogui(self, mock_sleep, mock_click):
        """Test that click_compass calls pyautogui.click with correct coordinates."""
        test_position = (100, 200)
        
        click_compass(test_position)
        
        mock_click.assert_called_once_with(100, 200)
        mock_sleep.assert_called_once_with(1)

    @patch('bot.compass.pyautogui.click')
    @patch('bot.compass.time.sleep')
    def test_click_compass_different_coordinates(self, mock_sleep, mock_click):
        """Test clicking compass at different coordinates."""
        coordinates = [(50, 50), (100, 150), (200, 300)]
        
        for coord in coordinates:
            mock_click.reset_mock()
            click_compass(coord)
            mock_click.assert_called_once_with(coord[0], coord[1])

    @patch('bot.compass.pyautogui.click')
    @patch('bot.compass.time.sleep')
    @patch('bot.compass.logging')
    def test_click_compass_logs_action(self, mock_logging, mock_sleep, mock_click):
        """Test that compass click is logged."""
        test_position = (150, 250)
        
        click_compass(test_position)
        
        mock_logging.info.assert_called_once()
        call_args = mock_logging.info.call_args[0]
        assert "Clicked compass" in call_args[0]
        assert test_position in call_args

    @patch('bot.compass.pyautogui.click')
    @patch('bot.compass.time.sleep')
    def test_click_compass_waits_after_click(self, mock_sleep, mock_click):
        """Test that there's a delay after clicking."""
        test_position = (100, 200)
        
        click_compass(test_position)
        
        # Verify sleep is called after click
        assert mock_click.called
        assert mock_sleep.called
