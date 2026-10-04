import os
import uvicorn
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"status": "Online", "message": "Colour Bot is running successfully on Railway!"}

# --- PUT YOUR BOT CODE BELOW THIS LINE ---


# This securely handles Railway's port assignment so you never get a crash
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
