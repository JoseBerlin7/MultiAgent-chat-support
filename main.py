''' Starting the FastAPI app, handles incoming cjhat post requests, coordinates the agent workflow
Userquery -> logging -> Intent classifictaion -> routing -> response-> notify (on ticket creation) -> logging 
'''
from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel as Basemodel
from agents.routing_agent import Router
import database.db_utils as db_utils
from utils.logger import message_logger
from database.schemas import DB_schemas

app = FastAPI()

# To create the DB with few dummy data(first time only)
db_utils.create_tables()

# To clear all the logs
# DB_schemas().delete_all('convo_log.db', 'conversations')
# DB_schemas().delete_all('customer_tickets.db', 'tickets')
# print("clear")

class ChatRequest(Basemodel):
    phone: str
    message: str


class ChatResponse(Basemodel):
    agent: str
    response: str

async def log_message(customer_id, sender, message, agent):
    logg= message_logger()
    await logg.log_message(customer_id=customer_id,sender=sender, message=message, agent=agent)

@app.post("/chat", response_model=ChatResponse)
async def handle_chat(req: ChatRequest, bg_tasks: BackgroundTasks):
    
    # selecting specific customer_id
    # customer_id = 4
    
    user_data = DB_schemas().get_customer_id(phone=req.phone)
    customer_id = user_data['customer_id']

    bg_tasks.add_task(log_message, customer_id,"user",req.message, "")
    response, agent_name = Router().route(req.message, customer_id)
    bg_tasks.add_task(log_message, customer_id,"assistant",response,agent_name)
    return ChatResponse(response=response, agent= agent_name)
