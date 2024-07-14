pre_cmd = "python cli.py"
version = "0.0.1-alpha"
dirs = {
    "temporal": "./temporal"
}

requestsHeaders = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 "
                  "Safari/537.36",
    "Accept-Language": "en-US,en;q=0.5"
}

INFO_MARKDOWN = """\
# Snatch

Repo: https://github.com/FJRG2007/snatch

## Features

Coming Soon!

- Typography *emphasis*, **strong**, `inline code` etc.
- Headers
- Lists (bullet and ordered)
- Syntax highlighted code blocks
- Tables!
"""

AI = {
    "defaultSystemPrompt": "You are a helpful pentesting assistant. You will assist the user by performing the "
                           "pentesting functions for them.",
    "providers": [
        {
            "name": "Anthropic",
            "models": ["claude"]
        },
        {
            "name": "Dymo",
            "models": ["dymo", "ela"]
        },
        {
            "name": "Google",
            "models": ["gemini"]
        },
        {
            "name": "Groq",
            "models": ["llama3-8b-8192", "llama3-70b-8192", "mixtral-8x7b-32768", "gemma-7b-it", "gemma2-9b-it",
                       "whisper-large-v3"]
        },
        {
            "name": "Meta",
            "models": ["llama3"]
        },
        {
            "name": "Ollama",
            "models": ["llama3"]
        },
        {
            "name": "OpenAI",
            "models": ["gpt-4o", "gpt-4", "gpt-3.5-turbo"]
        },
        {
            "name": "Perplexity",
            "models": ["llama3"]
        }
    ]
}

DEFAULT_API_KEYS = {
    "HUNTER": ["5d5015259730682de8b542355525b16ab7026c976a72993d", "83e338e3a43cdcc649a1ea49957d2c0223b601bb",
               "36a4ce62890b18e216951bb2cf4b9748129418f8"]
}
