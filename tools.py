import subprocess

from terminal import run_command
from database import save_memory, update_memory, forget_memory


def get_current_directory():
    output = run_command(["pwd"])
    return output.strip()


def list_files():
    output = run_command(["ls"])
    return output.strip()


def read_file(filename):
    try:
        with open(filename, "r") as file:
            return file.read()
    except FileNotFoundError:
        return f"File not found: {filename}"
    except IsADirectoryError:
        return f"{filename} is a directory."


def find_files(extention):
    output = run_command(["find", ".",
                          "-type", "f", "-name", f"*.{extention}"])
    return output.strip()


def search_code(pattern):
    output = run_command([
        "grep",
        "-R",
        "-n",
        pattern,
        "."
    ])

    return output.strip()


def remember(content):
    save_memory(content)
    return "Memory saved successfully."


def update_memory_tool(memory_id, new_content):
    return update_memory(memory_id, new_content)


def forget_memory_tool(memory_id):
    return forget_memory(memory_id)


def git_status():
    result = subprocess.run(
        ["git", "status"],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        return result.stderr

    return result.stdout


def git_log():
    result = subprocess.run(
        ["git", "log", "-5", "--oneline"],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        return result.stderr

    return result.stdout


def git_diff():
    result = subprocess.run(
        ["git", "diff"],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        return result.stderr

    return result.stdout
