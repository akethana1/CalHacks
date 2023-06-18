from hume import HumeBatchClient
from hume.models.config import LanguageConfig
from itertools import islice
import requests

def get_job_id():
    url = "https://api.hume.ai/v0/batch/jobs"

    files = {"file": ("test.mp3", open("assets/test.mp3", "rb"), "audio/mpeg")}
    payload = {"json": "{}"}
    headers = {
        "accept": "application/json",
        "X-Hume-Api-Key": "yuETNz2lWdHFHtKNzdeVNsAhBOQCCzAHFsjeAKQkYOtlFqcS"
    }

    response = requests.post(url, data=payload, files=files, headers=headers)

    return response.json()["job_id"]

job_id = get_job_id()

def get_predictions():
    url = "https://api.hume.ai/v0/batch/jobs/" + job_id + "/predictions"

    headers = {
        "accept": "application/json; charset=utf-8",
        "X-Hume-Api-Key": "yuETNz2lWdHFHtKNzdeVNsAhBOQCCzAHFsjeAKQkYOtlFqcS"
    }

    response = requests.get(url, headers=headers)
    full_predictions = response.json()
    print(job_id)
    print(full_predictions)

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
                    
print(get_predictions())


            
                