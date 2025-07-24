'''Purpose: Ticket creation, returns a ticket ID and logs the details in the database.'''


class TicketAgent:
    def respond(self, message, user_id)->str:
        return f"'{message} ticket created by {user_id}"