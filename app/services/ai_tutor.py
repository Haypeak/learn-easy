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


# import llm

# # Load your local DeepSeek model
# # model_path = "C:/Users/Hughe/.lmstudio/models/lmstudio-community/DeepSeek-R1-Distill-Llama-8B-GGUF/deepseek-r1.gguf"

# # llm.register_model("deepseek", model_path)

# # Retrieve the model
# try:
#     model = llm.get_model("gpt-4o-mini")
# except llm.UnknownModelError as e:
#     print(f"Error: {e}")


# def generate_personalized_model(user_id, user_prefs):
#     """
#     Generates a user-specific model instance with memory and preferences.
#     """
#     # Retrieve user preferences (e.g., preferred difficulty level, topic focus)
#     learning_style = user_prefs.get("learning_style", "visual")
#     difficulty = user_prefs.get("difficulty", "medium")

#     # Create an instance of the Model
#     user_model = llm.Model


#     # Set properties or configurations if applicable
#     user_model.set_memory(user_id)
#     user_model.set_learning_style(learning_style)
#     user_model.set_difficulty(difficulty)
#     user_model.set_model(model)

#     # Define a personalized prompt
#     system_prompt = f"""
#     You are an AI tutor. The user prefers {learning_style} learning.
#     Adjust explanations to a {difficulty} difficulty level.
#     Provide interactive examples and questions where applicable.
#     """
#     user_model.set_prompt(system_prompt)
    
#     return user_model



# def ask_personalized_tutor(user_id, user_prefs, question):
#     """
#     Uses the personalized LLM model to generate a response.
#     """
#     user_model = generate_personalized_model(user_id, user_prefs)

#     # Generate response
#     response = user_model.prompt(question)
#     return response



import torch
from gguf import GGUFModel
from transformers import AutoTokenizer, AutoModelForCausalLM



# tokenizer = AutoTokenizer.from_pretrained("deepseek-ai/DeepSeek-R1-Distill-Llama-8B")
# model = AutoModelForCausalLM.from_pretrained("deepseek-ai/DeepSeek-R1-Distill-Llama-8B")

# Path to your locally downloaded DeepSeek model
MODEL_PATH = r'c:\Users\Hughe\.lmstudio\models\lmstudio-community\DeepSeek-R1-Distill-Llama-8B-GGUF'

# Load tokenizer and model from local storage
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
model = AutoModelForCausalLM.from_pretrained(MODEL_PATH, torch_dtype=torch.float16, device_map="auto", gguf_filename=MODEL_PATH)
# model = GGUFModel.from_pretrained(MODEL_PATH)
# def generate_response(prompt):
#     """Generates AI responses using locally stored DeepSeek model."""
#     inputs = tokenizer(prompt, return_tensors="pt").to("cuda" if torch.cuda.is_available() else "cpu")
#     outputs = model.generate(**inputs, max_new_tokens=200)
#     return tokenizer.decode(outputs[0], skip_special_tokens=True)

# if __name__ == '__main__':
#     question = "What is the importance of adaptive learning?"
#     response =generate_response(question)
#     print(response)
class AITutor:
    def __init__(self, model_path, tokenizer_name="bert-base-uncased"):
        """Initialize the AI Tutor with a reasoning model."""
        self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_path, torch_dtype=torch.float16, device_map="auto"
        )

    def analyze_performance(self, quiz_results, assignment_results):
        """
        Analyze quiz and assignment results to identify areas of improvement.
        """
        focus_areas = []
        for topic, score in quiz_results.items():
            if score < 70:  # Example threshold for low performance
                focus_areas.append(topic)

        for topic, feedback in assignment_results.items():
            if "needs improvement" in feedback.lower():
                focus_areas.append(topic)

        return list(set(focus_areas))  # Remove duplicates

    def generate_study_plan(self, focus_areas):
        """
        Generate a personalized study plan based on focus areas.
        """
        prompt = (
            "You are an AI tutor. Based on the following focus areas, "
            "generate a personalized study plan with actionable steps:\n"
            f"{', '.join(focus_areas)}"
        )
        inputs = self.tokenizer(prompt, return_tensors="pt").to(
            "cuda" if torch.cuda.is_available() else "cpu"
        )
        outputs = self.model.generate(**inputs, max_new_tokens=300)
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)

    def tutor(self, quiz_results, assignment_results, question):
        """
        Provide tutoring by analyzing performance and answering questions.
        """
        focus_areas = self.analyze_performance(quiz_results, assignment_results)
        study_plan = self.generate_study_plan(focus_areas)

        # Answer the student's question
        inputs = self.tokenizer(question, return_tensors="pt").to(
            "cuda" if torch.cuda.is_available() else "cpu"
        )
        outputs = self.model.generate(**inputs, max_new_tokens=200)
        answer = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        return {"study_plan": study_plan, "answer": answer}


if __name__ == '__main__':
    # Example quiz and assignment results
    quiz_results = {"Math": 65, "Science": 80, "History": 55}
    assignment_results = {"Math": "Needs improvement", "History": "Good effort"}

    # Initialize the AI Tutor
    ai_tutor = AITutor(MODEL_PATH)

    # Generate tutoring suggestions
    question = "Can you explain the Pythagorean theorem?"
    tutoring_response = ai_tutor.tutor(quiz_results, assignment_results, question)

    print("Study Plan:")
    print(tutoring_response["study_plan"])
    print("\nAnswer to Question:")
    print(tutoring_response["answer"])