from rest_framework.decorators import api_view
from rest_framework.response import Response
import openai, os
from dotenv import load_dotenv
from django.http import JsonResponse
from django.conf import settings
import uuid

from hume import HumeBatchClient
from hume.models.config import LanguageConfig
from itertools import islice
import requests
import time
import soundfile
from .ChatGPT.ai import getAIResponse
base_url = "https://api.assemblyai.com/v2"

headers = {
    "authorization": "34fcffda0aba42ae8b70a6b6909fcafc"
}
# import whisper
# from .Transformer.transformer import audio_to_text


# model = whisper.load_model("medium")
def get_predictions(fPath):
    
    def get_job_id():
      url = "https://api.hume.ai/v0/batch/jobs"

      files = {"file": ("test.mp3", open(fPath, "rb"), "audio/mpeg")}
      payload = {"json": "{}"}
      headers = {
          "accept": "application/json",
          "X-Hume-Api-Key": "yuETNz2lWdHFHtKNzdeVNsAhBOQCCzAHFsjeAKQkYOtlFqcS"
      }

      response = requests.post(url, data=payload, files=files, headers=headers)

      return response.json()["job_id"]
    
    job_id = get_job_id()
    url = "https://api.hume.ai/v0/batch/jobs/" + job_id + "/predictions"

    headers = {
        "accept": "application/json; charset=utf-8",
        "X-Hume-Api-Key": "yuETNz2lWdHFHtKNzdeVNsAhBOQCCzAHFsjeAKQkYOtlFqcS"
    }
    while True:
        response = requests.get(url, headers=headers)
        data = response.json()
        if 'status' in data and data['status'] == 400:
            time.sleep(1)  # Pause for 1 second before making the next request
            continue
        break
    full_predictions = response.json()
    #print(job_id)
    #print(full_predictions)

    for source in full_predictions:
        predictions = source["results"]["predictions"]
        for prediction in predictions:
            prosody_predictions = prediction["models"]["prosody"]["grouped_predictions"]
            for prosody_prediction in prosody_predictions:
                for segment in prosody_prediction["predictions"][:1]:
                    entries = segment["emotions"]
                    emotions = {entry['name'] : entry['score'] for entry in entries}
                    top_emotions = dict(sorted(emotions.items(), key=lambda x: x[1], reverse=True)[:5])
                    final_emotions = list(top_emotions.keys())
                    return final_emotions

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
        filename2 = 'hello2.mp3'
        file_path = os.path.join(audio_folder, filename)
        file_path2 = os.path.join(audio_folder, filename2)
        with open(file_path, 'wb') as destination:
            for chunk in audio_file.chunks():
                destination.write(chunk)

        ##written

        res = get_predictions(file_path)
        print(res)


        ########
        with open(file_path, "rb") as f:
            response = requests.post(base_url + "/upload",
                                    headers=headers,
                                    data=f)

        upload_url = response.json()["upload_url"]

        data = {
            "audio_url": upload_url # You can also use a URL to an audio or video file on the web
        }

        url = base_url + "/transcript"
        resp = requests.post(url, json=data, headers=headers)

        transcript_id = resp.json()['id']
        polling_endpoint = f"https://api.assemblyai.com/v2/transcript/{transcript_id}"

        while True:
            transcription_result = requests.get(polling_endpoint, headers=headers).json()

            if transcription_result['status'] == 'completed':
                break

            elif transcription_result['status'] == 'error':
                raise RuntimeError(f"Transcription failed: {transcription_result['error']}")

            else:
                time.sleep(3)

        userInputText = transcription_result["text"]

        res.append(transcription_result["text"])

        aiResponse = getAIResponse(userInputText)
        res.append(aiResponse)
        return JsonResponse({"response": res})

    return JsonResponse({'error': 'Invalid request.'}, status=400)