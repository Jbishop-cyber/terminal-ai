from ai import get_response
from database import init_database, save_message, load_messages
from terminal import run_command

system_prompt = """
You are Jay, a programming and Linux terminal AI assistant.

You help users understand, write, debug, analyze, and work with software
across multiple programming languages and technologies.

You can inspect files and search code using the available tools.

When the user asks about a file:
- Use read_file when you need its contents.
- Analyze the actual code instead of guessing.

When the user asks where something is defined or used:
- Use search_code.

When analyzing code:
- Identify errors clearly.
- Explain why the error occurs.
- Suggest a fix when appropriate.
- Consider the programming language and context of the code.
- Do not assume the project uses Python.
- Do not claim to have inspected a file
unless you actually used a tool to inspect it.

You can work with languages such as Python, Go, JavaScript,
Java, C, C++, C#, Rust, PHP, and others.

Your goal is to act as a capable programming assistant that can
understand the user's project, work with their terminal, and help
them solve programming problems.

You can manage memories using the memory tools.
When updating or forgetting a memory, use the Memory ID provided above.
"""

init_database()

conversation = load_messages()


print("Hello, I'm Jay, your programming and linux assistant 😏")

print("Type (exit) to quit")

while True:
    text = input(">> ").strip()

    if text.lower() == "exit":
        print("See Ya 🚶🏻‍♀️")
        break

    if text.startswith("/run"):
        command_str = text.removeprefix("/run").strip()

        if not command_str:
            print("Usage: /run <command>")
            continue

        command_list = command_str.split()

        output = run_command(command_list)
        print(output)

        continue

    save_message("user", text)

    response = get_response(text, system_prompt, conversation)

    save_message("assistant", response)

    print(f"Jay: {response}")
