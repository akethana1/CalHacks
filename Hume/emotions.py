from hume import HumeBatchClient
from hume.models.config import LanguageConfig
from itertools import islice

client = HumeBatchClient("ZH01lHke6S8yBjZAAr05j3elbMkM6UwPJlGH2cH0HzBaOeoa")
urls = ["https://storage.googleapis.com/hume-test-data/audio/ninth-century-laugh.mp3"]
config = LanguageConfig()
job = client.submit_job(urls, [config])

print(job)
print("Running...")

job.await_complete()

full_predictions = job.get_predictions()
for source in full_predictions:
    source_name = source["source"]["url"]
    predictions = source["results"]["predictions"]
    for prediction in predictions:
        language_predictions = prediction["models"]["language"]["grouped_predictions"]
        for language_prediction in language_predictions:
            for segment in language_prediction["predictions"][:1]:
                entries = segment["emotions"]
                emotions = {entry['name'] : entry['score'] for entry in entries}
                top_emotions = dict(sorted(emotions.items(), key=lambda x: x[1], reverse=True)[:5])
                print(top_emotions)

                