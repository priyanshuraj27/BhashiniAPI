import requests
import base64
import json
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("BHASHINI_API_KEY")

url = "https://dhruva-api.bhashini.gov.in/services/inference/pipeline"

headers = {
    "Authorization": API_KEY,
    "Content-Type": "application/json"
}

payload = {
    "pipelineTasks": [
        {
            "taskType": "tts",
            "config": {
                "language": {
                    "sourceLanguage": "mr"
                },
                "serviceId": "",  # Optional: use a specific serviceId if available
                "gender": "female",
                "samplingRate": 8000
            }
        }
    ],
    "inputData": {
        "input": [
            {
                "source": "माझं नाव बब्या आहे आणि मी भाषावर्ष वापरतोय."
            }
        ]
    }
}

response = requests.post(url, headers=headers, json=payload)

print(f"Status Code: {response.status_code}")

try:
    data = response.json()
    audio_base64 = data["pipelineResponse"][0]["audio"][0]["audioContent"]

    with open("tts_marathi.wav", "wb") as f:
        f.write(base64.b64decode(audio_base64))

    print("✅ Saved Bhojpuri TTS to 'tts_marathi.wav'")
except Exception as e:
    print("❌ Failed to decode audio:", e)
    print("Response text:", response.text)
