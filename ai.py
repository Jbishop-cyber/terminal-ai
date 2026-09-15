import os
import json

from dotenv import load_dotenv
from openai import OpenAI

from database import search_memories

from tools import (
    get_current_directory,
    list_files,
    read_file,
    find_files,
    search_code,
    remember,
    update_memory_tool,
    forget_memory_tool,
    git_status,
    git_log,
    git_diff
)

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_directory",
            "description": "Get the current working directory.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": "List the files and directories in the current "
            "working directory.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read contents  of a text file in the current "
            "working directory.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "The name or path of the file to read."
                    }
                },
                "required": ["filename"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "find_files",
            "description": "Find files with a specific extention in the "
            "current directory and it's subdirectories.",
            "parameters": {
                "type": "object",
                "properties": {
                    "extention": {
                        "type": "string",
                        "description": "The file extention to search for, "
                        "without the dot. Example: py"
                    }
                },
                "required": ["extention"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_code",
            "description": "Search recursively through files in the current "
            "directory for a specific text or code pattern.",
            "parameters": {
                "type": "object",
                "properties": {
                    "pattern": {
                        "type": "string",
                        "description": "The text or code pattern "
                        "to search for."
                    }
                },
                "required": ["pattern"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "remember",
            "description": "Save important information that should be "
            "remembered across future conversations.",
            "parameters": {
                "type": "object",
                "properties": {
                    "content": {
                        "type": "string",
                        "description": "The information to remember."
                    }
                },
                "required": ["content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_memory",
            "description": "Update an existing memory with new information.",
            "parameters": {
                "type": "object",
                "properties": {
                    "memory_id": {
                        "type": "integer",
                        "description": "The ID of the memory to update."
                    },
                    "new_content": {
                        "type": "string",
                        "description": "The new information to store."
                    }
                },
                "required": ["memory_id", "new_content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "forget_memory",
            "description": "Delete an existing memory that is no longer "
            "useful or correct.",
            "parameters": {
                "type": "object",
                "properties": {
                    "memory_id": {
                        "type": "integer",
                        "description": "The ID of the memory to delete."
                    }
                },
                "required": ["memory_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "git_status",
            "description": "Show the current Git status of the project.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "git_log",
            "description": "Show the five most recent Git commits.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "git_diff",
            "description": "Show the changes that have been made to tracked files but have not been committed.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    }
]

available_tools = {
    "get_current_directory": get_current_directory,
    "list_files": list_files,
    "read_file": read_file,
    "find_files": find_files,
    "search_code": search_code,
    "remember": remember,
    "update_memory": update_memory_tool,
    "forget_memory": forget_memory_tool,
    "git_status": git_status,
    "git_log": git_log,
    "git_diff": git_diff
}


def get_response(message, system_prompt, conversation):
    conversation.append({
        "role": "user",
        "content": message
    })

    memories = search_memories(message)

    memory_text = "\n".join(
        f"- Memory ID {memory_id}: {content}"
        for memory_id, content in memories
    )

    messages = [
        {
            "role": "system",
            "content": f"""
{system_prompt}

Important memories:
{memory_text}
"""
        }
    ]

    messages.extend(conversation[-10:])

    try:
        response = client.chat.completions.create(
            model="openrouter/free",
            max_tokens=500,
            messages=messages,
            tools=tools
        )
    except Exception as e:
        print("ERROR:", e)
        return "😔 I'm unable to reach the AI service right now."

    message_response = response.choices[0].message

    # print("DEBUG TOOL CALLS:", message_response.tool_calls)

    max_tool_rounds = 5
    tool_round = 0

    while message_response.tool_calls and tool_round < max_tool_rounds:

        tool_round += 1

        messages.append(message_response)

        for tool_call in message_response.tool_calls:

            tool_name = tool_call.function.name

            tool_function = available_tools.get(tool_name)

            if tool_function:
                arguments = json.loads(tool_call.function.arguments)

                result = tool_function(**arguments)

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                })

        try:
            second_response = client.chat.completions.create(
                model="openrouter/free",
                max_tokens=500,
                messages=messages,
                tools=tools
            )
        except Exception as e:
            print("ERROR:", e)
            return "😔 I am unable to reach the AI service right now!"

        message_response = second_response.choices[0].message

    if message_response.tool_calls:
        return "😔 I couldn't complete that request because it required too many tool steps."

    answer = message_response.content

    conversation.append({
        "role": "assistant",
        "content": answer
    })

    return answer
