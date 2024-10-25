import json
import logging
from textblob import TextBlob
import os

questions_file_path = os.path.join(os.path.dirname(__file__), 'questions.json')

def load_question_responses():
    try:
        with open(questions_file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.error("Error loading questions: %s", e)
        return {}

def clean_question(question):
    return question.lower().replace("click here to continue", "").strip()

def correct_text(text):
    blob = TextBlob(text)
    return str(blob.correct())

def lookup_response(question, question_responses):
    cleaned_question = clean_question(question)
    for entry in question_responses['questions']:
        if cleaned_question == entry['question'].lower() or entry['keyword'].lower() in cleaned_question:
            return entry['answer'].capitalize()
    return "bald"  # Default response if no match
