from rest_framework.decorators import api_view
from rest_framework.response import Response
import openai, os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_KEY", None)

@api_view(['POST'])
def postText(request):
  userText = request.data.get('text')

  if api_key is not None:
            openai.api_key = api_key
            res = openai.Completion.create(
                engine = "text-davinci-003",
                prompt = userText,
                max_tokens = 256,
                temperature = 0.5
            )
  return Response(res)