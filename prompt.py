import openai

openai.api_key = 'sk-vFey-R3pjo-cjOpALdmoP0pa7QhVDaVydpntGUQ2X9T3BlbkFJAeHyrr4PaFCXJoMm8qTuKzlr4M5QmaUDWgqJfZo2EA'

def test_openai():
    try:
        response = openai.Completion.create(
            engine="gpt-3.5-turbo-instruct",  # Or your preferred model
            prompt="Can you help me navigate within TAMUCC campus?",
            max_tokens=50
        )
        print(response.choices[0].text.strip())
    except openai.error.OpenAIError as e:
        print(f"OpenAI API Error: {str(e)}")
    except Exception as e:
        print(f"Unexpected Error: {str(e)}")

test_openai()