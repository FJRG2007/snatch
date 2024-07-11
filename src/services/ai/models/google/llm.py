import os, json
# from . import tools
from src.lib.config import config
import google.generativeai as genai
from src.utils.basics import terminal

class LLM:

    def __init__(self, context = []):
        self.client = genai.configure(api_key=os.getenv("GOOGLE_GEMINI_API_KEY"))
        # self.tools = tools.get_tools()
        self.system = "You are a helpful pentesting assistant. You will assist the user by performing the pentesting functions for them."
        self.context = context
        
    def process_request(self, prompt):
        try: 
            messages = [
                {"role": "system", "content": self.system},
                *self.context,
                {"role": "user", "content": prompt},
            ]
            response = self.client.chat.completions.create(
                model = config.ai.model,
                messages = messages,
                temperature = config.ai.temperature,
                max_tokens = config.ai.max_tokens,
                tools = self.tools,
                tool_choice = "auto"
            )
        except Exception as e: terminal("e", e)