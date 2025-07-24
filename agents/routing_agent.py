'''Purpose: Routing agent for handling requests and directing them to appropriate agents.'''
from agents.Support_agents.faq_agent import FAQAgent
from agents.Support_agents.account_agent import AccountAgent
from agents.Support_agents.ticket_agent import TicketAgent

class Router:
    def route(self, intent:str, message: str, user_id: str):
        if intent == "FAQ":
            return FAQAgent().respond(message), "FAQ Agent"
        elif intent == "Account":
            return AccountAgent().respond(message, user_id), "Account Agent"
        elif intent == "Ticket":
            return TicketAgent().respond(message, user_id), "Ticket Agent"
        return "Sorry, we will assign you to a customer support", "Unknown"

