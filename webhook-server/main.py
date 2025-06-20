from fastapi import FastAPI, Request
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("webhook")

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Welcome to the GitHub Webhook Server"}


@app.post("/webhook")
async def github_webhook(request: Request):
    payload = await request.json()
    issue = payload.get("issue")
    logger.info(f"Received webhook payload: {payload}")
    if issue:
        title = issue.get("title")
        body = issue.get("body")
        number = issue.get("number")
        print(f"New issue #{number}: {title}")
        print(f"Body: {body}")
    return {"status": "received"}
