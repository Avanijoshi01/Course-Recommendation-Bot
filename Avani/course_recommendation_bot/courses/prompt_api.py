# courses/prompt_api.py

import requests
from django.conf import settings

IBM_CLOUD_API_KEY = settings.WATSONX_API_KEY
WATSONX_URL = "https://us-south.ml.cloud.ibm.com/ml/v1/text/generation?version=2023-05-29"
WATSONX_PROJECT_ID = "8a115b86-559b-4d6c-bb17-6957e7e3672a"
MODEL_ID = "ibm/granite-3-8b-instruct"

def get_iam_token(api_key):
    url = "https://iam.cloud.ibm.com/identity/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
        "apikey": api_key
    }

    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        raise Exception("❌ Failed to get access token: " + response.text)

def get_course_recommendation(prompt_text, access_token):
    body = {
        "input": prompt_text,
        "parameters": {
            "decoding_method": "greedy",
            "max_new_tokens": 200,
            "min_new_tokens": 0,
            "repetition_penalty": 1
        },
        "model_id": MODEL_ID,
        "project_id": WATSONX_PROJECT_ID,
        "moderations": {
            "hap": {
                "input": {"enabled": True, "threshold": 0.5, "mask": {"remove_entity_value": True}},
                "output": {"enabled": True, "threshold": 0.5, "mask": {"remove_entity_value": True}}
            },
            "pii": {
                "input": {"enabled": True, "threshold": 0.5, "mask": {"remove_entity_value": True}},
                "output": {"enabled": True, "threshold": 0.5, "mask": {"remove_entity_value": True}}
            },
            "granite_guardian": {
                "input": {"threshold": 1}
            }
        }
    }

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.post(WATSONX_URL, headers=headers, json=body)

    if response.status_code != 200:
        raise Exception("❌ Non-200 response from watsonx.ai: " + str(response.text))

    return response.json()["results"][0]["generated_text"]

# === STEP 4: Manual Test Runner ===
if __name__ == "__main__":
    try:
        access_token = get_iam_token(IBM_CLOUD_API_KEY)

        sample_prompt = """
You are a helpful course recommendation assistant. Based on the user's interests and available courses, recommend the most suitable course. If no specific courses are provided, offer general guidance.

Input: User Interests: I want to learn about data analysis and programming.
Available Courses:
Course ID: DATA007, Title: SQL for Data Analysis, Description: Master SQL for querying and managing relational databases.
Course ID: PYTHON008, Title: Python Programming for Beginners, Description: Learn the basics of Python programming.
Output:
"""
        result = get_course_recommendation(sample_prompt, access_token)
        print("✅ Generated Recommendation:\n", result)

    except Exception as e:
        print("❌ Error:", e)
