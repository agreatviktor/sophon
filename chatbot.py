import os
import requests
import json


class Chatbot:

    def __init__(self, system_prompt, api_url, model="llama3.1", temperature=0.9, seed=0, format=None, api_key=None):
        self.model = model
        self.system_prompt = system_prompt
        self.api_url = api_url
        self.temperature = temperature
        self.seed = seed
        self.format = format
        self.messages = [{"role": "system", "content": system_prompt}]
        self.output_tokens = []
        self.api_key = api_key

    def generate_response(self, prompt: str):
        """
        Asks the Ollama API for a response.

        Arguments:
            input: User input text
        """

        

        
        if "googleapis.com" in self.api_url:
            self.payload = {
                "model": self.model,
                "messages": [{"role": "system", "content": self.system_prompt}, {"role": "user", "content": prompt}],
                "format": "json" if self.format is not None else None
            }
            self.payload["model"] = "meta/llama3-8b-instruct-maas"
            self.payload["stream"] = False
            headers = {
                "Authorization": "Bearer " + self.api_key,
                "Content-Type": "application/json"
            }
            self.api_response = requests.post(self.api_url, headers=headers, json=self.payload)
        else:
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
            api_endpoint = self.api_url + "/api/generate"
            self.api_response = requests.post(api_endpoint, json=self.payload, stream=False)

        # Check if the request was successful
        if self.api_response.status_code == 200:
            if "googleapis.com" in self.api_url:
                return self.api_response.json()["choices"][0]["message"]["content"]
            else:
                for line in self.api_response.iter_lines():
                    if line:
                        self.data = json.loads(line)
                        if self.data["done"]:
                            return self.data["response"]
        else:
            # Print an error message if the request failed
            print("Error:", self.api_response.text)
