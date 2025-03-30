import whisper
from datetime import datetime

# model = whisper.load_model("base.en")
# model = whisper.load_model("medium.en")
model = whisper.load_model("turbo")

start_time = datetime.now()
# load audio and pad/trim it to fit 30 seconds
audio = whisper.load_audio("3b9279b6-9515-4666-bd9e-f831cd61c8c3.wav")
# audio = whisper.load_audio("recording.wav")
audio = whisper.pad_or_trim(audio)
print("✅ Audio loaded!")

# make log-Mel spectrogram and move to the same device as the model
mel = whisper.log_mel_spectrogram(audio, n_mels=model.dims.n_mels).to(model.device)

# detect the spoken language
# _, probs = model.detect_language(mel)
# print(f"Detected language: {max(probs, key=probs.get)}")

# decode the audio
options = whisper.DecodingOptions(language='en')
result = whisper.decode(model, mel, options)
end_time = datetime.now()
print("✅ Audio transcribed!")

# Time taken
print(start_time, end_time)
print(end_time - start_time)

# print the recognized text
print(result.text)
