from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from backend.database import SessionLocal, Chat, init_db
from backend.llm_handlers import call_openai, call_gemini, call_llama
from datetime import datetime

# Initialize FastAPI app
app = FastAPI()

# Initialize database (Run once during setup)
init_db()

# Define a request model for chat input
class ChatRequest(BaseModel):
    prompt: str
    model: str
    session_id: int = None  # Optional session ID


@app.post("/chat")
def chat(request: ChatRequest):
    """
    Endpoint to handle chat requests.
    - Accepts a JSON payload with `prompt`, `model`, and optional `session_id`.
    """
    prompt = request.prompt
    model = request.model
    session_id = request.session_id

    # Validate the selected model
    if model not in ["openai", "gemini", "llama"]:
        raise HTTPException(status_code=400, detail="Unsupported model")

    # Call the appropriate LLM API
    if model == "openai":
        response = call_openai(prompt)
    elif model == "gemini":
        response = call_gemini(prompt)
    elif model == "llama":
        response = call_llama(prompt)

    # Generate a new session ID if none is provided
    if session_id is None:
        session_id = int(datetime.utcnow().timestamp())  # Use Unix timestamp as session ID

    # Save chat to the database
    db = SessionLocal()
    chat_entry = Chat(session_id=session_id, user_input=prompt, bot_response=response)
    db.add(chat_entry)
    db.commit()
    db.close()

    return {"response": response, "session_id": session_id}


@app.get("/chats")
def get_chats():
    """
    Endpoint to retrieve all past chat sessions with their full message history.
    """
    db = SessionLocal()
    chats = db.query(Chat).all()
    db.close()

    # Group chats by session ID
    sessions = {}
    for chat in chats:
        if chat.session_id not in sessions:
            sessions[chat.session_id] = {
                "session_id": chat.session_id,
                "messages": []
            }
        
        # Add the user input and bot response correctly
        sessions[chat.session_id]["messages"].append(
            {"role": "user", "text": chat.user_input}
        )
        sessions[chat.session_id]["messages"].append(
            {"role": "bot", "text": chat.bot_response}
        )

    return list(sessions.values())


@app.post("/start_session")
def start_session():
    """
    Endpoint to start a new chat session.
    Generates a new session ID and returns it.
    """
    session_id = int(datetime.utcnow().timestamp())  # Generate a unique session ID
    return {"session_id": session_id}
