import openai
import os
import numpy as np
from dotenv import load_dotenv
import tiktoken
from tqdm import tqdm

# Load environment variables from secrets.env file
load_dotenv("secrets.env")


class PromptingGPT:
    def __init__(self):
        # Load API key and organization from environment variables
        openai.api_key = os.getenv("OPENAI_API_KEY")  # Ensure your environment variables are loaded correctly

        # Initialize OpenAI client with API key
        self.client = openai.OpenAI(api_key=openai.api_key, organization=openai.organization)

        # Tokenizer for OpenAI models (specifically for text-embedding-ada-002)
        self.tokenizer = tiktoken.encoding_for_model("text-embedding-3-small")

    ClientOpenAi = openai.OpenAI(
        api_key=openai.api_key,
        organization=openai.organization
    )

    def make_prompts(self, prompt, gpt_model='gpt-4o'):
        """
        Create a conversation with a GPT model. With
        the following code you create a prompt with a GPT model
        :param prompt: str (input text)
        :param gpt_model: str (model to be selected)
        :return: response of GPT model
        """
        messages = [{'role': 'system', 'content': 'You are a helpful assistant.'}]
        messages.append({'role': 'user', 'content': prompt})

        response = openai.chat.completions.create(
            model=gpt_model,
            messages=messages,
            max_tokens=4000,
        )

        # Extract and print the model's reply
        reply = response.choices[0].message.content
        print(reply)

        # Update conversation history
        return reply

    def tokenize_text(self, text, max_token_length):
        # Tokenize the text
        tokens = self.tokenizer.encode(text)

        # If the token length exceeds the max_token_length, truncate it
        if len(tokens) > max_token_length:
            tokens = tokens[:max_token_length]  # Truncate tokens

        # Convert tokens back to text (using tokenizers decode function)
        truncated_text = self.tokenizer.decode(tokens)

        return truncated_text

    def get_embeddings(self, texts, max_token_length, model="text-embedding-3-small"):
        """
        Generate embeddings for a list of texts using OpenAI's embedding model.
        """
        embeddings = []
        for text in tqdm(texts, total=len(texts)):
            text_with_limit = self.tokenize_text(text=text, max_token_length=max_token_length)

            response = self.client.embeddings.create(input=text_with_limit, model=model)
            embedding = np.array(response.data[0].embedding)
            embeddings.append(embedding)
        return np.array(embeddings)
