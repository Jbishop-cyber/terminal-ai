import subprocess

DANGEROUS_COMMANDS = [
    "rm",
    "rmdir",
    "mkfs",
    "dd",
    "shutdown",
    "reboot",
    "poweroff",
]


def run_command(command):
    try:
        if command[0] in DANGEROUS_COMMANDS:
            return f"⚠️ Dangerous command detected: {' '.join(command)}"

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode == 0:
            return result.stdout
        else:
            return result.stderr

    except subprocess.TimeoutExpired:
        return "Command timed out after 10 seconds."

    except FileNotFoundError:
        return f"Command not found: {command[0]}"
