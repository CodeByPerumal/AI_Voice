import sounddevice as sd
import soundfile as sf
import numpy as np
import queue
import time 
from faster_whisper import WhisperModel

SAMPLE_RATE = 16000
BLOCK_SIZE = 1024
# SILENCE_THRESHOLD = 0.01
SILENCE_THRESHOLD = 0.003
# MAX_SILENCE_SEC = 1.2
MAX_SILENCE_SEC = 2.0

q = queue.Queue()
model = WhisperModel("small", device = "cpu", compute_type = "int8")

def audio_callback(indata, frames,time_info, status):
    q.put(indata.copy())

def record_once(filename = "input.wav"):
    audio = []
    silence_start = None
    start_time = time.time()
    MIN_RECORD_SEC = 0.8

    print("\nSpeak Now: ")

    with sd.InputStream(
        samplerate = SAMPLE_RATE,
        channels = 1,
        blocksize = BLOCK_SIZE,
        callback = audio_callback,
        dtype = "float32"
    ):
        while True:
            block = q.get()
            audio.append(block)
            rms = np.sqrt(np.mean(block**2))

            if rms < SILENCE_THRESHOLD:
                if silence_start is None:
                    silence_start = time.time()
                elif (
                    time.time() - silence_start > MAX_SILENCE_SEC and time.time() - start_time > MIN_RECORD_SEC
                ):
                    break
            else:
                silence_start = None

    audio_np = np.concatenate(audio, axis = 0)
    sf.write(filename, audio_np, SAMPLE_RATE)
    print("Recording Stopped...")


def transcribe(filename="input.wav"):
    segments, _ = model.transcribe(filename, language= 'en')
    return ' '.join(seg.text for seg in segments).strip()