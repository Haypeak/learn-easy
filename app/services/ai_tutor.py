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


import llm

# Load your local DeepSeek model
# model_path = "C:/Users/Hughe/.lmstudio/models/lmstudio-community/DeepSeek-R1-Distill-Llama-8B-GGUF/deepseek-r1.gguf"

# llm.register_model("deepseek", model_path)

# Retrieve the model
try:
    model = llm.get_model("gpt-4o-mini")
except llm.UnknownModelError as e:
    print(f"Error: {e}")


def generate_personalized_model(user_id, user_prefs):
    """
    Generates a user-specific model instance with memory and preferences.
    """
    # Retrieve user preferences (e.g., preferred difficulty level, topic focus)
    learning_style = user_prefs.get("learning_style", "visual")
    difficulty = user_prefs.get("difficulty", "medium")

    # Create an instance of the Model
    user_model = llm.Model


    # Set properties or configurations if applicable
    user_model.set_memory(user_id)
    user_model.set_learning_style(learning_style)
    user_model.set_difficulty(difficulty)
    user_model.set_model(model)

    # Define a personalized prompt
    system_prompt = f"""
    You are an AI tutor. The user prefers {learning_style} learning.
    Adjust explanations to a {difficulty} difficulty level.
    Provide interactive examples and questions where applicable.
    """
    user_model.set_prompt(system_prompt)
    
    return user_model



def ask_personalized_tutor(user_id, user_prefs, question):
    """
    Uses the personalized LLM model to generate a response.
    """
    user_model = generate_personalized_model(user_id, user_prefs)

    # Generate response
    response = user_model.prompt(question)
    return response



# import torch
# from gguf import GGUFModel
# from transformers import AutoTokenizer, AutoModelForCausalLM



# # tokenizer = AutoTokenizer.from_pretrained("deepseek-ai/DeepSeek-R1-Distill-Llama-8B")
# # model = AutoModelForCausalLM.from_pretrained("deepseek-ai/DeepSeek-R1-Distill-Llama-8B")

# # Path to your locally downloaded DeepSeek model
# MODEL_PATH = r'c:\Users\Hughe\.lmstudio\models\lmstudio-community\DeepSeek-R1-Distill-Llama-8B-GGUF'

# # Load tokenizer and model from local storage
# tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
# # model = AutoModelForCausalLM.from_pretrained(MODEL_PATH, torch_dtype=torch.float16, device_map="auto")
# model = GGUFModel.from_pretrained(MODEL_PATH)
# def generate_response(prompt):
#     """Generates AI responses using locally stored DeepSeek model."""
#     inputs = tokenizer(prompt, return_tensors="pt").to("cuda" if torch.cuda.is_available() else "cpu")
#     outputs = model.generate(**inputs, max_new_tokens=200)
#     return tokenizer.decode(outputs[0], skip_special_tokens=True)

if __name__ == '__main__':
    question = "What is the importance of adaptive learning?"
    generate_personalized_model("user123", {"learning_style": "visual", "difficulty": "medium"})
    response =ask_personalized_tutor("user123", {"learning_style": "visual", "difficulty": "medium"}, question)
    print(response)