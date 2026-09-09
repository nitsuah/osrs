import os
import json
import logging
import re
from textblob import TextBlob

questions_file_path = os.path.join(os.path.dirname(__file__), 'questions.json')

# Returned when no question/keyword match is found (also used by callers to
# detect the "no confident answer" case, e.g. to pause and screenshot).
DEFAULT_RESPONSE = "bald"

# Collapse OCR-introduced whitespace runs (newlines, tabs, double spaces)
# down to a single space so keyword matching isn't defeated by noise.
_WHITESPACE_RE = re.compile(r"\s+")


def load_question_responses() -> dict:
    try:
        with open(questions_file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.error("Error loading questions: %s", e)
        return {}


def clean_question(question: str) -> str:
    logging.info("Cleaning question: '%s'", question)
    without_prompt = (question or "").replace("Click here to continue", "")
    return _WHITESPACE_RE.sub(" ", without_prompt).strip()


def normalize_for_match(text: str) -> str:
    """Lower-case and whitespace-normalize text for case/spacing-insensitive matching.

    OCR output frequently varies in case and inserts stray whitespace runs
    (line breaks mid-word, doubled spaces), so every comparison in
    `lookup_response` should go through this instead of comparing raw strings.
    """
    return _WHITESPACE_RE.sub(" ", (text or "")).strip().lower()


def correct_text(text: str) -> str:
    try:
        blob = TextBlob(text or "")
        corrected = str(blob.correct())
    except Exception as e:  # pragma: no cover - defensive against textblob/corpus errors
        logging.error("Error correcting text '%s': %s", text, e)
        return text or ""
    logging.info("Correcting text using blob: '%s' to '%s'", text, corrected)
    return corrected


def lookup_response(question: str, question_responses: dict) -> str:
    cleaned_question = clean_question(question)
    logging.info("Cleaned Question: '%s'", cleaned_question)
    # Correct the already-cleaned text (not the raw OCR string) so spell
    # correction isn't fighting leftover prompt text/whitespace noise.
    corrected_question = correct_text(cleaned_question)
    logging.info("Corrected Question: '%s'", corrected_question)

    normalized_cleaned = normalize_for_match(cleaned_question)
    normalized_corrected = normalize_for_match(corrected_question)

    entries = question_responses.get('questions', []) if question_responses else []
    for entry in entries:
        entry_question = normalize_for_match(entry.get('question', ''))
        entry_keyword = normalize_for_match(entry.get('keyword', ''))
        # Logging the check for debugging.
        if normalized_cleaned == entry_question:
            return entry['answer']  # Return the exact answer
        elif entry_keyword and entry_keyword in normalized_cleaned:
            return entry['answer']  # Fallback to keyword match
        elif entry_keyword and entry_keyword in normalized_corrected:
            return entry['answer']  # Fallback to keyword match in corrected question
    return DEFAULT_RESPONSE  # Default response if no match found
