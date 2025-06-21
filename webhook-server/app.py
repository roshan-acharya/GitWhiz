import requests

payload = {
    "action": "opened",
    "issue": {
        "number": 42,
        "title": "Dummy Issue for Testing",
        "body": "This is a dummy issue webhook payload.",
        "user": {
            "login": "test-user"
        }
    },
    "repository": {
        "name": "example-repo",
        "owner": {
            "login": "example-owner"
        }
    },
    "installation": {
        "id": 12345678
    }
}

headers = {
    "Content-Type": "application/json",
    "X-GitHub-Event": "issues",
    "X-GitHub-Delivery": "dummy-delivery-id"
}

response = requests.post("https://gitwhiz-1.onrender.com/webhook", json=payload, headers=headers)
print("Status:", response.status_code)
print("Response:", response.text)
