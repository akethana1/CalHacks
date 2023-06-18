from rest_framework.decorators import api_view
from rest_framework.response import Response
import openai, os
from dotenv import load_dotenv
from django.http import JsonResponse
from django.conf import settings
import uuid
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

@api_view(['POST'])
def upload_audio(request):
    if request.method == 'POST' and request.FILES.get('file'):
        audio_file = request.FILES['file']
        # Assuming you want to save the file in a specific directory
        base_dir = settings.BASE_DIR
        audio_folder = os.path.join(base_dir, 'mysite', "Audio")

        # Generate a unique filename for the audio file
        filename = 'hello1.mp3'

        file_path = os.path.join(audio_folder, filename)
        with open(file_path, 'wb') as destination:
            for chunk in audio_file.chunks():
                destination.write(chunk)

        return JsonResponse({'message': 'File uploaded successfully.'})

    return JsonResponse({'error': 'Invalid request.'}, status=400)