"""Tests for OCR-facing question cleaning, correction, and matching."""
from unittest.mock import patch, MagicMock

from bot.skills.question_handler import (
    DEFAULT_RESPONSE,
    clean_question,
    correct_text,
    lookup_response,
    normalize_for_match,
)


SAMPLE_RESPONSES = {
    "questions": [
        {"question": "What colour is the sky?", "answer": "blue", "type": "logic", "keyword": "sky"},
        {"question": "Who made Runescape?", "answer": "Jagex", "type": "logic", "keyword": "Runescape"},
    ]
}


class TestCleanQuestion:
    """Test stripping of the anti-bot prompt boilerplate and whitespace noise."""

    def test_strips_click_here_prompt(self):
        assert clean_question("What colour is the sky? Click here to continue") == "What colour is the sky?"

    def test_collapses_ocr_whitespace_noise(self):
        # OCR frequently inserts line breaks / doubled spaces mid-sentence.
        noisy = "What   colour\nis the\tsky?"
        assert clean_question(noisy) == "What colour is the sky?"

    def test_handles_empty_string(self):
        assert clean_question("") == ""

    def test_handles_none(self):
        assert clean_question(None) == ""


class TestNormalizeForMatch:
    """Test the case/whitespace-insensitive normalization helper."""

    def test_lowercases(self):
        assert normalize_for_match("SKY") == "sky"

    def test_collapses_whitespace(self):
        assert normalize_for_match("what   colour  is the sky") == "what colour is the sky"

    def test_handles_none(self):
        assert normalize_for_match(None) == ""


class TestCorrectText:
    """Test TextBlob-based correction and its failure handling."""

    def test_returns_corrected_text(self):
        mock_blob = MagicMock()
        mock_blob.correct.return_value = "sky"
        with patch("bot.skills.question_handler.TextBlob", return_value=mock_blob):
            assert correct_text("sky") == "sky"

    def test_falls_back_to_original_text_on_error(self):
        with patch("bot.skills.question_handler.TextBlob", side_effect=RuntimeError("corpus unavailable")):
            assert correct_text("noisy ocr text") == "noisy ocr text"

    def test_handles_none_without_raising(self):
        with patch("bot.skills.question_handler.TextBlob", side_effect=RuntimeError("boom")):
            assert correct_text(None) == ""


class TestLookupResponse:
    """Test end-to-end matching against noisy OCR-style input."""

    def _no_op_correct(self, monkeypatch=None):
        # Keep correction a no-op so these tests exercise matching logic only.
        return patch("bot.skills.question_handler.correct_text", side_effect=lambda t: t)

    def test_exact_match_case_insensitive(self):
        with self._no_op_correct():
            response = lookup_response("what colour is the sky?", SAMPLE_RESPONSES)
        assert response == "blue"

    def test_exact_match_with_prompt_suffix(self):
        with self._no_op_correct():
            response = lookup_response("What colour is the sky? Click here to continue", SAMPLE_RESPONSES)
        assert response == "blue"

    def test_keyword_match_with_noisy_whitespace(self):
        with self._no_op_correct():
            response = lookup_response("Hey,   who   made\nRunescape anyway?", SAMPLE_RESPONSES)
        assert response == "Jagex"

    def test_keyword_match_is_case_insensitive(self):
        with self._no_op_correct():
            response = lookup_response("SKY is what colour today", SAMPLE_RESPONSES)
        assert response == "blue"

    def test_no_match_returns_default_response(self):
        with self._no_op_correct():
            response = lookup_response("completely unrelated garbled ocr noise", SAMPLE_RESPONSES)
        assert response == DEFAULT_RESPONSE

    def test_empty_question_responses_returns_default(self):
        with self._no_op_correct():
            response = lookup_response("what colour is the sky?", {})
        assert response == DEFAULT_RESPONSE

    def test_missing_questions_key_does_not_raise(self):
        with self._no_op_correct():
            response = lookup_response("what colour is the sky?", {"unexpected": []})
        assert response == DEFAULT_RESPONSE
