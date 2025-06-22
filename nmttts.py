import requests
import base64
import json
from dotenv import load_dotenv
import os

# Load API key
load_dotenv()
API_KEY = os.getenv("BHASHINI_API_KEY")

# 📝 INPUT
SOURCE_TEXT = "मैं हूँ प्रियांशु और मैं भाषिणी एपीआई टेस्ट कर रहा हूँ।"
SOURCE_LANGUAGE = "hi"  # Input language
TARGET_LANGUAGE = "en"  # Translated + TTS output language

# Optional service IDs
NMT_SERVICE_ID = ""
TTS_SERVICE_ID = ""

# Pipeline payload
payload = {
    "pipelineTasks": [
        {
            "taskType": "translation",
            "config": {
                "language": {
                    "sourceLanguage": SOURCE_LANGUAGE,
                    "targetLanguage": TARGET_LANGUAGE
                },
                "serviceId": NMT_SERVICE_ID
            }
        },
        {
            "taskType": "tts",
            "config": {
                "language": {
                    "sourceLanguage": TARGET_LANGUAGE
                },
                "serviceId": TTS_SERVICE_ID,
                "gender": "female",
                "samplingRate": 8000
            }
        }
    ],
    "inputData": {
        "input": [
            {
                "source": SOURCE_TEXT
            }
        ]
    }
}

# Send request
headers = {
    "Authorization": API_KEY,
    "Content-Type": "application/json"
}

response = requests.post(
    "https://dhruva-api.bhashini.gov.in/services/inference/pipeline",
    headers=headers,
    json=payload
)

# Process response
print(f"Status Code: {response.status_code}")
try:
    result = response.json()
    print("✅ Full Pipeline Output:")
    print(json.dumps(result, indent=2, ensure_ascii=False))

    # Extract translated text
    for task in result.get("pipelineResponse", []):
        if task["taskType"] == "translation":
            translated = task["output"][0]["target"]
            print("\n🌐 Translated Text:", translated)

    # Extract TTS audio and save
    for task in result.get("pipelineResponse", []):
        if task["taskType"] == "tts":
            audio_base64 = task["audio"][0]["audioContent"]
            with open("nmt_tts_output.wav", "wb") as f:
                f.write(base64.b64decode(audio_base64))
            print("🔊 Saved spoken audio as 'nmt_tts_output.wav'")

except Exception as e:
    print("❌ Error parsing response:", e)
    print("Raw response:", response.text)
