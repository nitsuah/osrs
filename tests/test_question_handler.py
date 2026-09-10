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

    def test_strips_click_here_prompt_case_insensitively(self):
        # OCR sometimes reads the prompt in all-caps or mixed case.
        assert clean_question("What colour is the sky? CLICK HERE TO CONTINUE") == "What colour is the sky?"
        assert clean_question("What colour is the sky? Click Here To Continue") == "What colour is the sky?"

    def test_strips_click_here_prompt_with_ocr_whitespace_noise(self):
        assert clean_question("What colour is the sky? Click  here\nto   continue") == "What colour is the sky?"

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

    def test_null_questions_value_does_not_raise(self):
        # A hand-edited questions.json can legitimately have {"questions": null}.
        with self._no_op_correct():
            response = lookup_response("what colour is the sky?", {"questions": None})
        assert response == DEFAULT_RESPONSE

    def test_non_list_questions_value_does_not_raise(self):
        with self._no_op_correct():
            response = lookup_response("what colour is the sky?", {"questions": "not a list"})
        assert response == DEFAULT_RESPONSE

    def test_non_dict_entry_is_skipped_without_raising(self):
        malformed = {"questions": ["not a dict", {"question": "who made runescape?", "answer": "Jagex", "keyword": "Runescape"}]}
        with self._no_op_correct():
            response = lookup_response("who made runescape?", malformed)
        assert response == "Jagex"

    def test_entry_missing_answer_key_falls_back_to_default(self):
        malformed = {"questions": [{"question": "what colour is the sky?", "keyword": "sky"}]}
        with self._no_op_correct():
            response = lookup_response("what colour is the sky?", malformed)
        assert response == DEFAULT_RESPONSE

    def test_entry_with_non_string_field_is_skipped_without_raising(self):
        # A hand-edited questions.json could have a non-string value for
        # question/keyword/answer (e.g. a stray number or nested object).
        # normalize_for_match assumes a string, so this must be skipped
        # rather than crash the bot mid-loop.
        malformed = {
            "questions": [
                {"question": 12345, "keyword": "sky", "answer": "wrong"},
                {"question": "who made runescape?", "keyword": ["Runescape"], "answer": "wrong"},
                {"question": "what colour is the sky?", "keyword": "sky", "answer": {"nested": True}},
                {"question": "who made runescape?", "keyword": "Runescape", "answer": "Jagex"},
            ]
        }
        with self._no_op_correct():
            response = lookup_response("who made runescape?", malformed)
        assert response == "Jagex"
