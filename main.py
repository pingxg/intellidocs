import os
import json
from openai import OpenAI
import openai
import fitz
from pdf2image import convert_from_path
import base64
import pandas as pd
from dotenv import load_dotenv
import requests

# Load environment variables from a .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

class OpenAIClient:
    def __init__(self, api_key):
        """
        Initializes the OpenAI client with the provided API key.
        """
        self.client = OpenAI(api_key=api_key)

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
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": text},
                ],
            )
            return completion.choices[0].message
        except Exception as e:
            print(f"Error extracting data with Langchain: {e}")
            return None


def process_pdfs_in_folder(folder_path, output_file):
    """
    Processes all PDF files in a folder, extracts data, and saves it to an Excel file.
    """
    data = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            file_path = os.path.join(folder_path, filename)
            print(f"Processing file: {file_path}")

            # Extract text from PDF
            extracted_text = extract_text_from_pdf(file_path)

            if extracted_text.strip():
                print(f"Text successfully extracted from {file_path}")
                try:
                    extracted_data = extract_data_with_langchain(extracted_text)
                    json_data = json.loads(
                        extracted_data.content.strip("```json\n").strip("```")
                    )
                    data.append(json_data)
                except Exception as e:
                    print(f"Error processing extracted text: {e}")

            else:
                print(
                    f"Text extraction failed, switching to image extraction for {file_path}"
                )
                try:
                    images = convert_from_path(file_path)
                    for i, image in enumerate(images):
                        image_path = f"temp_image_{i}.jpg"
                        image.save(image_path, "JPEG")

                        encoded_image = encode_image(image_path)

                        extracted_data = extract_data_from_image(encoded_image)
                        print(f"Extracted Data from page {i + 1}: {extracted_data}")

                        try:
                            extracted_json = json.loads(
                                extracted_data["choices"][0]["message"]["content"]
                                .strip("```json\n")
                                .strip("```")
                            )
                            data.append(extracted_json)
                        except Exception as e:
                            print(f"Error parsing GPT-4 response: {e}")

                        os.remove(image_path)

                except Exception as e:
                    print(f"Error processing {file_path}: {e}")

    if data:
        df = pd.DataFrame(data)
        df.to_excel(output_file, index=False)
        print(f"Data successfully saved to {output_file}")
    else:
        print("No data to save.")

if __name__ == "__main__":
    api_key = os.getenv("OPENAI_API_KEY")
    openai_client = OpenAIClient(api_key)
    folder_path = "invoices"
    output_file = "output.xlsx"
    process_pdfs_in_folder(folder_path, output_file)