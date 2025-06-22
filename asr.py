import requests
import base64
import json
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("BHASHINI_API_KEY")

url = "https://dhruva-api.bhashini.gov.in/services/inference/pipeline"

with open("audio_hi.wav", "rb") as audio_file:
    audio_base64 = base64.b64encode(audio_file.read()).decode("utf-8")

payload = {
    "pipelineTasks": [
        {
            "taskType": "asr",
            "config": {
                "language": {
                    "sourceLanguage": "en"
                },
                "audioFormat": "wav",          
                "samplingRate": 16000
            }
        }
    ],
    "inputData": {
        "audio": [
            {
                "audioContent": audio_base64
            }
        ]
    }
}
headers = {
    "Authorization": API_KEY,
    "Content-Type": "application/json"
}

response = requests.post(url, headers=headers, json=payload)

print(f"Status Code: {response.status_code}")
try:
    print("✅ ASR Output:")
    print(response.json())
except Exception as e:
    print("❌ Failed to parse JSON:", e)
    print("Raw Response Text:")
    print(response.text)
