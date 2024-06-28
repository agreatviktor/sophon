import os
import random
import json
import argparse

from chatbot import Chatbot
from frontend import Frontend

def main(api_url, starting_level):
    with open("levels.json") as f:
        levels_json = json.load(f)

    def get_level_info(levels_json, level):
        return next((item for item in levels_json if item.get("level") == level), None)

    def load_level_1(query, level_info):

        secret_word = level_info["secret_word"]

        # Load bot
        for bot in level_info["bots"]:
            if bot["role"] == "guard":
                guard_bot = Chatbot(
                    system_prompt=bot["system_prompt"].replace(
                        "{secret_word}", secret_word
                    ),
                    api_url=api_url,
                    model=bot["model"]
                )

        return guard_bot.generate_response(query)
    
    def load_level_2(query, level_info):

        secret_word = level_info["secret_word"]

        # Load bot
        for bot in level_info["bots"]:
            if bot["role"] == "guard":
                guard_bot = Chatbot(
                    system_prompt=bot["system_prompt"].replace(
                        "{secret_word}", secret_word
                    ),
                    api_url=api_url,
                    model=bot["model"]
                )

        return guard_bot.generate_response(query)

    def load_level_3(query, level_info):

        secret_word = level_info["secret_word"]

        # Load bots
        for bot in level_info["bots"]:
            if bot["role"] == "guard":
                guard_bot = Chatbot(
                    system_prompt=bot["system_prompt"].replace(
                        "{secret_word}", secret_word
                    ),
                    api_url=api_url,
                    model=bot["model"]
                )
            if bot["role"] == "query_checker":
                query_checker_bot = Chatbot(
                    system_prompt=bot["system_prompt"].replace(
                        "{secret_word}", secret_word
                    ),
                    api_url=api_url,
                    model=bot["model"],
                    format="json",
                )

        print("Checking if the query is asking for the password...")
        checked_query = query_checker_bot.generate_response(f"User query: {query}")
        if json.loads(checked_query)["asking_for_password"]:
            print("User query is asking for the password.")
            return "You're asking for the password, that's not allowed!"
        else:
            print("User query is valid...")
            return guard_bot.generate_response(query)

    def load_level_4(query, level_info):

        secret_word = level_info["secret_word"]

        # Load bots
        for bot in level_info["bots"]:
            if bot["role"] == "guard":
                guard_bot = Chatbot(
                    system_prompt=bot["system_prompt"].replace(
                        "{secret_word}", secret_word
                    ),
                    api_url=api_url,
                    model=bot["model"]
                )
            if bot["role"] == "query_checker":
                query_checker_bot = Chatbot(
                    system_prompt=bot["system_prompt"].replace(
                        "{secret_word}", secret_word
                    ),
                    api_url=api_url,
                    model=bot["model"],
                    format="json"
                )
            if bot["role"] == "response_checker":
                response_checker_bot = Chatbot(
                    system_prompt=bot["system_prompt"].replace(
                        "{secret_word}", secret_word
                    ),
                    api_url=api_url,
                    model=bot["model"],
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

        level_info = get_level_info(levels_json, level)

        if level == 1:
            return load_level_1(query, level_info)

        if level == 2:
            return load_level_2(query, level_info)

        if level == 3:
            return load_level_3(query, level_info)
        
        if level == 4:
            return load_level_4(query, level_info)

    gui = Frontend(levels_json=levels_json, starting_level=starting_level)
    gui.launch(intercept_response, levels_json)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--api_url', type=str, default='http://localhost:11434', help='The API URL to be used (default: http://localhost:11434).')
    parser.add_argument('--starting_level', type=int, default=1, help='The starting level (default: 1).')
    
    args = parser.parse_args()
    main(args.api_url, args.starting_level)
