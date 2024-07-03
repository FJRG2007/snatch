import importlib
import json
from rich import print as rprint

tools = [
    {
        "worker": "src.services.portscanner.worker", # worker module path
        "type": "function",
        "function": {
            "name": "scan_ports",
            "description": "scan the target host with the given range of ports, then generate a report of open ports",
            "parameters": {
                "type": "object",
                "properties": {
                    "target": {
                        "type": "string",
                        "description": "the target host to scan, example: 1.1.1.1 or example.com",
                    },
                    "ports": {
                        "type": "string",
                        "description": "the range of ports to scan, example: 1-100 or 1,2,3 or 1-100,200-300 or 1-100,200",
                    },
                },
                "required": ["target", "ports"]
            }
        }
    }
]
def get_tools():
    tools_ = json.loads(json.dumps(tools.copy(), ensure_ascii=False))
    no_worker_tools = []
    for tool_ in tools_:
        tool_.pop("worker")
        no_worker_tools.append(tool_)
    return no_worker_tools

def get_worker(name):
    tool = list(filter(lambda x: x["function"]["name"] == name, tools))[0]
    return importlib.import_module(tool["worker"]).main