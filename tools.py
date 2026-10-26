from terminal import run_command
from database import save_memory, update_memory, forget_memory


def get_current_directory():
    output = run_command(["pwd"])
    return output.strip()


def list_files(directory="."):
    if not isinstance(directory, str) or not directory.strip():
        return "Error: Directory must be a non-empty string."

    output = run_command(["ls", "-la", "--", directory])
    return output.strip()


def read_file(filename):
    if not isinstance(filename, str) or not filename.strip():
        return "Error: Filename must be a non-empty string."
    try:
        with open(filename, "r", encoding="utf-8") as file:
            content = file.read()

        if not content:
            return f"The file '{filename}' is empty."

        return content

    except FileNotFoundError:
        return f"File not found: {filename}"

    except IsADirectoryError:
        return f"'{filename}' is a directory, not a file."

    except PermissionError:
        return f"Permission denied: {filename}"

    except OSError as error:
        return f"Unable to read '{filename}': {error}"


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
    return run_command(["git", "status"])


def git_log():
    return run_command(["git", "log", "-5", "--oneline"])


def git_diff():
    return run_command(["git", "diff"])


def git_add(files):
    if not isinstance(files, list) or not files:
        return "Error: Provide a list of files to stage."

    if not all(isinstance(filename, str) and filename.strip() for filename in files):
        return "Error: Every filename must be a non-empty string."

    return run_command(["git", "add", "--", *files])


def git_commit(message):
    if not isinstance(message, str) or not message.strip():
        return "Error: Commit message cannot be empty."

    return run_command(["git", "commit", "-m", message])


def git_push(remote="origin", branch="main"):
    if not isinstance(remote, str) or not remote.strip():
        return "Error: Remote name cannot be empty."

    if not isinstance(branch, str) or not branch.strip():
        return "Error: Branch name cannot be empty."

    return run_command(["git", "push", remote, branch])


def git_clone(repository_url, destination=None):
    if not isinstance(repository_url, str) or not repository_url.strip():
        return "Error: Repository URL cannot be empty."

    command = ["git", "clone", "--", repository_url]

    if destination is not None:
        if not isinstance(destination, str) or not destination.strip():
            return "Error: Destination cannot be empty."

        command.append(destination)

    return run_command(command)
