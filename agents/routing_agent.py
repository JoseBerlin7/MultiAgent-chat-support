'''Purpose: Routing agent for handling requests and directing them to appropriate agents.'''
from agents.Support_agents import AccountAgent, TicketAgent, FAQAgent
account_agent = AccountAgent()
ticket_agent = TicketAgent()
faq_agent = FAQAgent()

from agents.answer_handling import generate_answer
from database.schemas import DB_schemas
from utils.logger import message_logger
import os
from dotenv import load_dotenv
from openai import AzureOpenAI

class IntentClassifier:

    def __init__(self):
        load_dotenv()
        self.endpoint =  os.getenv("ENDPOINT")
        self.deployment = os.getenv("OPENAI_DEPLOYMENT")
        self.openai_key = os.getenv("API_KEY")
        self.client = AzureOpenAI(
            azure_endpoint = self.endpoint,
            api_key = self.openai_key,
            api_version = "2025-01-01-preview"
        )

    def get_convo_prompt(self):
        chat_prompt = [
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": "You are a friendly, helpful assistant for eSIM Mobile Reach Out, a company providing eSIM services and account support. Your goal is to keep the customer engaged in a natural, casual conversation while gently asking questions to better understand their needs related to eSIM activation, plans, balance, technical issues, or account information.\n\nStart with a warm, welcoming message.\n\nAsk open-ended questions specifically about eSIM services, plans, account, or technical issues.\n\nAvoid going off-topic; if the user asks about unrelated subjects, politely remind them that you specialize in eSIM services and ask how you can help with those.\n\nKeep responses brief, clear, empathetic, and focused on the customer’s needs regarding their eSIM and account.\n\nOnce you clearly understand the customer’s intent, suggest the next best step or action (for example, connecting with the right agent or providing info).\n\nIf you can’t understand the request after a couple of attempts, suggest contacting a human support representative.\n\nExample conversation starters:\n\n\"Hi! How can I assist you with your eSIM or account today?\"\n\n\"I’d love to help you with your eSIM plan or account. Could you please tell me more about what you need?\"\n\n\"Thanks for reaching out! Are you having any issues with your eSIM or account that I can help with?\"\n\n"
                    }
                ]
            }]
        return chat_prompt

    def get_func_prompt(self, message):
        # Prompt with few-shot 
        chat_prompt = [
                {
                    "role": "system",
                    "content": [
                        {
                            "type": "text",
                            "text": "You are a routing agent for eSIM Mobile Reach Out, a company providing eSIM services to customers. Your goal is to analyze the customer’s message, understand their intent, and determine the appropriate support agent to handle the request.You should return 'Unknown' until you figure out agents\n\nAvailable agents and when to route to them:\n\nAccountAgent(): Use when the customer asks about account-specific details such as balance, current plan, or account status.\n\nTicketAgent(): Use when the customer is experiencing an issue or requires support from a human agent, so a support ticket should be created.\n\nFAQAgent(): Use when the question is general or commonly asked FAQs, and can be answered by an automated knowledge base.\n\nYour task:\nGiven the customer message, customer ID, and any user data, decide which agent to call by selecting one of the following functions:\n\nAccountAgent().respond\n\nTicketAgent().create_ticket\n\nFAQAgent().respond\n\nOutput only the exact function call as a string without additional explanation."
                        }
                    ]
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "\nMessage: \"Can you tell me what’s my current eSIM data plan?\"\nCustomer ID: \"12345\"\nUser Data: { \"plan\": \"prepaid\", \"balance\": \"$15\" }"
                        }
                    ]
                },
                {
                    "role": "assistant",
                    "content": [
                        {
                            "type": "text",
                            "text": "\nAccountAgent().respond"
                        }
                    ]
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "How to activate my simcard"
                        }
                    ]
                },
                {
                    "role": "assistant",
                    "content": [
                        {
                            "type": "text",
                            "text": "FAQAgent().respond"
                        }
                    ]
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "how ro upgrade my plan"
                        }
                    ]
                },
                {
                    "role": "assistant",
                    "content": [
                        {
                            "type": "text",
                            "text": "FAQAgent().respond"
                        }
                    ]
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Hi how are you"
                        }
                    ]
                },
                {
                    "role": "assistant",
                    "content": [
                        {
                            "type": "text",
                            "text": "Unknown"
                        }
                    ]
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "I want to know my balance"
                        }
                    ]
                },
                {
                    "role": "assistant",
                    "content": [
                        {
                            "type": "text",
                            "text": "AccountAgent().respond"
                        }
                    ]
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"{message}"
                        }
                    ]
                }
            ]


        return chat_prompt

class Router(IntentClassifier):
        
    def get_history(self, customer_id, message):
        logg = message_logger()
        last_messages = logg.get_last_chat(customer_id, 5)
        if last_messages==None:
            return [].append({"role":'user', 'content': [{"type":"text", "text":message}]})
        history = [{"role":sender, "content": [{"type":"text", "text":message}]} for sender, message in last_messages]+[{"role":'user', 'content': [{"type":"text", "text":message}]}]
        return history

    def route(self, message, customer_id):
        target = generate_answer().get_answer(self.get_func_prompt(message))
        user_data = DB_schemas().get_customer_data(customer_id=customer_id)
        allowed_functions = {
        "AccountAgent().respond": lambda: AccountAgent().respond(user_data=user_data,message=message), #Done
        "TicketAgent().create_ticket": lambda: TicketAgent().create_ticket(message=message, user_data=user_data), #Done
        "FAQAgent().respond": lambda: FAQAgent().respond(message), #Done
        }
        chat_history =self.get_history(customer_id=customer_id, message=message)
        prompt = self.get_convo_prompt()
        conv_history = prompt.append(chat_history)

        func_key = None
        for key in allowed_functions.keys():
            if target.startswith(key):
                func_key = key
                break
        if func_key is None:
            response = generate_answer().get_answer(prompted_message=conv_history)
            return response, "Unknown"
        
        response = allowed_functions[func_key]()

        if response == "Unknown":
            response = "Seems like we're having some trouble fetching that information for you, would you like to talk to a agent?"
        return response, func_key