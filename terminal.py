import subprocess

# Commands that are permitted without confirmation.
SAFE_COMMANDS = {
    "pwd",
    "ls",
    "echo",
    "printf",
    "whoami",
    "date",
    "uname",
    "id",
    "cat",
    "head",
    "tail",
    "grep",
    "wc",
}

SAFE_GIT_COMMANDS = {
    ("status",),
    ("log",),
    ("diff",),
}

DANGEROUS_COMMANDS = {
    "rm",
    "rmdir",
    "mkfs",
    "dd",
    "shutdown",
    "reboot",
    "poweroff",
    "wipefs",
    "fdisk",
    "parted",
}


def user_choice():
    """Ask the user to approve command execution."""
    user_input = input(
        "Do you want to execute this command? (yes/no): "
    )

    return user_input.strip().lower() == "yes"


def get_actual_command(command):
    """Identify common command wrappers for safety checks."""
    if not command:
        return None

    index = 0

    # Handle common prefixes such as sudo and env.
    while index < len(command):
        current = command[index]

        if current == "sudo":
            index += 1

            # Skip common sudo options and their arguments.
            while index < len(command):
                argument = command[index]

                if argument in {"-u", "--user", "-g", "--group"}:
                    index += 2
                elif argument.startswith("-"):
                    index += 1
                else:
                    break

        elif current == "env":
            index += 1

            while index < len(command):
                argument = command[index]

                if argument.startswith("-"):
                    index += 1
                elif "=" in argument:
                    index += 1
                else:
                    break

        elif current == "command":
            index += 1

            if index < len(command) and command[index] == "--":
                index += 1

        else:
            break

    if index >= len(command):
        return None

    return command[index]


def is_safe_git_command(command):
    actual_command = get_actual_command(command)

    if actual_command != "git":
        return False

    try:
        git_index = command.index("git")
    except ValueError:
        return False

    git_arguments = command[git_index + 1:]

    return tuple(git_arguments[:1]) in SAFE_GIT_COMMANDS


def run_command(command):
    """Run a command with confirmation for unapproved commands."""

    if not isinstance(command, (list, tuple)) or not command:
        return "Error: No command provided."

    if not all(isinstance(argument, str) for argument in command):
        return "Error: Command arguments must be strings."

    if not command[0].strip():
        return "Error: Invalid command."

    command = list(command)

    try:
        actual_command = get_actual_command(command)

        if actual_command is None:
            return "Error: Could not identify the command."

        # Unknown commands and dangerous commands require approval.
        requires_confirmation = (
            (
                command[0] not in SAFE_COMMANDS
                and not is_safe_git_command(command)
            )
            or actual_command in DANGEROUS_COMMANDS
        )

        if requires_confirmation:
            print(
                f"⚠️ Command requires confirmation: "
                f"{' '.join(command)}"
            )

            if not user_choice():
                return "Command cancelled."

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=10,
            shell=False,
        )

        if result.returncode == 0:
            return result.stdout

        return result.stderr or (
            f"Command failed with exit code {result.returncode}."
        )

    except subprocess.TimeoutExpired:
        return "Command timed out after 10 seconds."

    except FileNotFoundError:
        return f"Command not found: {command[0]}"

    except PermissionError:
        return "Permission denied."

    except OSError as error:
        return f"Unable to execute command: {error}"
