import json
import openai
from . import tools
from os import getenv
from rich import print as rprint
from src.lib.config import config

class LLM:

    def __init__(self, context = []):
        self.client = openai.OpenAI(api_key=getenv("OPENAI_API_KEY"))
        self.tools = tools.get_tools()
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
        
            message = response.choices[0].message
            messages.append(message.model_dump())
            if message.tool_calls is not None:
                for tool_call in message.tool_calls:
                    tool_name = tool_call.function.name
                    tool_worker = tools.get_worker(tool_name)
                    tool_args = json.loads(tool_call.function.arguments)
                    tool_response = tool_worker(**tool_args)
                    messages.append({
                        "role": "tool",
                        "content": json.dumps({
                            "open_ports": tool_response
                        }, ensure_ascii=False),
                        "name": tool_name,
                        "tool_call_id": tool_call.id
                    })
                second_response = self.client.chat.completions.create(
                    model=config.ai.model,
                    messages=messages,
                    temperature=config.ai.temperature,
                    max_tokens=config.ai.max_tokens
                )
                message = second_response.choices[0].message
                messages.append(message.model_dump())
                return message.content, messages
            rprint(f"[bold magenta]AI: {message.content}[/bold magenta]")
        except openai.NotFoundError as e: rprint(f"[red]Error: Define a valid AI model.[/red]")
        except openai.RateLimitError as e: rprint(f"[red]Error: Check your OpenAI plan and billing details.[/red]")
        except openai.AuthenticationError as e: rprint(f"[red]Error: OpenAI API KEY invalid.[/red]")