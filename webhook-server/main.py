from fastapi import FastAPI, Request

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Welcome to the GitHub Webhook Server"}


@app.post("/webhook")
async def github_webhook(request: Request):
    payload = await request.json()
    issue = payload.get("issue")
    if issue:
        title = issue.get("title")
        body = issue.get("body")
        number = issue.get("number")
        print(f"New issue #{number}: {title}")
        print(f"Body: {body}")
    return {"status": "received"}
