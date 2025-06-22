import requests
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
            "taskType": "translation",
            "config": {
                "language": {
                    "sourceLanguage": "hi",
                    "targetLanguage": "en"
                }
            }
        }
    ],
    "inputData": {
        "input": [
            {
                "source": "नमस्ते दुनिया"
            }
        ]
    }
}

response = requests.post(url, headers=headers, json=payload)

print(f"Status Code: {response.status_code}")
try:
    print("✅ Translation Output:")
    print(response.json())
except Exception as e:
    print("❌ Failed to parse JSON:", e)
    print("Raw Response Text:")
    print(response.text)
