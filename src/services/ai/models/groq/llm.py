import os, json
import groq
from ... import tools
from src.lib.data import AI
from src.lib.config import config
from src.utils.basics import terminal

class LLM:
    
    def __init__(self, context = []):
        self.client = groq.Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.tools = tools.get_tools()
        self.system = AI["systemPrompt"]
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
            terminal("ai", f"[bold magenta]AI: {message.content}[/bold magenta]")
        except groq.NotFoundError as e: terminal("e", f"Define a valid AI model.")
        except groq.RateLimitError as e: terminal("e", f"Check your Groq plan and billing details.")
        except groq.AuthenticationError as e: terminal("e", f"Groq API KEY invalid.")
        except Exception as e: terminal("e", e)