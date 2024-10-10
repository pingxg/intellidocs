import config.config as cfg
from typing import List
from openai import OpenAI
import fitz
import base64
import pandas as pd
import requests


class OpenAIClient:
    def __init__(self):
        """
        Initializes the OpenAI client with the provided API key.
        """
        self.client = OpenAI(api_key=cfg.OPENAI_API_KEY)

    def extract_data_with_langchain(self, text):
        """
        Sends a request to OpenAI API to extract data from text.
        """
        prompt = """
        You are given the text of a machine installment payment invoice. Extract the following information as plain json, please remember to parse all the date information to the format of yyyy.mm.dd:
        - Manufacturer
        - Billing company
        - Invoice numbers
        - Contract numbers
        - Device names (if any)
        - Address related to the use of this device
        - Contract term
        - Current billing month
        - Total contract term
        - Net price every term

        If there are multiple contract numbers in an invoice, the exported file can have an additional row.
        If there are duplicates in the result, only keep one; if there is only one result, it does not need to be a list.
        no need to output any additonal characters
        all output in english
        """
        try:
            completion = self.client.chat.completions.create(
                model=cfg.LLM_MODEL,
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": text},
                ],
            )
            return completion.choices[0].message
        except Exception as e:
            print(f"Error extracting data with Langchain: {e}")
            return None


    def extract_data_from_image(image_base64):
        """
        Sends a request to OpenAI API to extract data from an image.
        """
        prompt = """
        You are given the image of a machine installment payment invoice. Extract the following information as plain json, and ensure to parse all date information into the format yyyy.mm.dd:
        - Manufacturer
        - Billing company
        - Invoice numbers
        - Contract numbers
        - Device names (if any)
        - Address related to the use of this device
        - Contract term
        - Current billing month
        - Total contract term
        - Net price every term

        If there are multiple contract numbers in an invoice, the exported file can have an additional row.
        If there are duplicates in the result, only keep one; if there is only one result, it does not need to be a list.
        no need to output any additonal characters
        all output in english
        """

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {openai.api_key}",
        }

        payload = {
            "model": cfg.LLM_MODEL,
            "messages": [
                {"role": "system", "content": prompt},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "What’s in this invoice image?"},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"},
                        },
                    ],
                },
            ],
        }

        response = requests.post(
            "https://api.openai.com/v1/chat/completions", headers=headers, json=payload
        )
        return response.json()


    def get_text_embedding(text: str) -> List[float]:
        response = openai.Embedding.create(input=text, model=cfg.EMBEDDING_MODEL)
        return response['data'][0]['embedding']