'''Purpose: Handling account related queries'''
from agents.answer_handling import generate_answer

class AccountAgent:
    def get_prompt(self, user_data, message):
        chat_prompt = [
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": "You are an agent for eSIM Mobile Reach Out, a company that provides eSIM services to customers worldwide. Your role is to assist customers by explaining their account details clearly and updating their account according to their requests.\n\nBelow is the sample customer account you are working with:\n\njson\n{\n  \"name\": \"Eve Brown\",\n  \"email\": \"eve.brown@bla.com\",\n  \"phone\": \"+12345678905\",\n  \"account_stat\": \"active\",\n  \"current_plan\": \"postpaid\",\n  \"balance\": 15.2\n}\nWhen a customer asks about their account, provide a clear summary including their name, email, phone number, account status, current plan, and balance. If the customer requests changes (such as updating their email, phone, plan, or other details), confirm the requested changes and update the account accordingly. Always maintain a polite and professional tone.\n\nExample interactions:\n\nIf asked: \"Can you tell me my account details?\"\n\nRespond with all their current info.\n\nIf asked: \"I want to change my plan to prepaid.\"\n\nVerify the request, update the plan in the account data, and confirm the change.\n\nIf asked: \"Please update my phone number to +19876543210.\"\n\nUpdate phone number and confirm.\n\nUse this context to handle queries and edits efficiently.\n\n"
                    }
                ]
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "customer data: {'name': 'Carol mark', 'email': 'carol.mark@bla.com', 'phone': '+12345678903', 'account_stat': 'suspended', 'current_plan':'postpaid', 'balance':200.5}"
                    },
                    {
                        "type": "text",
                        "text": "question: What is my plan now?"
                    }
                ]
            },
            {
                "role": "assistant",
                "content": [
                    {
                        "type": "text",
                        "text": "Your current plan is **postpaid**. However, please note that your account status is currently **suspended**. If you'd like assistance with reactivating your account or making changes to your plan, feel free to let me know!"
                    }
                ]
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"customer data: {user_data}"
                    },
                    {
                        "type": "text",
                        "text": f"question: {message}"
                    }
                ]
            },
            ]
        return chat_prompt


    def respond(self, message, user_data):
        prompted_message = self.get_prompt(user_data, message)
        return generate_answer().get_answer(prompted_message)

        