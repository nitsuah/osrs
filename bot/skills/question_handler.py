import os
import json
import logging
from textblob import TextBlob

questions_file_path = os.path.join(os.path.dirname(__file__), 'questions.json')


def load_question_responses() -> dict:
    try:
        with open(questions_file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.error("Error loading questions: %s", e)
        return {}


def clean_question(question: str) -> str:
    logging.info("Cleaning question: '%s'", question)
    return question.replace("Click here to continue", "").strip()


def correct_text(text: str) -> str:
    blob = TextBlob(text)
    logging.info("Correcting text using blob: '%s' to '%s'", text, str(blob.correct()))
    return str(blob.correct())


def lookup_response(question: str, question_responses: dict) -> str:
    cleaned_question = clean_question(question)
    logging.info("Cleaned Question: '%s'", cleaned_question)
    corrected_question = correct_text(question)
    logging.info("Corrected Question: '%s'", corrected_question)
    for entry in question_responses['questions']:
        # logging the check for debugging
        if cleaned_question == entry['question'].lower():
            return entry['answer']  # Return the exact answer
        elif entry['keyword'].lower() in cleaned_question:
            return entry['answer']  # Fallback to keyword match
        elif entry['keyword'].lower() in corrected_question:
            return entry['answer']  # Fallback to keyword match in corrected question
    return "bald"  # Default response if no match - need chatgpt to generate a last ditch response
