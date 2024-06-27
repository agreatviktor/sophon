import os
import requests
import json

ollama_api_url = os.getenv("OLLAMA_API_URL", "http://100.99.72.98:11434/")


class Chatbot:

    def __init__(self, system_prompt, api_url="http://localhost:11434/", model="llama3",  temperature=0.9, seed=0, format=None):
        self.model = model
        self.system_prompt = system_prompt
        self.api_url = api_url
        self.temperature = temperature
        self.seed = seed
        self.format = format
        self.messages = [{"role": "system", "content": system_prompt}]
        self.output_tokens = []

    def generate_response(self, prompt: str):
        """
        Asks the Ollama API for a response.

        Arguments:
            input: User input text
        """

        self.payload = {
            "model": self.model,
            "system": self.system_prompt,
            "prompt": prompt,
            "temperature": self.temperature,
            "seed": self.seed,
            "stream": False,
        }

        if self.format is not None:
            self.payload['format'] = self.format

        api_endpoint = self.api_url + "api/generate"
        self.api_response = requests.post(api_endpoint, json=self.payload, stream=False)

        # Check if the request was successful
        if self.api_response.status_code == 200:
            for line in self.api_response.iter_lines():
                if line:
                    self.data = json.loads(line)
                    if self.data["done"]:
                        return self.data["response"]
        else:
            # Print an error message if the request failed
            print("Error:", self.api_response.text)

    def chat_stream(self, prompt: str, history: dict):
        """
        Asks the Ollama API for a response.

        Arguments:
            input: User input text
        """
        self.latest_response = ""

        self.messages.append({"role": "user", "content": prompt})
        self.payload = {"model": self.model, "messages": self.messages}
        api_endpoint = ollama_api_url + "api/chat"
        self.api_response = requests.post(api_endpoint, json=self.payload, stream=True)

        # Check if the request was successful
        if self.api_response.status_code == 200:
            # Iterate over the chunks in the api_response
            for line in self.api_response.iter_lines():
                if line:
                    self.data = json.loads(line)
                    if not self.data["done"]:
                        self.latest_response = (
                            self.latest_response + self.data["message"]["content"]
                        )
                        yield self.latest_response

                        print(self.data["message"]["content"], end="", flush=True)

                    elif self.data["done"]:
                        # Append the AI's response as an "assistant" role message to the list of messages
                        self.messages.append(
                            {"role": "assistant", "content": self.latest_response}
                        )
        else:
            # Print an error message if the request failed
            print("Error:", self.api_response.text)
