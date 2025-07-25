# MultiAgent-chat-support
This repository contains modular, AI-based customer support backend using python, fastapi, Azure Openai, Language embedding.
This project simulates a multi-agent architecture for handling user queries (FAQs, raising tickes, account-info).

##Features
1. Intent Classification using prompt engineerings and few-shot prompting
2. Agent Routing to find the suitable agent for the task
3. Ticket Agent to raise mock tickets
4. Account Agent to respond to account related queries
5. FAQ Agent using similarity search over CSV data embedding
6. Notify Agent to send emails using sendgrid

## Project Structure


## Instructions to run
1. switch to directory

        cd MultiAgent-chat-support

2. Install dependencies

        pip install -r requirements.txt

3. Set the env
Create .env files with the following

        MODEL_NAME = "gpt-4o"
        OPENAI_DEPLOYMENT = "gpt-4o"
        ENDPOINT = ""
        API_KEY = ""
        EMBEDDING_MODEL_NAME = "text-embedding-3-small"
        EMBEDDING_DEPLOYMENT = ""
        SENDGRID_API_KEY = ""

4. Run the app

        uvicorn main:app --reload

5. Then visit

        http://127.0.0.1:8000/docs

6. Select try it youserlf

Example request:

        {
          "user_id": "+12345678901",
          "message": "How do I activate my sim card?"
        }

Sample response:

        {
          "agent": "FAQAgent",
          "response": "Download the Cogniwide app, scan the QR code provided, and follow the on-screen instructions."
        }


