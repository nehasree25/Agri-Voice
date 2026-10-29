
import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GNANI_API_KEY")
API_URL = "https://api.vachana.ai/api/v1/tts/inference"

if not API_KEY:
    raise ValueError("GNANI_API_KEY is missing from your .env file")

# A short Telugu sentence for the AgriVoice project
payload = {
    "text": "నమస్కారం రైతు సోదరా! మీ పంటను ఏ మార్కెట్లో అమ్మితే ఎక్కువ ఆదాయం వస్తుందో తెలుసుకుందాం. ముందుగా మీ పంట పేరు, పంట పరిమాణం, మీ గ్రామం వివరాలను తెలపండి. అప్పుడు మేము మీకు అత్యుత్తమ మార్కెట్ సూచనలను అందిస్తాము.",
    "model": "timbre-v3.0",
    "voice": "Lakshmi",
    "language": "te-IN",
    "speed": 1.0,
    "audio_config": {
        "encoding": "linear_pcm",
        "container": "wav",
        "num_channels": 1,
        "sample_rate": 48000,
        "sample_width": 2
    }
}

headers = {
    "X-API-Key-ID": API_KEY,
    "Content-Type": "application/json"
}

try:
    print("Sending text to Timbre TTS...")

    response = requests.post(
        API_URL,
        headers=headers,
        json=payload,
        timeout=(10, 90)
    )

    print("HTTP status:", response.status_code)

    if response.status_code == 200:
        with open("response.wav", "wb") as audio_file:
            audio_file.write(response.content)

        print("TTS successful!")
        print("Audio saved as response.wav")
        print("Audio size:", len(response.content), "bytes")
    else:
        print("Error response:", response.text[:1500])
        response.raise_for_status()

except requests.Timeout:
    print("The request timed out. Please try again later.")

except requests.RequestException as error:
    print("TTS request failed:", error)
