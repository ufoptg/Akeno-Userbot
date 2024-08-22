import os
import nest_asyncio

import uvicorn
from fastapi import FastAPI


app = FastAPI(
title="PyroThon",
version="1.0.0",
contact={
  "name": "Aᴋᴇɴᴏ",
  "url": "https://github.com/ufoptg/Akeno-Userbot/",
},
docs_url=None, redoc_url="/"
)


@app.get("/status")
def status():
    return {"message": "running"}

if name == "main":
    nest_asyncio.apply()
    uvicorn.run(app, host="0.0.0.0", port=7860)
