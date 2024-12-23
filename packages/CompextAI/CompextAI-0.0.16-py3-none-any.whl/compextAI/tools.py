from typing import Callable

ToolRegistry = {}

def register_tool(func:Callable):
    ToolRegistry[func.__name__] = func
    return ToolRegistry[func.__name__]

def get_tool(name:str):
    if name not in ToolRegistry:
        raise Exception(f"Tool {name} not found, please register the tool first")
    return ToolRegistry[name]

def get_tool_names():
    return ToolRegistry.keys()
