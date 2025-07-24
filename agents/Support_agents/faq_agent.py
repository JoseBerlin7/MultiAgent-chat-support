'''Purpose: Responds to FAQs with a model trained on FAQ data.'''

class FAQAgent:
    def respond(self, message)->str:
        return f"'{message}' been recieved"
