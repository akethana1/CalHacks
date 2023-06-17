from django.test import TestCase
import openai, os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_KEY", None)
# Create your tests here.
class testing(TestCase):
    def test1(self):
        chatbot_response = None
        if api_key is not None:
            openai.api_key = api_key
            userInput = ""
            prompt = ""

            res = openai.Completion.create(
                engine = "text-davinci-003",
                prompt=prompt,
                max_tokens = 256,
                temperature = 0.5
            )
            print(res)
        print("hello world")