from fastapi import FastAPI
import os

# This is the "app" that Uvicorn is looking for in your Procfile!
app = FastAPI()

@app.get("/")
def home():
    return {"status": "Online", "message": "Colour Bot is running successfully on Railway!"}

# --- PUT YOUR BOT CODE BELOW THIS LINE ---
# If you are making a Telegram or Discord bot, you can initialize it down here.
