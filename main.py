from fastapi import FastAPI
from groq import Groq
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from dotenv import load_dotenv

load_dotenv()

class ChatRequest (BaseModel):
    message: str

SYSTEM_PROMPT = """ You are Turo, a teaching assistant built by Emyl.AI.
                    You do not just give answers - you guide users to think and understand first.
                    You explain the reasoning behind everything you say.
                    You treat every user as a normal person capable of learning anything.
                    Keep response simple, clear, and human.
                    """

conversation_history = []


client = Groq(api_key=os.getenv("GROQ_API_KEY"))

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def root():
    return FileResponse("static/index.html")

@app.get("/chat")
def chat():
    return {"message": "Emyl you are going to be great. Today is your day 1, you didnt comply at all at 4:30am workout but still you show at your self to do the first one thing that gonna happen. Keep continue and be happy that you had a progress today."}

@app.get("/chat2")
def chat2():
    return {"message": "This is my second door"}


@app.post("/ai-chat")
def ai_chat(request: ChatRequest):

    conversation_history.append({
        "role": "user",
        "parts": [{"text": request.message}]
    })

    # convert your existing history into Groq format
    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

    for item in conversation_history:
        role = item["role"]

        # Groq uses "assistant" instead of "model"
        if role == "assistant":
            role = "assistant"

        messages.append({
            "role": role,
            "content": item["parts"][0]["text"]
        })

    # CALL GROQ AI
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages
    )

    reply = response.choices[0].message.content

    conversation_history.append({
    "role": "assistant",
    "parts": [{"text": reply}]
})

    return {"reply": reply}