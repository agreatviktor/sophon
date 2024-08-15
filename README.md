# Sophon

Sophon is a game that takes inspiration from https://gandalf.lakera.ai/ (Gandalf). The objective of the game is to try to convince an AI to give you a secret word that the AI has received. When you have received the secret word, you can use it to advance to the next level. 

# Installation

## Requirements

**Ollama**

The default backend of Sophon is [Ollama](https://github.com/ollama/ollama), a simple server that can run large language models locally. Install Ollama for your platform using the instructions in the Ollama github repo: https://github.com/ollama/ollama

## Installing Sophon

Clone the repo:
``` bash
git clone https://github.com/agreatviktor/sophon.git
```

Install dependencies, preferably in an environment manager like [venv](https://docs.python.org/3/library/venv.html) or [conda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html):
``` bash
pip install -r requirements.txt
```

Run the application:
``` bash
python main.py
```

The default api_url for Ollama is http://localhost:11434, but you can change this by passing --api_url to main.py like this:
``` bash
python main.py --api_url=http://my-server:11434
```

You can also launch the application at a specified starting level using --starting_level, for example to start at level 2:
``` bash
python main.py --starting_level=2
```

# Hosting an external Ollama server

To host an external Ollama server, install Ollama normally. To allow connections to Ollama from outside your computer, set OLLAMA_HOST to 0.0.0.0:

``` bash
export OLLAMA_HOST=0.0.0.0
```

And then run Ollama using "ollama serve":

``` bash
ollama serve
```

To allow your application to access the Ollama server, you need to allow external connections from your computer to port 11434. This can be done using Tailscale, an app that allows you to connect to your server from your personal computer with Tailscale installed, or from any computer using Tailscale Funnel. 

First install Tailscale on your computer: https://tailscale.com/download

Then enable Tailscale Funnel using the following guide: https://tailscale.com/kb/1223/funnel

Finally, you can connect to your Ollama server from your personal computer or any other computer using Tailscale Funnel by running this command in a terminal: 

``` bash
tailscale funnel 11434
```

This will give you a url that you can use to access the Ollama server. You can also use this url with your application, but it is recommended to use the --api_url flag in main.py instead of changing the api_url directly.