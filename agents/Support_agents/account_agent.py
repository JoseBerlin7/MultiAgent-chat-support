'''Purpose: Handling account related queries'''

class AccountAgent:
    def respond(self, message, user_id)->str:
        return f"'{message} recived from {user_id}"