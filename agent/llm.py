from dotenv import load_dotenv
from tools import agent_tools
from langchain_groq import ChatGroq
from memory import recall, remember, forget, memory_tools
import os

load_dotenv()

llm = ChatGroq(
    model='llama-3.3-70b-versatile',  
    temperature=0,                     
    max_tokens=2048,
    timeout=None,
    max_retries=3
)

SYSTEM_PROMPT = """
You are NeuroForge, an autonomous coding agent. You help users build, debug, and ship real software projects.

You have access to tools that let you create files, run terminal commands, search the web, manage projects, and execute code. Use them.

You operate in a Thought → Action → Observation loop:
- THOUGHT: Reason about what needs to happen next
- ACTION: Call the appropriate tool
- OBSERVATION: Read the result and decide your next step

Rules:
- When calling remember(), metadata values must be simple strings or numbers only. No nested objects or lists.
- Always think before acting
- Always verify your work by running code after writing it
- If something fails, read the error, reason about it, and fix it — do not give up
- Break large tasks into small steps
- Never guess — if you don't know something, use web_search
- When the task is complete, summarize what you built and where the files are
"""

llm_with_tools = llm.bind_tools(agent_tools + memory_tools)  

from tools import create_file, read_file, edit_file, delete_file, list_directory, create_directory, run_terminal, run_python_file, install_package, check_python_version

tool_map = {
    "create_file": create_file,
    "read_file": read_file,
    "edit_file": edit_file,
    "delete_file": delete_file,
    "list_directory": list_directory,
    "create_directory": create_directory,
    "run_terminal": run_terminal,
    "run_python_file": run_python_file,
    "install_package": install_package,
    "check_python_version": check_python_version,
    "remember": remember, 
    "recall": recall,
    "forget": forget
}

if __name__ == "__main__":
    USER_INPUT = input("User: ")
    message = [("system", SYSTEM_PROMPT), ("human", USER_INPUT)]
    ai_msg = llm_with_tools.invoke(message)
    print(ai_msg.content)
    print("Tool calls:", ai_msg.tool_calls)
