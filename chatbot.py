import os
import requests
import json


class Chatbot:
    """
    A chatbot class that interfaces with either OpenAI or Ollama API endpoints to generate responses
    based on a given prompt and system configuration.

    Attributes:
        model (str): The model used for response generation (default is 'llama3.1').
        system_prompt (str): The initial system prompt provided to set the context.
        api_url (str): The URL of the API endpoint for Ollama.
        api_key (str, optional): The API key for accessing OpenAI. If None, Ollama is assumed.
        temperature (float): The temperature for response generation, controlling randomness (default is 0.9).
        seed (int): The seed value for deterministic output (default is 0).
        format (str, optional): Response format, either plain text or 'json'.

    Methods:
        generate_response(prompt: str):
            Sends the user input to the API and returns the chatbot's response.
            Supports both OpenAI and Ollama endpoints.
    """

    def __init__(self, system_prompt, api_url, api_key=None, model="llama3.1", temperature=0.9, seed=0, format=None):
        self.model = model
        self.system_prompt = system_prompt
        self.api_url = api_url
        self.api_key = api_key
        self.temperature = temperature
        self.seed = seed
        self.format = format
        self.messages = [{"role": "system", "content": system_prompt}]
        self.output_tokens = []

    def generate_response(self, prompt: str):
        """
        Asks the API for a response. Supports both Ollama and OpenAI endpoints.

        Arguments:
            input: User input text
        """

        self.messages.append({"role": "user", "content": prompt})

        if self.api_key:  # Assuming OpenAI endpoint if API key is provided
            self.payload = {
                "model": "gpt-4o-mini",
                "messages": self.messages,
            }

            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            if self.format=="json":
                self.payload['response_format'] = {"type": "json_object"}

            api_endpoint = "https://api.openai.com/v1/chat/completions"
            self.api_response = requests.post(api_endpoint, json=self.payload, headers=headers)

        else:  # Assuming Ollama endpoint if API key is not provided
            self.payload = {
                "model": self.model,
                "system": self.system_prompt,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": self.temperature,
                    "seed": self.seed
                }
            }

            if self.format=="json":
               self.payload['format'] = self.format

            api_endpoint = self.api_url + "/api/generate"
            self.api_response = requests.post(api_endpoint, json=self.payload, stream=False)

        # Check if the request was successful
        if self.api_response.status_code == 200:
            if self.api_key:  # For OpenAI endpoint
                self.data = self.api_response.json()
                return self.data["choices"][0]["message"]["content"]
            else:
                for line in self.api_response.iter_lines():
                    if line:
                        self.data = json.loads(line)
                        if self.data["done"]:
                            return self.data["response"]
        else:
            # Print an error message if the request failed
            print("Error:", self.api_response.text)
