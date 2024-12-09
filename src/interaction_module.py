
import os
import openai
from text_to_speech import text_to_speech

# openai.api_key = os.getenv("OPENAI_API_KEY")

def handle_student_interaction(original_text, user_explanation, is_hint=True):
    """
    Handles interaction by comparing the student's explanation to the original text.
    :param original_text: The original text for comparison.
    :param user_explanation: The student's explanation.
    :param is_hint: If True, provide a hint; otherwise, provide detailed feedback.
    """
    feedback_prompt = (
        f"You are a teacher giving feedback to a student. The student was asked to explain the following text:\n"
        f"Original Text: {original_text}\n"
        f"The student gave this explanation: {user_explanation}\n"
    )
    
    if is_hint:
        feedback_prompt += "\nPlease give a short, constructive hint to help the student improve their answer without giving away the full explanation."
    else:
        feedback_prompt += "\nPlease provide a full and detailed explanation of why their answer is correct or incorrect. Offer suggestions to improve."

    feedback = generate_response(feedback_prompt)
    return {"feedback": feedback, "is_hint": is_hint}


def generate_response(feedback_prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": feedback_prompt},
            ]
        )
        return response['choices'][0]['message']['content']
    except openai.error.AuthenticationError as auth_err:
        print(f"Authentication Error: {auth_err}")
        raise
    except Exception as e:
        print(f"Error generating response: {e}")
        raise
