import whisper

def transcribeVoiceContentToText(pathToAudio):
    model = whisper.load_model("base")
    result = model.transcribe(pathToAudio)
    return result["text"].strip()
