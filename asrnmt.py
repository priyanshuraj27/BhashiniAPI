import requests
import base64
import json
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("BHASHINI_API_KEY")

# Language setup
SOURCE_LANGUAGE = "en"
TARGET_LANGUAGE = "hi"
AUDIO_FILE_PATH = "audio_hi.wav"  

ASR_SERVICE_ID = ""
NMT_SERVICE_ID = ""

with open(AUDIO_FILE_PATH, "rb") as audio_file:
    audio_base64 = base64.b64encode(audio_file.read()).decode("utf-8")

payload = {
    "pipelineTasks": [
        {
            "taskType": "asr",
            "config": {
                "language": {
                    "sourceLanguage": SOURCE_LANGUAGE
                },
                "serviceId": ASR_SERVICE_ID,
                "audioFormat": "wav",
                "samplingRate": 16000
            }
        },
        {
            "taskType": "translation",
            "config": {
                "language": {
                    "sourceLanguage": SOURCE_LANGUAGE,
                    "targetLanguage": TARGET_LANGUAGE
                },
                "serviceId": NMT_SERVICE_ID
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

response = requests.post(
    "https://dhruva-api.bhashini.gov.in/services/inference/pipeline",
    headers=headers,
    json=payload
)

print(f"Status Code: {response.status_code}")
try:
    result = response.json()
    print("✅ Full Pipeline Output:")
    print(json.dumps(result, indent=2, ensure_ascii=False))

    for task in result.get("pipelineResponse", []):
        if task["taskType"] == "translation":
            translated = task["output"][0]["target"]
            print("\n📝 Translated Text (Hindi):", translated)
except Exception as e:
    print("❌ Error parsing response:", e)
    print("Raw Response Text:", response.text)
