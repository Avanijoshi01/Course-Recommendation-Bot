import requests

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
        access_token = response.json()["access_token"]
        return access_token
    else:
        raise Exception("Failed to get access token: " + response.text)

# Example usage:
# token = get_iam_token("your_real_api_key_here")
if __name__ == "__main__":
    api_key = "0_W3cDUfarxX3RXK_HQCAg2nid7aYJ_IWQTc4CqPAJ8P"
    token = get_iam_token(api_key)
    print("Your Bearer Token:\n", token)
