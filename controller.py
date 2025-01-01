import fastapi
from fastapi import UploadFile, File
from model import transcribeVoiceContentToText
import uvicorn
import os

app = fastapi.FastAPI()

@app.post("/audio")
async def makeTranscription(file: UploadFile = File( ... )):
    if file.content_type not in ["audio/mpeg", "audio/mp4", "audio/mpeg", "audio/mpga", "audio/m4a", "audio/wav", "audio/webm"]:
        return {"error": "Invalid file type"}
    
    filePath = f"./.cache/{file.filename}"
    
    with open(filePath, "wb") as audio_file:
        content = await file.read()
        audio_file.write(content)
        
    result = transcribeVoiceContentToText(filePath)
    
    os.remove(filePath)
    
    return {"transcription": result}

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)