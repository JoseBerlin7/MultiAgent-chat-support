'''Purpose: to classify user input into an intent'''
import os
from dotenv import load_dotenv
from openai import AzureOpenAI

class IntentClassifier:

    def __init__(self):
        load_dotenv()
        self.endpoint =  os.getenv("ENDPOINT")
        self.deployment = os.getenv("DEPLOYMENT")
        self.openai_key = os.getenv("OPENAI_API_KEY")
        self.client = AzureOpenAI(
            azure_endpoint = self.endpoint,
            api_key = self.openai_key,
            api_version = "2025-01-01-preview"
        )

    def get_prompt(self, message):
        # Prompt with few-shot 
        chat_prompt = [
                {
                    "role": "system",
                    "content": [
                        {
                            "type": "text",
                            "text": '''You are an intent classifier for eSIM Mobile Reach Out, a company providing 
                            eSIM services to customers. Your goal is to classify the user’s request into exactly one 
                            of the following intents:\n\nAccount: Requests related to user account management such as profile updates, 
                            billing issues, password reset, account settings, or account access problems.\n\n
                            FAQ: General informational questions covering common topics about eSIM activation, usage, pricing, 
                            coverage, connectivity, or policies normally answered by FAQs.\n\nTicket: Requests involving support 
                            tickets, customer complaints, troubleshooting, or technical help which would require a support agent ticket.
                            \n\nConnectSupport: Requests or expressions by users explicitly asking to connect with a live person or agent 
                            directly for assistance.\n\nUnknown: Requests that do not clearly fit any of the above categories or are 
                            ambiguous.\n\nGiven the user request below, respond with ONLY one intent label (Account, Ticket, 
                            FAQ, ConnectSupport, or Unknown). Do NOT provide any explanation.'''
                        }
                    ]
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "What is my current balance?"
                        }
                    ]
                },
                {
                    "role": "assistant",
                    "content": [
                        {
                            "type": "text",
                            "text": "Account"
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
                }]
        return chat_prompt
    
    def classify(self, message):
        messages = self.get_prompt(message)
        response = self.client.chat.completions.create(
            model=self.deployment,
            messages=messages,
            max_tokens=800,
            temperature=0.7,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None,
            stream=False

        )

        intent = response.choices[0].message.content.strip()
        return intent
        
    
print(IntentClassifier().classify(input()))
    