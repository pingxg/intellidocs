from typing import List, Union
import requests
from openai import OpenAI
import config.config as cfg
from utils.logger import get_logger

logger = get_logger(__name__)

class OpenAIClient:
    def __init__(self):
        """
        Initializes the OpenAI client with the provided API key.
        """
        self.client = OpenAI(api_key=cfg.OPENAI_API_KEY)


    def extract_document_metadata(self, input_data: Union[str, List[str], bytes, List[bytes]]) -> Union[dict, None]:
        """
        Sends a request to OpenAI API to extract data from text or image input.
        """
        prompt = """
        All output should be in ENGLISH, ENGLISH, ENGLISH.
        You are given a document. Extract the following key metadata as plain JSON:
        below are the keys you must use in your output JSON:
        - [filename] (in English): please suggest a descriptive filename in ENGLISH based on the document content, all lowercase, no special characters, spaces replaced with underscores, no file extension
        - [description] (in English): please suggest a description/shot summary in ENGLISH based on the document content
        - [start_date]: the date of creation of the document you must find this date in the document content, please parse it into the format of yyyy.mm.dd
        - [end_date]: the date of expiration of the document or the validity period of the document, for example if it is a contract, find the end date of the contract, you must find this date in the document content, please parse it into the format of yyyy.mm.dd, if there are multiple dates, please use the most recent date, if there are no dates, please output an empty string
        
        and please output all other very important document metadata.

        Ensure all date information is parsed into the format yyyy.mm.dd.
        If there are duplicates in the result, only keep one; if there is only one result, it does not need to be a list.
        No need to output any additional characters.
        All output should be in ENGLISH, ENGLISH, ENGLISH.
        All the output text should not be encoded, print the text directly even if there are special characters in the text. Please handle the text encoding issue very carefully.
        If there are weired characters in the output, please remove them or replace them with the corresponding English characters. like $ to USD, € to EUR, £ to GBP, etc..
        """

        try:
            if isinstance(input_data, (str, list)):
                messages = [{"role": "system", "content": prompt}]
                if isinstance(input_data, str):
                    messages.append({"role": "user", "content": input_data})
                else:
                    for text in input_data:
                        messages.append({"role": "user", "content": text})

                completion = self.client.chat.completions.create(
                    model=cfg.LLM_MODEL,
                    messages=messages,
                    temperature=0.0,
                    response_format={ "type": "json_object" }
                )
                return completion.choices[0].message.content

            elif isinstance(input_data, (bytes, list)):
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {cfg.OPENAI_API_KEY}",
                }

                if isinstance(input_data, bytes):
                    input_data = [input_data]

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
                                    "image_url": {"url": f"data:image/jpeg;base64,{input_data}"},
                                },
                            ],
                        },
                    ],
                    "temperature": 0.0,
                    "response_format": { "type": "json_object" }
                }

                response = requests.post(
                    "https://api.openai.com/v1/chat/completions", headers=headers, json=payload
                )
                return response.json()

        except Exception as e:
            logger.error(f"Error extracting data: {e}")
            return None


    def get_text_embedding(self, text: str) -> List[float]:
        try:
            response = self.client.embeddings.create(input=text, model=cfg.EMBEDDING_MODEL)
            return response['data'][0]['embedding']
        except Exception as e:
            logger.error(f"Error getting text embedding: {e}")
            return None
