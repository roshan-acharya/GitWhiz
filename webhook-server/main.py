from fastapi import FastAPI, Request
import logging
from dotenv import load_dotenv
from requests_toolbelt.multipart.encoder import MultipartEncoder
import os
import jwt
import time
import requests

# Load environment variables
load_dotenv()

# FastAPI app instance
app = FastAPI()

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("webhook")


@app.get("/")
async def read_root():
    return {"message": "Welcome to the GitHub Webhook Server"}


@app.post("/webhook")
async def github_webhook(request: Request):
    try:
        payload = await request.json()
        issue = payload.get("issue")
        logger.info(f"Received webhook payload: {payload}")

        if issue:
            title = issue.get("title")
            body = issue.get("body")
            number = issue.get("number")
            installation_id = payload.get("installation", {}).get("id")
            repo_owner = payload.get("repository", {}).get("owner", {}).get("login")
            repo_name = payload.get("repository", {}).get("name")

            installation_token = generate_installation_token(installation_id)
            print(installation_token)

            m = MultipartEncoder(
            fields={
                "issue_title": title or "",
                "issue_body": body or "",
                "issue_number": str(number) if number else "",
                "repo_owner": repo_owner or "",
                "repo_name": repo_name or "",
                "installation_token": installation_token
            }
        )

        kestra_url = "http://localhost:8080/api/v1/main/executions/github/github-issue-triage-openai"
        headers = {"Content-Type": m.content_type}

        kestra_response = requests.post(kestra_url, data=m, headers=headers)
        kestra_response.raise_for_status()

        return {"status": "triggered"}

    except Exception as e:
        logger.error("Error handling webhook", exc_info=True)
        return {"status": "error", "message": str(e)}


def generate_installation_token(installation_id: str) -> str:
    app_id = os.getenv("GITHUB_APP_ID")
    private_key_path = os.getenv("GITHUB_PRIVATE_KEY_PATH")

    if not app_id or not installation_id or not private_key_path:
        raise EnvironmentError("Missing GITHUB_APP_ID, installation_id, or GITHUB_PRIVATE_KEY_PATH")

    with open(private_key_path, "r") as f:
        private_key = f.read()

    now = int(time.time()) 
    payload = {
        "iat": now,
        "exp": now + 600,
        "iss": app_id
    }

    jwt_token = jwt.encode(payload, private_key, algorithm="RS256")

    # Check app authentication
    auth_headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Accept": "application/vnd.github+json"
    }
    check_response = requests.get("https://api.github.com/app", headers=auth_headers)
    if check_response.status_code != 200:
        raise Exception(f"App authentication failed: {check_response.text}")

    # Get installation token
    url = f"https://api.github.com/app/installations/{installation_id}/access_tokens"
    token_response = requests.post(url, headers=auth_headers)
    token_response.raise_for_status()

    token = token_response.json().get("token")
    if not token:
        raise Exception("Failed to retrieve installation token")

    return token


