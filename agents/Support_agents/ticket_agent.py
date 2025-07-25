'''Purpose: Ticket creation, returns a ticket ID and logs the details in the database.'''
from agents.answer_handling import generate_answer
from database.schemas import DB_schemas
# from agents.Support_agents.notify_agent import send_mail

class TicketAgent:
    def get_prompt(message):
        chat_prompt = [
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": "You are an agent for eSIM Mobile Reach Out, a company providing eSIM services to customers. Your task is to:\n\nRead and understand the customer's message carefully.\n\nConfirm with the customer if they want to create a support ticket regarding their issue or request.\n\nIf the customer confirms, ask for issue description.\n\nCreate a support ticket with the collected information.\n\nRespond to the customer positively, reassuring them that their ticket has been created and that the support team will reach out soon.\n\nAlways be polite, clear, and helpful.\n"
                    }
                ]
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Customer data: {\"name\": \"Eve Brown\",  \"email\": \"eve.brown@bla.com\",  \"phone\": \"+12345678905\",  \"account_stat\": \"active\",  \"current_plan\": \"postpaid\",  \"balance\": 15.2}\nCustomer: Hi, I'm having trouble activating my eSIM on my new phone."
                    }
                ]
            },
            {
                "role": "assistant",
                "content": [
                    {
                        "type": "text",
                        "text": "Thanks for reaching out! To assist you better, would you like me to create a support ticket for this eSIM activation issue?"
                    }
                ]
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "I am having trouble with topping up my sim card, I would like to create a ticket"
                    }
                ]
            },
            {
                "role": "assistant",
                "content": [
                    {
                        "type": "text",
                        "text": "Thank you for letting me know. Could you please provide a brief description of the issue you're facing while trying to top up your SIM card? This will help us create a detailed support ticket for you."
                    }
                ]
            }
        ]

        return chat_prompt
    
    def create_ticket(self, message, user_data):
        DB_schemas().add_ticket(message=message,customer_id=user_data['customer_id'],status="OPEN")
        # send_mail().send_email_via_sendgrid(to_emails=user_data['email'], subject="Ticket raised", text_content=message)
        return "I've successfully raised a ticket for you, you'll be recieving a email conformation regarding this ticket"

        
    def respond(self, message, user_data):
        prompted_message = self.get_prompt(message)
        return generate_answer.get_answer(prompted_message)
        
        