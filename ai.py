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
    git_diff,
    git_add,
    git_commit,
    git_push,
    git_clone
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
            "description": "List files and directories inside the specified "
            "directory, including hidden entries. Defaults to the current "
            "directory.",
            "parameters": {
                "type": "object",
                "properties": {
                    "directory": {
                        "type": "string",
                        "description": "The directory to inspect. Default to the current directory."
                    }
                },
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
            "description": "Show changes to tracked files that have not been committed.",
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
            "name": "git_add",
            "description": "Stage specified files for a Git commit after user confirmation.",
            "parameters": {
                "type": "object",
                "properties": {
                    "files": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                        "description": "A list of file paths to stage."
                    }
                },
                "required": ["files"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "git_commit",
            "description": "Create a Git commit with the supplied message after user confirmation.",
            "parameters": {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "The commit message."
                    }
                },
                "required": ["message"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "git_push",
            "description": "Push local commits to a remote Git repository after user confirmation.",
            "parameters": {
                "type": "object",
                "properties": {
                    "remote": {
                        "type": "string",
                        "description": "The Git remote name, usually origin."
                    },
                    "branch": {
                        "type": "string",
                        "description": "The branch to push, usually main."
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "git_clone",
            "description": "Clone a Git repository after user confirmation.",
            "parameters": {
                "type": "object",
                "properties": {
                    "repository_url": {
                        "type": "string",
                        "description": "The repository URL."
                    },
                    "destination": {
                        "type": "string",
                        "description": "Optional local directory for the cloned repository."
                    }
                },
                "required": ["repository_url"]
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
    "git_diff": git_diff,
    "git_add": git_add,
    "git_commit": git_commit,
    "git_push": git_push,
    "git_clone": git_clone
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
                try:
                    arguments = json.loads(tool_call.function.arguments)

                    if not isinstance(arguments, dict):
                        raise ValueError("Tool arguments must be a JSON object.")

                    result = tool_function(**arguments)

                except (json.JSONDecodeError, TypeError, ValueError) as error:
                    result = f"Tool execution error for {tool_name}: {error}"

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(result)
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
