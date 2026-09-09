"""Tests for OCR chat-region capture and its failure handling."""
import numpy as np
from unittest.mock import patch

from bot.skills.screen_processing import capture_and_process_chat, save_screenshot


# A tiny fake "screen" big enough to slice a chat region out of.
FAKE_SCREEN = np.zeros((100, 100, 3), dtype=np.uint8)
CHAT_REGION = (0, 0, 50, 50)


class TestCaptureAndProcessChat:
    """Test chat-region OCR extraction, including noisy/failure cases."""

    @patch("bot.skills.screen_processing.pytesseract.image_to_string")
    def test_returns_ocr_text_and_cropped_image(self, mock_ocr):
        mock_ocr.return_value = "What colour is the sky?"

        chat_text, chat_image = capture_and_process_chat(FAKE_SCREEN, CHAT_REGION)

        assert chat_text == "What colour is the sky?"
        assert chat_image.shape == (50, 50, 3)

    @patch("bot.skills.screen_processing.pytesseract.image_to_string")
    def test_crops_the_requested_region(self, mock_ocr):
        mock_ocr.return_value = ""
        region = (10, 20, 40, 60)

        _, chat_image = capture_and_process_chat(FAKE_SCREEN, region)

        assert chat_image.shape == (40, 30, 3)  # (y2-y1, x2-x1, channels)

    @patch("bot.skills.screen_processing.pytesseract.image_to_string")
    def test_ocr_failure_returns_empty_text_instead_of_raising(self, mock_ocr):
        mock_ocr.side_effect = RuntimeError("tesseract is not installed or it's not in your PATH")

        chat_text, chat_image = capture_and_process_chat(FAKE_SCREEN, CHAT_REGION)

        assert chat_text == ""
        assert chat_image is not None  # the crop should still be returned for screenshotting

    @patch("bot.skills.screen_processing.pytesseract.image_to_string")
    @patch("bot.skills.screen_processing.logging")
    def test_ocr_failure_logs_the_error(self, mock_logging, mock_ocr):
        mock_ocr.side_effect = RuntimeError("boom")

        capture_and_process_chat(FAKE_SCREEN, CHAT_REGION)

        assert mock_logging.error.called

    @patch("bot.skills.screen_processing.pytesseract.image_to_string")
    def test_noisy_ocr_output_is_passed_through_unmodified(self, mock_ocr):
        # capture_and_process_chat itself doesn't clean text -- that's
        # question_handler's job -- so raw noisy OCR output should round-trip.
        mock_ocr.return_value = "What   colour\nis the\tsky?  \n\n"

        chat_text, _ = capture_and_process_chat(FAKE_SCREEN, CHAT_REGION)

        assert chat_text == "What   colour\nis the\tsky?  \n\n"


class TestSaveScreenshot:
    """Test debug-screenshot saving, including a read-only filesystem."""

    @patch("bot.skills.screen_processing.cv2.imwrite")
    @patch("bot.skills.screen_processing.os.makedirs")
    def test_saves_to_the_screenshot_directory(self, mock_makedirs, mock_imwrite):
        save_screenshot(FAKE_SCREEN)

        mock_makedirs.assert_called_once()
        assert mock_imwrite.called

    @patch("bot.skills.screen_processing.os.makedirs", side_effect=PermissionError("read-only filesystem"))
    def test_permission_error_does_not_raise(self, mock_makedirs):
        # Should not raise even though the directory can't be created
        # (e.g. the non-root Docker runtime user has no write access).
        save_screenshot(FAKE_SCREEN)

    @patch("bot.skills.screen_processing.os.makedirs", side_effect=PermissionError("read-only filesystem"))
    @patch("bot.skills.screen_processing.logging")
    def test_permission_error_logs_the_failure(self, mock_logging, mock_makedirs):
        save_screenshot(FAKE_SCREEN)

        assert mock_logging.error.called
