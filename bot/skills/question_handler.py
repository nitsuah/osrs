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


# OCR output can vary in case ("CLICK HERE TO CONTINUE") and insert stray
# whitespace inside the phrase, so this is matched case-insensitively with
# whitespace runs treated as a single space -- a plain str.replace() only
# ever matched the exact title-case string.
_CLICK_HERE_RE = re.compile(r"click\s+here\s+to\s+continue", re.IGNORECASE)


def clean_question(question: str) -> str:
    logging.info("Cleaning question: '%s'", question)
    without_prompt = _CLICK_HERE_RE.sub("", question or "")
    return _WHITESPACE_RE.sub(" ", without_prompt).strip()


def normalize_for_match(text: str) -> str:
    """Lower-case and whitespace-normalize text for case/spacing-insensitive matching.

    OCR output frequently varies in case and inserts stray whitespace runs
    (doubled spaces, tabs) between words, so every comparison in
    `lookup_response` should go through this instead of comparing raw strings.
    This collapses whitespace runs to a single space -- it does not remove
    whitespace entirely, so a line break that splits a single word in two
    ("Runes\ncape") still normalizes to two words ("runes cape"), not one
    ("runescape"). For that intra-token case, see `squash_for_match`.
    """
    return _WHITESPACE_RE.sub(" ", (text or "")).strip().lower()


def squash_for_match(text: str) -> str:
    """Like `normalize_for_match`, but removes whitespace entirely.

    OCR can legitimately break a single word across two lines when chat text
    wraps mid-token (no hyphen inserted), which `normalize_for_match` alone
    can't compensate for -- "Runes\ncape" normalizes to "runes cape", which
    will never match the keyword "runescape". `lookup_response` tries this
    squashed form as a fallback after the normalized one.
    """
    return _WHITESPACE_RE.sub("", (text or "")).strip().lower()


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
    squashed_cleaned = squash_for_match(cleaned_question)
    squashed_corrected = squash_for_match(corrected_question)

    # questions.json is hand-edited, so `question_responses` may legitimately
    # be malformed (not a dict at all, {"questions": null}, "questions"
    # missing entirely, a non-list value, or an entry that isn't an object)
    # -- none of that should ever crash the bot mid-loop, it should just
    # fall through to DEFAULT_RESPONSE like "no match found" does.
    entries = (
        question_responses.get('questions')
        if isinstance(question_responses, dict)
        else None
    )
    if not isinstance(entries, list):
        entries = []

    for entry in entries:
        if not isinstance(entry, dict):
            continue
        # A hand-edited questions.json can have a non-string value for any
        # of these fields (e.g. a number or nested object) -- normalize_for_match
        # assumes a string and would raise on anything else, so skip entries
        # that don't hold up their end of the contract rather than crashing
        # the bot mid-loop.
        raw_question = entry.get('question', '')
        raw_keyword = entry.get('keyword', '')
        raw_answer = entry.get('answer', DEFAULT_RESPONSE)
        if not (
            isinstance(raw_question, str)
            and isinstance(raw_keyword, str)
            and isinstance(raw_answer, str)
        ):
            continue
        entry_question = normalize_for_match(raw_question)
        entry_keyword = normalize_for_match(raw_keyword)
        squashed_keyword = squash_for_match(raw_keyword)
        # Logging the check for debugging.
        if normalized_cleaned == entry_question:
            return raw_answer  # Return the exact answer
        elif entry_keyword and entry_keyword in normalized_cleaned:
            return raw_answer  # Fallback to keyword match
        elif entry_keyword and entry_keyword in normalized_corrected:
            return raw_answer  # Fallback to keyword match in corrected question
        elif squashed_keyword and squashed_keyword in squashed_cleaned:
            # A line break inside a single OCR'd word ("Runes\ncape") survives
            # normalize_for_match as two words -- try the whitespace-free form
            # too before giving up on this entry.
            return raw_answer
        elif squashed_keyword and squashed_keyword in squashed_corrected:
            return raw_answer
    return DEFAULT_RESPONSE  # Default response if no match found
