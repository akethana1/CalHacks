from transformers import Speech2TextProcessor, Speech2TextForConditionalGeneration
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

    return transcription