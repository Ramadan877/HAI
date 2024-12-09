
import spacy
import openai

nlp = spacy.load("en_core_web_sm")  

def extract_keywords_from_file(file_path):
    with open(file_path, 'r') as file:
        text = file.read()

    doc = nlp(text)
    keywords = [token.text for token in doc if token.pos_ in ['NOUN', 'PROPN']]
    return keywords

def generate_feedback_prompt(original_text, user_explanation, is_hint):
    if is_hint:
        return f"""
        Original Text: {original_text}
        User Explanation: {user_explanation}
        Provide a short, constructive hint to help the user refine their explanation.
        """
    else:
        return f"""
        Original Text: {original_text}
        User Explanation: {user_explanation}
        Provide detailed feedback on the explanation.
        """

def generate_follow_up_question(student_text, keywords):
    prompt = f"""
    Based on the student's explanation: "{student_text}" and the keywords: {keywords},
    generate a follow-up question to deepen their understanding.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
        )
        return response['choices'][0]['message']['content']
    except openai.error.OpenAIError as e:
        print(f"Error generating follow-up question: {e}")
        return "Could not generate follow-up question."
