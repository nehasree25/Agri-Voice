
import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GNANI_API_KEY")
API_URL = "https://api.vachana.ai/stt/v3"

if not API_KEY:
    raise ValueError("GNANI_API_KEY is missing from .env")

for attempt in range(1, 3):
    print(f"Attempt {attempt}/2...")

    try:
        with open("test.wav", "rb") as audio:
            response = requests.post(
                API_URL,
                headers={"X-API-Key-ID": API_KEY},
                data={
                    "language_code": "te-IN",
                    "preferred_language": "te-IN",
                    "format": "transcribe",
                },
                files={
                    "audio_file": ("test.wav", audio, "audio/wav")
                },
                timeout=(10, 90),
            )

        print("HTTP status:", response.status_code)

        if response.status_code == 200:
            print("Response:", response.text)
            break

        print("Response:", response.text[:1000])

        if response.status_code not in (502, 503, 504):
            break

        if attempt < 2:
            print("Server timeout. Waiting 60 seconds...")
            time.sleep(60)

    except requests.Timeout:
        print("The request timed out. The server may be busy.")
        if attempt < 2:
            print("Waiting 60 seconds before retrying...")
            time.sleep(60)

    except requests.RequestException as error:
        print("Request error:", error)
        break
