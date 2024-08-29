# Sophon

Sophon is a game that takes inspiration from https://gandalf.lakera.ai/ (Gandalf). The objective of the game is to try to convince an AI to give you a secret word that the AI has received. When you have received the secret word, you can use it to advance to the next level. 

# Installation

## Requirements
**Git**

Git is required to clone the repository. If you don't have Git installed, you can download it from: https://git-scm.com/downloads

**Python**

Python 3.7 or higher is required. You can download Python from: https://www.python.org/downloads/

**Virtual Environment (venv)**

It's recommended to use a virtual environment. Python 3.3+ comes with the venv module. If you're using an earlier version, you can install it with:


**Ollama**

The default backend of Sophon is [Ollama](https://github.com/ollama/ollama), a simple server that can run large language models locally. Install Ollama for your platform using the instructions in the Ollama github repo: https://github.com/ollama/ollama

## Installing Sophon

```
python -m venv venv
```

2. Activate the virtual environment:

- On Windows:
```
.\venv\Scripts\activate
```

- On macOS and Linux:
```
source venv/bin/activate
```

3. Clone the repo:

```
git clone https://github.com/agreatviktor/sophon.git
```

Install dependencies:
```
pip install -r requirements.txt
```

Run the application:
```
python main.py
```

The default api_url for Ollama is http://localhost:11434, but you can change this by passing --api-url to main.py like this:
```
python main.py --api-url=http://my-server:11434
```

You can also launch the application at a specified starting level using --starting-level, for example to start at level 2:
```
python main.py --starting-level=2
```
