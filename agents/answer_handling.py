'''Purpose: to classify user input into an intent'''
import os
from dotenv import load_dotenv
from openai import AzureOpenAI

class generate_answer:

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
    
    def get_answer(self, prompted_message):
        try:
            response = self.client.chat.completions.create(
                model=self.deployment,
                messages=prompted_message,
                max_tokens=800,
                temperature=0.7,
                top_p=0.95,
                frequency_penalty=0,
                presence_penalty=0,
                stop=None,
                stream=False
            )

            answer = response.choices[0].message.content.strip()
        except Exception as e:
            return "Seems like I am having some trouble looking for your trouble would you like me to connect with the team?"
        return answer