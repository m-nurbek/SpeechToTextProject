import whisper
from pydub import AudioSegment
import io
import numpy as np

def transcribeVoiceContentToText(audio_file):
    audio_waveform, _ = convertAudioFileToWaveForm(audio_file)
    model = whisper.load_model("base")
    result = model.transcribe(audio_waveform)
    return result["text"].strip()


def convertAudioFileToWaveForm(audio_file):
    """
    Converts an audio file to a waveform numpy array.
    
    Args:
        audio_file (file-like object): The uploaded audio file.
    
    Returns:
        np.ndarray: The waveform as a numpy array.
        int: The sample rate of the audio.
    """
    audio = AudioSegment.from_file(io.BytesIO(audio_file.read()))
    
    # Convert audio to mono (1 channel) and sample rate to 16 kHz if needed
    audio = audio.set_frame_rate(16000).set_channels(1)
    
    # Get raw data and convert to numpy array
    samples = np.array(audio.get_array_of_samples(), dtype=np.float32)
    # Normalize waveform to range [-1.0, 1.0]
    samples /= np.iinfo(audio.array_type).max
    
    return samples, audio.frame_rate