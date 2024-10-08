from langchain_huggingface.embeddings import HuggingFaceEmbeddings
import tiktoken
from dotenv import load_dotenv
import os
import config
import logging
from openai import OpenAI


logging.basicConfig(
    filename='app.log',
    filemode='a',
    level=logging.INFO,
    format='%(message)s',
    encoding='utf-8'
)


def calculate_tokens(text):
    tokens = config.encoding.encode(text)
    return len(tokens)


def generate_prompt_with_content(query, contents, max_tokens=12000):
    # NOTE: YOU WILL ALWAYS REPLY TO THE USER IN URDU LANGUAGE BY TRANSLATING THE GIVEN CONTENT IN URDU LANGUAGE.

    prompt_template = f"""
    You are an Islamic assistant. Your role is to provide precise answers to the user's query based solely on the content provided below. You must not create or infer new information; use only the information provided.

    Instructions:
    - Carefully read and understand the user's query.
    - Respond using only the content given below.
    - If the answer to the query is directly found in the content, provide that exact answer without modification.
    - Avoid adding any additional context or information outside of the provided content.
    - Maintain a respectful and accurate tone that aligns with Islamic teachings.
    - Answer the users QUERY using the CONTENTS text below.
    - Keep your answer ground in the facts of the CONTENTS.
    - If the CONTENTS does not contain the facts to answer the QUERY reply with the this same text as it is: "I DONT KNOW".
    - you are restricted to provide the meta data to the user of the answer.
    - always mention source name to the user.
    - always mention page number to the user.
    - always mention the title of the content to the user.

    Query: {query}

    Content 01:
    MetaData: {contents[0].metadata}
    Content: {contents[0].page_content}

    Content 02:
    MetaData: {contents[1].metadata}
    Content: {contents[1].page_content}

    Content 03:
    MetaData: {contents[2].metadata}
    Content: {contents[2].page_content}

    Content 04:
    MetaData: {contents[3].metadata}
    Content: {contents[3].page_content}
    """

    logging.info(f"Final Prompt: {prompt_template}")
    return prompt_template


def get_response(query):
    results = config.vectorstore.similarity_search(query=query, k=10)

    logging.info(f"Contents from PC: {results}")

    if not results:
        return "I Dont Know"

    final_prompt = generate_prompt_with_content(query, results)

    client = OpenAI(api_key=config.OPENAI_API_KEY)

    try:
        response = client.chat.completions.create(
            model=config.model_name,
            messages=[
                {
                    "role": "system",
                    "content": ("You are an Islamic assistant. Answer the user's query based only on the provided content. "
                                "If the answer is not present, respond with 'I don't know.'")
                },
                {
                    "role": "user",
                    "content": final_prompt
                }
            ]
        )
        final_response = response.choices[0].message.content
        return final_response

    except Exception as e:
        logging.error(f"Error calling OpenAI API: {e}")
        return "Something went wrong. Please try again later."


def get_response_elastic(query):
    results = config.elasticstore.similarity_search(query=query, k=10)

    logging.info(f"Contents from Elastic: {results}")

    if not results:
        return "I Dont Know"

    final_prompt = generate_prompt_with_content(query, results)

    client = OpenAI(api_key=config.OPENAI_API_KEY)

    try:
        response = client.chat.completions.create(
            model=config.model_name,
            messages=[
                {
                    "role": "system",
                    "content": ("You are an Islamic assistant. Answer the user's query based only on the provided content. "
                                "If the answer is not present, respond with 'I don't know.'")
                },
                {
                    "role": "user",
                    "content": final_prompt
                }
            ]
        )
        final_response = response.choices[0].message.content
        return final_response

    except Exception as e:
        logging.error(f"Error calling OpenAI API: {e}")
        return "Something went wrong. Please try again later."


def get_response_fined(query):
    client = OpenAI(api_key=config.OPENAI_API_KEY)

    try:
        response = client.chat.completions.create(
            model="ft:gpt-3.5-turbo-0125:dawat-e-islami:faizaneramazanv2:AAxpUq84",
            temperature=0.5,
            max_tokens=1000,
            messages=[
                {
                    "role": "system",
                    "content": ("You are a islamic assistant of dawat-e-islami and belongs to sunni hanafi maslak. you are strictly supposed to answer only from the dataset of dawat-e-islami. you are strictly not allowed to answer any question which is not related to dawat-e-islami or sunni hanafi school of thought. strictly answer with i dont know if someone asks any non religious, political, historical, etc question or any religious question which is not related to dawat-e-islami or sunni hanafi school of thought.")
                },
                {
                    "role": "user",
                    "content": query
                }
            ]
        )
        final_response = response.choices[0].message.content
        return final_response

    except Exception as e:
        logging.error(f"Error calling OpenAI API: {e}")
        return "Something went wrong. Please try again later."
