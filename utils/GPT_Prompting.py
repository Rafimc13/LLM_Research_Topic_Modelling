import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv("secrets.env")


class PromptingGPT:
    def __init__(self):
        # Load API key and organization from environment variables
        openai.api_key = os.getenv("OPENAI_API_KEY")  # Ensure your environment variables are loaded correctly

        # Initialize OpenAI client with API key
        self.client = openai.OpenAI(api_key=openai.api_key, organization=openai.organization)

    ClientOpenAi = openai.OpenAI(
        api_key=openai.api_key,
        organization=openai.organization
    )

    def make_prompts(self, prompt, GPT_model='gpt-4o'):
        """
        Create a conversation with a GPT model. With
        the following code you create a prompt with a GPT model
        :param prompt: str (input text)
        :param GPT_model: str (model to be selected)
        :return: response of GPT model
        """
        messages = [{'role': 'system', 'content': 'You are a helpful assistant.'}]
        messages.append({'role': 'user', 'content': prompt})

        response = openai.chat.completions.create(
            model=GPT_model,
            messages=messages,
            max_tokens=4000,
        )

        # Extract and print the model's reply
        reply = response.choices[0].message.content
        print(reply)

        # Update conversation history
        return reply
