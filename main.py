''' Starts FastAPI app, handles incoming cjhat post requesrs, coordinates the agent workflow
Intent classifictaion -> routing -> response -> logging ->Notification
'''
from fastapi import FastAPI, Request
from pydantic import BaseModel as Basemodel
from agents.intent_classifier import IntentClassifier
from agents.routing_agent import Router
from database.db_utils import init_db

app = FastAPI()

init_db()


class ChatRequest(Basemodel):
    user_id: str
    message: str


class ChatResponse(Basemodel):
    intent: str
    agent: str
    response: str


@app.post("/chat", response_model=ChatResponse)
async def handle_chat(req: ChatRequest):
    intent = IntentClassifier().classify(req.message)
    agent_name, response = Router().route(intent, req.message, req.user_id)

    return ChatResponse(intent=intent, agent= agent_name, response=response)