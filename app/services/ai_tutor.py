# import torch
# from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

# # Load pre-trained AI tutor model
# tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-cnn")
# model = AutoModelForSeq2SeqLM.from_pretrained("facebook/bart-large-cnn")

# def ask_ai(question):
#     """ AI tutor processes student questions and provides explanations """
#     inputs = tokenizer(question, return_tensors="pt", truncation=True, max_length=512)
#     outputs = model.generate(**inputs, max_length=200)
#     response = tokenizer.decode(outputs[0], skip_special_tokens=True)
#     return response

from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Path to your locally downloaded DeepSeek model

MODEL_PATH = 'deepseek-ai/DeepSeek-R1'  # Change this to your actual model path

# Load tokenizer and model from local storage
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForCausalLM.from_pretrained(MODEL_PATH, torch_dtype=torch.float16, device_map="auto")

def generate_response(prompt):
    """Generates AI responses using locally stored DeepSeek model."""
    inputs = tokenizer(prompt, return_tensors="pt").to("cuda" if torch.cuda.is_available() else "cpu")
    outputs = model.generate(**inputs, max_new_tokens=200)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# Test
question = "What is the importance of adaptive learning?"
response = generate_response(question)
print(response)
