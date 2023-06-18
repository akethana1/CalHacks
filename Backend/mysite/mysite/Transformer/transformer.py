import torch
from transformers import Speech2TextProcessor, Speech2TextForConditionalGeneration
from datasets import load_dataset
import soundfile as sf

model = Speech2TextForConditionalGeneration.from_pretrained("facebook/s2t-small-librispeech-asr")
processor = Speech2TextProcessor.from_pretrained("facebook/s2t-small-librispeech-asr")

def audio_to_text(file_path):
    audio, sound_rate = sf.read(file_path)
    ds = load_dataset("hf-internal-testing/librispeech_asr_demo", "clean", split="validation")

    inputs = processor(ds[0]["audio"]["array"], sampling_rate=ds[0]["audio"]["sampling_rate"], return_tensors="pt")
    generated_ids = model.generate(inputs["input_features"], attention_mask=inputs["attention_mask"])

    transcription = processor.batch_decode(generated_ids, skip_special_tokens=True)
    return transcription

'''from transformers import Speech2TextProcessor, Speech2TextForConditionalGeneration
import soundfile as sf
import torch
#model
processor = Speech2TextProcessor.from_pretrained("facebook/s2t-small-librispeech-asr")
model = Speech2TextForConditionalGeneration.from_pretrained("facebook/s2t-small-librispeech-asr")
#audio_to_text model utilizing HuggingFace Speech2Text Model
def audio_to_text(file_path):
    audio, s_rate = sf.read(file_path)
    input = processor(audio, sampling_rate=s_rate, return_tensors="pt")
    with torch.no_grad():
        logits = model(input.input_features, attention_mask=input.attention_mask).logits
        predicted_ids = torch.argmax(logits, dim=-1)
        transcription = processor.batch_decode(predicted_ids)[0]

    return transcription'''

