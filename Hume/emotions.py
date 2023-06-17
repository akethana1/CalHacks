#from utilities import print_emotions

from hume import HumeBatchClient
from hume.models.config import ProsodyConfig
from pprint import pprint

client = HumeBatchClient("ZH01lHke6S8yBjZAAr05j3elbMkM6UwPJlGH2cH0HzBaOeoa")
urls = ["https://storage.googleapis.com/hume-test-data/audio/ninth-century-laugh.mp3"]
config = ProsodyConfig()
job = client.submit_job(urls, [config])

print(job)
print("Running...")

job.await_complete()
predictions = job.get_predictions()
print(predictions)

full_predictions = job.get_predictions()
for source in full_predictions:
    source_name = source["source"]["url"]
    predictions = source["results"]["predictions"]
    for prediction in predictions:
        print()
        print("Speech prosody")
        prosody_predictions = prediction["models"]["prosody"]["grouped_predictions"]
        for prosody_prediction in prosody_predictions:
            for segment in prosody_prediction["predictions"][:1]:
                print(segment["emotions"])
                print ("\n")