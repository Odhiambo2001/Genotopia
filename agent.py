# Simulated Python Code to Respond to User Queries
import random

# Simulated responses based on the provided questions
def get_response(question):
    responses = {
        "Hi! Tell me something about George Mason NLP group!": "The George Mason NLP group focuses on research in natural language processing and machine learning, aiming to improve the way computers understand human language.",
        "Who is/are leading the group?": "The group is led by several faculty members, including prominent researchers in the field of NLP.",
        "Who is/are leading George Mason NLP group?": "The NLP group at George Mason University is led by distinguished faculty members with a strong background in natural language processing and computational linguistics.",
        "Find papers written by Ziyu Yao at George Mason University": "Ziyu Yao has authored numerous papers on topics related to natural language processing and machine learning. For the most up-to-date list, please refer to academic databases."
    }

    # Return a random response if the question is not recognized (not the case here, but for demonstration)
    return responses.get(question, "Sorry, I don't have information on that.")

# Example usage
questions = [
    "Hi! Tell me something about George Mason NLP group!",
    "Who is/are leading the group?",
    "Who is/are leading George Mason NLP group?",
    "Find papers written by Ziyu Yao at George Mason University"
]

for question in questions:
    print(f"User: {question}\nAgent: {get_response(question)}\n")

# Example observation
observation = """
The direct questions about the George Mason NLP group and its leadership provided straightforward responses. Combining questions or asking for specific academic contributions like papers reveals the limitations of static or predefined responses, highlighting the need for dynamic data access or tool augmentation to fetch real-time or updated information.
"""

print(observation)
