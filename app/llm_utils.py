import os
import joblib
import httpx
import requests
from dotenv import load_dotenv
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.chat_models import ChatOpenAI
from typing import Dict, Any

load_dotenv()

# model and functions for embeddings
# load embeddings cache file if it exits otherwise create one
try:
    embedding_cache = joblib.load("embedding_cache.joblib")
except FileNotFoundError:
    embedding_cache = {}

# wrapper function for caching the embeddings
def get_embeddings(text_list):
    embeddings = []
    for text in text_list:
        if text in embedding_cache:
            embeddings.append(embedding_cache[text])
        else:
            embedding = get_embedding_from_model(text)
            embedding_cache[text] = embedding
            embeddings.append(embedding)
    joblib.dump(embedding_cache, "embedding_cache.joblib")
    return embeddings

def get_embedding_from_model(text):
    embeddings_model = OpenAIEmbeddings(
        openai_api_base=os.environ['OPENAI_BASE'],
        openai_api_key=f"{os.environ['LLMFOUNDRY_TOKEN']}:{os.environ['PROJECT_NAME']}",
        model="text-embedding-3-small",
    )
    return embeddings_model.embed_documents([text])[0]

# Model for email extraction
def agent_and_email_model():
    return ChatOpenAI(
        openai_api_base=os.environ['OPENAI_BASE'],
        openai_api_key=f"{os.environ['LLMFOUNDRY_TOKEN']}:{os.environ['PROJECT_NAME']}",
        model="gpt-4o-mini",
)

# function using llm model for getting the card number extraction from image
def image_extraction_model_response(image_base64, image_type):
    response = requests.post(
        os.environ['IMAGE_LLM_BASE'],
        headers={"Authorization": f"Bearer {os.environ['LLMFOUNDRY_TOKEN']}:{os.environ['PROJECT_NAME']}"},
        json={
                "model": "prebuilt-document", # Or a more suitable model if available
                "document": f"data:image/{image_type};base64,{image_base64}",
                "prompt": """
                Extract the (15-16)digit credit/debit card number from the image. The numbers are mostly together, seperated from the rest. If no card number is found, return "None".  Return the output as a JSON string with the key "card_number".  For example:

                ```json
                {"card_number": "1234567890123456"}
                ```

                If no card number is found, return:

                ```json
                {"card_number": null}
                ```
                """,
            }
    )
    return response.json()