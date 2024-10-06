import openai
import config.config as cfg
from typing import List

openai.api_key = cfg.OPENAI_API_KEY

def get_text_embedding(text: str) -> List[float]:
    response = openai.Embedding.create(input=text, model="text-embedding-ada-002")
    return response['data'][0]['embedding']
