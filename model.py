import whisper
from pydub import AudioSegment
import io
import numpy as np
import streamlit as st
import noisereduce as nr
from scipy.signal import butter, lfilter

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


def reduce_noise(waveform, sample_rate):
    noise_profile = waveform[:sample_rate]
    return nr.reduce_noise(y=waveform, sr=sample_rate, y_noise=noise_profile)


def band_pass_filter_multilingual(waveform, sample_rate, lowcut=200, highcut=4000):
    nyquist = 0.5 * sample_rate
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(1, [low, high], btype="band")
    return lfilter(b, a, waveform)


def trim_silence_waveform(waveform, threshold=0.01):
    """
    Trims silence from a waveform based on amplitude.
    
    Args:
        waveform (np.ndarray): Input waveform.
        sample_rate (int): Sampling rate of the audio.
        threshold (float): Amplitude threshold for silence.
    
    Returns:
        np.ndarray: Trimmed waveform.
    """
    # Find non-silent indices
    non_silent_indices = np.where(np.abs(waveform) > threshold)[0]
    if len(non_silent_indices) == 0:
        return waveform  # Return original waveform if all is silent
    
    start, end = non_silent_indices[0], non_silent_indices[-1] + 1
    return waveform[start:end]

def pass_audio_pipeline(audio_file):
    waveform, sample_rate = convertAudioFileToWaveForm(audio_file)
    denoised_waveform = reduce_noise(waveform, sample_rate)
    filtered_waveform = band_pass_filter_multilingual(denoised_waveform, sample_rate)
    trimmed_waveform = trim_silence_waveform(filtered_waveform)
    
    return np.array(trimmed_waveform, dtype=np.float32)
    