# Sophon

Sophon is a game that takes inspiration from https://gandalf.lakera.ai/ (Gandalf). The objective of the game is to try to convince an AI to give you a secret word that the AI has received. When you have received the secret word, you can use it to advance to the next level. 

# Installation

## Requirements

**Ollama**

The default backend of Sophon is [Ollama](https://github.com/ollama/ollama), a simple server that can run large language models locally. Install Ollama for your platform using the instructions in the Ollama github repo: https://github.com/ollama/ollama

## Installing Sophon

Clone the repo:
```
git clone https://github.com/agreatviktor/sophon.git
```

Install dependencies, preferably in an environment manager like [venv](https://docs.python.org/3/library/venv.html) or [conda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html):
```
pip install -r requirements.txt
```

Run the application:
```
python main.py
```

The default api_url for Ollama is http://localhost:11434, but you can change this by passing --api_url to main.py like this:
```
python main.py --api_url=http://my-server:11434
```

You can also launch the application at a specified starting level using --starting_level, for example to start at level 2:
```
python main.py --starting_level=2
```