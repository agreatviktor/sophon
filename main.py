import os
import random
import json

from chatbot import Chatbot
from frontend import Frontend

ollama_api_url = "http://localhost:11434/"

def main():
    with open("levels.json") as f:
        levels_json = json.load(f)

    def load_level_1(query):
        level_info = next(
            (item for item in levels_json if item.get("level") == 1), None
        )
        secret_word = level_info["secret_word"]

        # Load bot
        for bot in level_info["bots"]:
            if bot["role"] == "guard":
                guard_bot = Chatbot(
                    system_prompt=bot["system_prompt"].replace(
                        "{secret_word}", secret_word
                    )
                )

        return guard_bot.generate_response(query)
    
    def load_level_2(query):
        level_info = next(
            (item for item in levels_json if item.get("level") == 1), None
        )
        secret_word = level_info["secret_word"]

        # Load bot
        for bot in level_info["bots"]:
            if bot["role"] == "guard":
                guard_bot = Chatbot(
                    system_prompt=bot["system_prompt"].replace(
                        "{secret_word}", secret_word
                    ),
                    api_url=ollama_api_url 
                )

        return guard_bot.generate_response(query)

    def load_level_3(query):
        level_info = next(
            (item for item in levels_json if item.get("level") == 2), None
        )
        secret_word = level_info["secret_word"]

        # Load bots
        for bot in level_info["bots"]:
            if bot["role"] == "guard":
                guard_bot = Chatbot(
                    system_prompt=bot["system_prompt"].replace(
                        "{secret_word}", secret_word
                    ),
                    api_url=ollama_api_url
                )
            if bot["role"] == "query_checker":
                query_checker_bot = Chatbot(
                    system_prompt=bot["system_prompt"].replace(
                        "{secret_word}", secret_word
                    ),
                    api_url=ollama_api_url,
                    format="json"
                )

        print("Checking if the query is asking for the password...")
        checked_query = query_checker_bot.generate_response(f"User query: {query}")
        if json.loads(checked_query)["asking_for_password"]:
            print("User query is asking for the password.")
            return "You're asking for the password, that's not allowed!"
        else:
            print("User query is valid...")
            return guard_bot.generate_response(query)

    def load_level_4(query):
        level_info = next(
            (item for item in levels_json if item.get("level") == 4), None
        )
        secret_word = level_info["secret_word"]

        # Load bots
        for bot in level_info["bots"]:
            if bot["role"] == "guard":
                guard_bot = Chatbot(
                    system_prompt=bot["system_prompt"].replace(
                        "{secret_word}", secret_word
                    ),
                    api_url=ollama_api_url
                )
            if bot["role"] == "query_checker":
                query_checker_bot = Chatbot(
                    system_prompt=bot["system_prompt"].replace(
                        "{secret_word}", secret_word
                    ),
                    api_url=ollama_api_url,
                    format="json"
                )
            if bot["role"] == "response_checker":
                response_checker_bot = Chatbot(
                    system_prompt=bot["system_prompt"].replace(
                        "{secret_word}", secret_word
                    ),
                    api_url=ollama_api_url,
                    format="json"
                )

        print("Checking if the query is asking for the password...")
        checked_query = query_checker_bot.generate_response(f"User query: {query}")
        if json.loads(checked_query)["asking_for_password"]:
            print("User query is asking for the password.")
            return "You're asking for the password, that's not allowed!"
        else:
            response = guard_bot.generate_response(query)
            print("Checking if the response contains the password...")
            checked_response = response_checker_bot.generate_response(
                f"Response: {response}"
            )
            if json.loads(checked_response)["response_contains_password"]:
                print("Response denied, it contains the password.")
                print(f"Denied response: {response}")
                return "You're trying to trick me into giving you the password, that's not allowed!"
            else:
                print("Response is valid. Sending reponse to user.")
                print("Bot response:", response)
                return response

    def intercept_response(query, level):

        print(f"Current level: {level}")
        print(f"User query: {query}")

        if level == 1:
            return load_level_1(query)

        if level == 2:
            return load_level_2(query)

        if level == 3:
            return load_level_3(query)
        
        if level == 4:
            return load_level_4(query)

    gui = Frontend(levels_json=levels_json, starting_level=4)
    gui.launch(intercept_response, levels_json)


if __name__ == "__main__":
    main()
