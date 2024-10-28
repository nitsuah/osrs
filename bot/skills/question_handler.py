import os
import json
import logging
from textblob import TextBlob

questions_file_path = os.path.join(os.path.dirname(__file__), 'questions.json')

def load_question_responses():
    try:
        with open(questions_file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.error("Error loading questions: %s", e)
        return {}

def clean_question(question):
    print(f"Cleaning question: '{question}'")
    return question.replace("Click here to continue", "").strip()

def correct_text(text):
    blob = TextBlob(text)
    print(f"Correcting text using blob: '{text}' to '{str(blob.correct())}'")
    return str(blob.correct())

def lookup_response(question, question_responses):
    cleaned_question = clean_question(question)
    logging.info("Cleaned Question: '%s'", cleaned_question)
    for entry in question_responses['questions']:
        logging.info("Checking entry: '%s' with keyword: '%s'", entry['question'], entry['keyword'])
        if cleaned_question == entry['question'].lower():
            return entry['answer']  # Return the exact answer
        elif entry['keyword'].lower() in cleaned_question:
            return entry['answer']  # Fallback to keyword match
    return "bald"  # Default response if no match
