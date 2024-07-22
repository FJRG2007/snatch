pre_cmd = "python cli.py"
version = "0.0.1-alpha"
dirs = {
    "temporal": "./temporal"
}

requestsHeaders = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.5"
}

INFO_MARKDOWN = f"""\
# Snatch

Repo: https://github.com/FJRG2007/snatch

Version: {version}

"""

AI = {
    "systemPrompt": "You are a helpful pentesting assistant. You will assist the user by performing the pentesting functions for them.",
    "providers": [
        {
            "name": "Anthropic",
            "models": [
                {
                    "name": "claude"
                }
            ]
        },
        {
            "name": "Dymo",
            "models": [
                {
                    "name": "dymo",
                    "tag": "Coming Soon"
                },
                {
                    "name": "ela",
                    "tag": "Coming Soon"
                }
            ]
        },
        {
            "name": "Google",
            "models": [
                {
                    "name": "gemini"
                }
            ]
        },
        {
            "name": "Groq",
            "tag": "Recommended",
            "models": [
                {
                    "name": "llama3-8b-8192"
                },
                {
                    "name": "llama3-70b-8192",
                    "tag": "Only model we currently recommend"
                },
                {
                    "name": "mixtral-8x7b-32768"
                },
                {
                    "name": "gemma-7b-it"
                },
                {
                    "name": "gemma2-9b-it"
                },
                {
                    "name": "whisper-large-v3"
                }
            ]
        },
        {
            "name": "Meta",
            "models": [
                {
                    "name": "llama3"
                }
            ]
        },
        {
            "name": "Ollama",
            "tag": "Local",
            "models": [
                {
                    "name": "llama3"
                }
            ]
        },
        {
            "name": "OpenAI",
            "models": [
                {
                    "name": "gpt-4o",
                    "tag": "Application required to OpenAI"
                },
                {
                    "name": "gpt-4",
                    "tag": "Application required to OpenAI"
                },
                {
                    "name": "gpt-3.5-turbo"
                }
            ]
        },
        {
            "name": "Perplexity",
            "models": [
                {
                    "name": "llama3"
                }
            ]
        }
    ]
}

DEFAULT_API_KEYS = {
    "HUNTER": ["5d5015259730682de8b542355525b16ab7026c976a72993d", "83e338e3a43cdcc649a1ea49957d2c0223b601bb", "36a4ce62890b18e216951bb2cf4b9748129418f8"]
}