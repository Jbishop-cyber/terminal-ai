# Jay — Terminal AI Assistant

Jay is a Python-based AI assistant designed to bring AI-powered programming assistance and Linux terminal operations into one application.

Jay can answer programming questions, inspect files, search code, manage persistent memories, and perform Git operations through an integrated set of tools.

## Features

- **AI-powered assistance:** Interact with an AI assistant for programming and Linux-related tasks.
- **Linux command execution:** Execute terminal commands with confirmation for commands that require approval.
- **File operations:** List files and read file contents.
- **Code analysis:** Search code and locate files.
- **Persistent memory:** Store and manage memories using SQLite.
- **Git integration:** Check repository status, view commit history and differences, stage files, commit changes, push commits, and clone repositories.
- **Automated testing:** Test command-execution behavior using Python's `unittest` framework.

## Technology Stack

- Python 3.12+
- OpenRouter API
- OpenAI Python client
- SQLite
- Git
- Linux

## Prerequisites

Before installing Jay, ensure you have:

- Python 3.12 or a compatible newer version.
- Git.
- A Linux environment.
- An OpenRouter account and API key.
- An internet connection for AI requests.

## Installation

### 1. Clone the repository

Open your terminal and run:

```bash
git clone https://github.com/Jbishop-cyber/terminal-ai.git
cd terminal-ai
```

### 2. Create a virtual environment

Create an isolated Python environment:

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

Upgrade pip and install the project's dependencies:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure your API key

Jay uses OpenRouter to access an AI model.

Create a `.env` file in the project root:

```bash
nano .env
```

Add the following line, replacing the placeholder with your own API key:

```dotenv
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

Save the file and exit the editor.

**Security:** Never publish your API key or commit your `.env` file to GitHub. Each user must configure their own API key.

### 5. Run Jay

Start the application:

```bash
python main.py
```

You should see a welcome message and the `>>` input prompt.

Enter a programming question or a request for assistance.

To exit, type:

```text
exit
```

## Using Jay

### Ask a programming question

At the `>>` prompt, enter a question, such as:

```text
Explain how Python dictionaries work.
```

### Inspect files

You can ask Jay to list files in a directory or read a file's contents.

For example:

```text
List the files in the current directory.
```

### Execute a Linux command

Jay supports direct terminal commands through the `/run` interface.

For example:

```text
/run pwd
```

Commands requiring confirmation prompt the user before execution.

### Work with Git

You can ask Jay to perform supported Git operations, including:

- Checking repository status.
- Viewing commit history.
- Reviewing changes.
- Staging files.
- Creating commits.
- Pushing commits to a remote repository.
- Cloning repositories.

Some operations require explicit confirmation before execution.

## Running Tests

To run the automated terminal tests, execute:

```bash
python -m unittest -v test_terminal
```

These tests cover safe command execution, cancellation of a command requiring confirmation, and execution after approval.

## Troubleshooting

### Missing or invalid API key

Check that your `.env` file exists in the project root and contains a valid `OPENROUTER_API_KEY`.

### API rate limits

OpenRouter may limit requests based on your account allowance or the availability of the selected model. If you receive a rate-limit error, check your account limits and retry when permitted.

### Missing Python dependencies

Ensure your virtual environment is activated and run:

```bash
pip install -r requirements.txt
```

### Git command failures

Check that Git is installed and that the current directory is the intended repository. Operations involving remote repositories may also require appropriate authentication and permissions.

## Safety Notice

Jay is an experimental learning project, not a security sandbox.

Command confirmation provides an additional safeguard, but it does not guarantee that every command is safe. Review commands carefully before approving them, especially commands that modify files, use elevated privileges, or interact with remote repositories.

Run Jay with appropriate user permissions and avoid granting unnecessary privileges.

## Project Status

Jay is under active development. Features, safety controls, and reliability may change as the project evolves.

## Author

**Justice Bishop**

GitHub: https://github.com/Jbishop-cyber