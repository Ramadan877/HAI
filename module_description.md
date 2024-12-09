Here’s a step-by-step approach to implement this:
Text or Image Upload:

The student uploads either a text or a photo.
If it's an image, you’ll need to use Optical Character Recognition (OCR) to extract the text from the image.
Text Analysis:

Extract the key terms or keywords from the uploaded text (or extracted from the image).
We can use Natural Language Processing (NLP) to extract keywords (for instance, using libraries like spaCy or nltk).
Request Explanation from the Student:

The AI asks the student to explain the content of the uploaded text or image.
The AI would generate a prompt like, "Can you explain what this text/image is about?"
Analyze Student’s Explanation:

The student's explanation is then analyzed to identify which keywords they frequently mention.
You can use NLP techniques to extract keywords from the student's response.
Compare Keywords:

Compare the keywords from the student's explanation with the keywords from the original text/image.
If they match the important keywords from the original content, the AI proceeds to the next phase.
Follow-up Questions:

Based on the analysis of the student's response, the AI can ask short follow-up questions to verify the student’s understanding. For example, "Can you explain what [specific term or concept] means?" or "What do you understand by [another key term]?"
If the student struggles or misses important concepts, the AI can ask further clarifying questions until the student demonstrates a sufficient level of understanding.