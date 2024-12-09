
import openai
import os
from interaction_module import generate_response

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_feedback(original_text, explanation_text, is_hint=True):
    feedback_prompt = (
        f"You are a teacher providing feedback to a student. The student was asked to explain the following text:\n"
        f"Original Text: {original_text}\n"
        f"The student gave this explanation: {explanation_text}\n"
    )
    
    if is_hint:
        feedback_prompt += "\nPlease provide a short, helpful hint to guide the student towards the correct answer without revealing the full explanation."
    else:
        feedback_prompt += "\nPlease give full, constructive feedback, explaining where the student's answer is correct or incorrect, and providing suggestions for improvement."

    return generate_response(feedback_prompt)

