# GitWhiz

GitWhiz: GitHub Issue Auto-Triage & Notification System

## Overview

GitWhiz is a smart GitHub automation system that classifies newly created issues using AI, automatically applies the appropriate label, and sends notifications to a Discord channel. This system is powered by FastAPI, Kestra, and Google Gemini API to reduce manual triaging and enhance team responsiveness.

## Why GitWhiz?

Managing incoming GitHub issues can be overwhelming. GitWhiz reduces this burden by:

- Auto-classifying issues into "bug", "feature", "question", or "other"
- Auto-labeling issues
- Sending real-time Discord notifications
- Enhancing issue awareness and team collaboration

## Features

- ✅ FastAPI webhook server to receive GitHub issue events
- ✅ JWT-based GitHub App authentication
- ✅ Google Gemini-powered AI classification
- ✅ Kestra orchestration to process workflows
- ✅ Discord notifications with issue title, body, and label

## Tech Stack

- **FastAPI** - Webhook API server
- **Kestra** - Workflow orchestration
- **Google Gemini API** - AI classification
- **GitHub REST API** - Issue labeling
- **Discord Webhook** - Team notification
- **ngrok** - Local development tunneling
- **Python 3.9+**

## Prerequisites

- Python 3.9+
- Kestra CLI or Docker
- GitHub App (with private key)
- Google Gemini API Key
- Discord Webhook URL
- ngrok account

## Setup & Running Locally

1. **Clone the Repository**
    ```sh
    git clone https://github.com/yourusername/gitwhiz.git
    cd gitwhiz
    ```

2. **Create .env File**
    ```
    GITHUB_APP_ID=<your_github_app_id>
    GITHUB_PRIVATE_KEY_PATH=<absolute/path/to/private-key.pem>
    GEMINI_API_KEY=<your_gemini_api_key>
    DISCORD_WEBHOOK_URL=<your_discord_webhook_url>
    ```

3. **Create Virtual Environment & Install Dependencies**
    ```sh
    python -m venv venv
    # Windows:
    venv\Scripts\activate
    # macOS/Linux:
    source venv/bin/activate

    pip install -r requirements.txt
    ```

4. **Run FastAPI Webhook Server**
    ```sh
    uvicorn main:app --host 0.0.0.0 --port 8000
    ```

5. **Expose Server with ngrok**
    ```sh
    ngrok config add-authtoken <your-ngrok-authtoken>
    ngrok http 8000
    ```
    Use the generated URL in your GitHub webhook settings:
    ```
    https://<your-ngrok-id>.ngrok.io/webhook
    ```

6. **Run Kestra (via Docker or CLI)**
    ```sh
    kestra dev
    ```

7. **Deploy the Workflow in Kestra UI**
    - Open [http://localhost:8080](http://localhost:8080)
    - Upload `github-issue-triage-openai.yaml`
    - Deploy it under namespace `github`

## Workflow Inputs

- `issue_title`
- `issue_body`
- `issue_number`
- `repo_owner`
- `repo_name`
- `installation_token`

## Output & Notifications

- Automatically applies label (e.g., bug, feature)
- Posts to Discord via webhook:
  ```
  New GitHub Issue: Bug in Dashboard
  Label: bug
  "The dashboard crashes on reload..."
  ```
- Adds comment to GitHub issue:
  ```
  Thanks for opening this issue! The team has been notified. 🎉
  ```

## Example requirements.txt

```
fastapi
uvicorn
python-dotenv
PyJWT
requests
requests-toolbelt
kestra
```

## License

MIT

Built with ❤️ by Roshan Acharya
