# routes/questions.py
from flask import Blueprint, request, jsonify
import os
from werkzeug.utils import secure_filename
from PyPDF2 import PdfReader
from docx import Document
from transformers import pipeline

questions_bp = Blueprint('questions', __name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load the question generation model
question_generator = pipeline("text2text-generation")

@questions_bp.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify(message='No file part'), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify(message='No selected file'), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)

    text = ''
    if filename.endswith('.pdf'):
        with open(file_path, 'rb') as f:
            reader = PdfReader(f)
            text = ''.join(page.extract_text() for page in reader.pages)
    elif filename.endswith('.docx'):
        doc = Document(file_path)
        text = '\n'.join(paragraph.text for paragraph in doc.paragraphs)
    elif filename.endswith('.txt'):
        with open(file_path, 'r') as f:
            text = f.read()

    questions = generate_questions(text)
    os.remove(file_path)  # Clean up the uploaded file

    return jsonify(questions=questions)

def generate_questions(text):
    # Use the question generation model to generate questions
    questions = question_generator(text)
    return questions
