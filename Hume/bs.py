from hume import HumeBatchClient
from hume.models.config import ProsodyConfig
from itertools import islice

client = HumeBatchClient("ZH01lHke6S8yBjZAAr05j3elbMkM6UwPJlGH2cH0HzBaOeoa")

urls = ["https://storage.googleapis.com/hume-test-data/audio/ninth-century-laugh.mp3"]
prosody_config = ProsodyConfig()

# Use a webhook callback to get a POST notification to your API when the batch job has completed
callback_url = "https://mockbin.org/bin/08d1f920-801c-4de1-9622-8c7b39658009"
job = client.submit_job(urls, [prosody_config], callback_url=callback_url)

print("Running...", job)
job.await_complete()
print("Job completed with status: ", job.get_status())

full_predictions = job.get_predictions()
print(full_predictions)

                