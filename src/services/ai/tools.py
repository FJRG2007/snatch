import importlib
import json

tools = [
    {
        "worker": "src.services.portscanner.worker",  # Worker module path.
        "type": "function",
        "function": {
            "name": "scan_ports",
            "description": "Scan the target host with the given range of ports, then generate a report of open ports.",
            "parameters": {
                "type": "object",
                "properties": {
                    "target": {
                        "type": "string",
                        "description": "The target host to scan, example: 1.1.1.1 or example.com",
                    },
                    "ports": {
                        "type": "string",
                        "description": "The range of ports to scan, example: 1-100 or 1,2,3 or 1-100,200-300 or "
                                       "1-100,200. For common ports set the value common instead of defining them "
                                       "yourself. (1,2,3 or 16-24 or *-24 or 24-* or * or common)",
                    },
                },
                "required": ["target", "ports"]
            }
        }
    }
]


def get_tools():
    no_worker_tools = []
    for tool_ in json.loads(json.dumps(tools.copy(), ensure_ascii=False)):
        tool_.pop("worker")
        no_worker_tools.append(tool_)
    return no_worker_tools


def get_worker(name):
    return importlib.import_module(list(filter(lambda x: x["function"]["name"] == name, tools))[0]["worker"]).main
