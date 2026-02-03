import asyncio
import edge_tts
import sounddevice as sd
import soundfile as sf

VOICE = 'en-US-AriaNeural'
OUTPUT_FILE = "response.wav"

async def _speak(text):
    communicate = edge_tts.Communicate(text=text, voice=VOICE)
    await communicate.save(OUTPUT_FILE)

def speak(text):
    asyncio.run(_speak(text))

    data, samplerate = sf.read(OUTPUT_FILE)
    sd.play(data, samplerate)
    sd.wait()