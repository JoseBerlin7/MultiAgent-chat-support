'''Purpose: Responds to FAQs with a model trained on FAQ data.'''
import os
import pandas as pd
from openai import AzureOpenAI
from azure.core.credentials import AzureKeyCredential
import pickle
import torch
from typing import List
from dotenv import load_dotenv


class FAQAgent:
    def __init__(self, faq_path="FAQ_dataset/FAQ.csv", cache_path: str="FAQ_dataset/FAQ_embedding.pkl"):
        load_dotenv()
        self.endpoint = os.getenv("ENDPOINT")
        self.deployment = os.getenv("EMBEDDING_DEPLOYMENT")
        self.api_key = os.getenv("API_KEY")
        self.api_version = "2024-02-01"
        self.client = AzureOpenAI(
            api_version = self.api_version,
            azure_endpoint=self.endpoint,
            api_key = self.api_key
        )

        # Loading csv
        self.faq_path = faq_path
        self.cache_path = cache_path
        self.faq_df = pd.read_csv(faq_path)
        self.questions = self.faq_df["Question"].tolist()
        self.answers = self.faq_df['Answer'].tolist()

        self.embedding = self.load_embedd()

    # Creating the embedding
    def create_embedd(self, text):
        try:
            response = self.client.embeddings.create(
                input=[text],
                model=self.deployment
            )
            embedding = response.data[0].embedding
            return torch.tensor(embedding)
        except Exception as E:
            print(f"Embedding creation error: {E}")
            return torch.zeros(500)
    
    # Loading the embedding
    def load_embedd(self):
        if os.path.exists(self.cache_path):
            with open(self.cache_path,"rb") as f:
                return pickle.load(f)
        else:
            embedding = [self.create_embedd(ques) for ques in self.questions]
            with open(self.cache_path, "wb") as f:
                pickle.dump(embedding,f)
                print("Created embedding")
                return embedding
    
    # finding teh most relevant answe index to the user question
    def respond(self, user_message):
        user_embedding = self.create_embedd(user_message)
        similarities = [torch.nn.functional.cosine_similarity(user_embedding, embed, dim=0) 
                        for embed in self.embedding]
        best_idx = torch.argmax(torch.tensor(similarities))

        if similarities[best_idx]>0.60:
            return self.answers[best_idx]
        else:
            return "Unknown"