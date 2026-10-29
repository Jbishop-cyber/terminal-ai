# Jay — Terminal AI Assistant

**Jay is an AI-powered programming and Linux assistant designed to bring AI assistance, terminal operations, code exploration, and Git workflows into one command-line application.**

Built with Python, Jay can answer programming questions, inspect files, search code, manage persistent memories, execute terminal commands, and assist with Git operations.

Jay is actively evolving from a personal development project into a portable, easy-to-install AI assistant for Linux users.

## Features

- **AI-powered assistance:** Ask programming questions and get help with Linux-related tasks.
- **Linux command execution:** Run terminal commands through Jay's `/run` interface, with confirmation for commands that require approval.
- **File operations:** List files and read file contents.
- **Code exploration:** Search code and locate files.
- **Persistent memory:** Store and manage memories using SQLite.
- **Git integration:** Check repository status, inspect commit history and changes, stage files, create commits, push changes, and clone repositories.
- **Automated testing:** Test terminal command-execution behavior using Python's `unittest` framework.
- **Debian packaging:** Install Jay system-wide through a Debian package.
- **APT repository:** Install and reinstall Jay through a public APT repository.

## Technology Stack

- **Language:** Python
- **AI integration:** OpenRouter API and OpenAI Python client
- **Database:** SQLite
- **Version control:** Git
- **Packaging:** Python packaging tools and Debian packages
- **Distribution:** APT repository hosted on GitHub Pages
- **Platform:** Linux

## Installation

Jay currently provides a Debian package for compatible **AMD64 Ubuntu/Debian systems using Python 3.12**.

### Option 1: Install through the APT repository

First, configure Jay's repository signing key:

```bash
sudo install -d -m 0755 /etc/apt/keyrings

curl -fsSL https://jbishop-cyber.github.io/jay-apt/public/jay-archive-key.gpg \
  -o /tmp/jay-archive-key.gpg

sudo install -m 0644 /tmp/jay-archive-key.gpg \
  /etc/apt/keyrings/jay-archive-key.gpg
```

Add the repository:

```bash
echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/jay-archive-key.gpg] https://jbishop-cyber.github.io/jay-apt stable main" \
  | sudo tee /etc/apt/sources.list.d/jay.list
```

Update the package list:

```bash
sudo apt update
```

Install Jay:

```bash
sudo apt install jay-terminal-assistant
```

After installation, launch Jay from any directory:

```bash
jay
```

**Note:** The repository configuration is required only once per system. The current package targets AMD64 systems with Python 3.12 and is not yet a universal Linux package.

### Option 2: Run from source

Clone the repository:

```bash
git clone https://github.com/Jbishop-cyber/terminal-ai.git
cd terminal-ai
```

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the dependencies:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Configure your API key as described below, then launch Jay:

```bash
python main.py
```

## Configuration

Jay uses OpenRouter to access AI models.

For development from source, create a `.env` file in the project root:

```bash
nano .env
```

Add your API key:

```dotenv
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

Replace the placeholder with your own key.

For the installed Debian package, Jay checks for a user configuration file at:

```text
~/.config/jay/.env
```

Create it with:

```bash
mkdir -p ~/.config/jay
nano ~/.config/jay/.env
```

Add the same `OPENROUTER_API_KEY` entry.

**Security:** Never commit API keys, `.env` files, or other secrets to GitHub. Each user must provide their own API key.

## Usage

### Start Jay

```bash
jay
```

When running from source:

```bash
python main.py
```

### Ask a programming question

```text
>> Explain how Python dictionaries work.
```

### Run a terminal command

```text
>> /run pwd
```

Jay executes supported terminal commands through its command interface. Commands requiring confirmation prompt the user before execution.

### Explore files and code

You can ask Jay to list files, read file contents, locate files, or search code.

For example:

```text
>> List the files in the current directory.
```

### Work with Git

Jay supports Git workflows including:

- Checking repository status.
- Viewing commit history.
- Reviewing changes.
- Staging files.
- Creating commits.
- Pushing commits.
- Cloning repositories.

Some operations require confirmation.

### Exit Jay

```text
>> exit
```

## Data Storage

Jay stores persistent conversation data in an SQLite database located at:

```text
~/.local/share/jay/conversation.db
```

For the Debian installation, configuration and conversation data are stored separately from the application files. Removing the package preserves these user files.

## Running Tests

From the source project, activate the virtual environment and run:

```bash
python -m unittest -v test_terminal
```

The terminal tests cover command execution, cancellation of commands requiring confirmation, and execution after approval.

## Troubleshooting

### Missing or invalid API key

Check that your configuration file exists and contains a valid `OPENROUTER_API_KEY`.

For a source installation, check the project's `.env` file. For a Debian installation, check `~/.config/jay/.env`.

Never share your API key when requesting troubleshooting help.

### API rate limits

OpenRouter may restrict requests based on account allowances or model availability. Check your account limits and the selected model before retrying.

### Missing Python dependencies

For a source installation, activate the virtual environment and run:

```bash
pip install -r requirements.txt
```

For the Debian package, reinstall through APT if the application environment is damaged:

```bash
sudo apt install --reinstall jay-terminal-assistant
```

### Git command failures

Ensure Git is installed and that the current directory is the intended repository. Remote operations may require appropriate authentication and permissions.

## Safety Notice

Jay is an experimental development project, not a security sandbox.

Command confirmation provides an additional safeguard but does not guarantee that every command is safe. Review commands carefully before approving them, especially commands that modify files, use elevated privileges, or interact with remote repositories.

Run Jay with appropriate user permissions and avoid granting unnecessary privileges.

## Roadmap

Jay is under active development. Planned improvements include:

- Automating package releases.
- Expanding compatibility across Linux distributions.
- Supporting additional processor architectures and Python environments.
- Improving programming assistance and codebase understanding.
- Strengthening testing and command-safety controls.
- Expanding documentation and contribution opportunities.

These are development goals, not promises that every feature is already available.

## Author

**Justice Bishop**

GitHub: https://github.com/Jbishop-cyber

## Repository

Source code: https://github.com/Jbishop-cyber/terminal-ai

APT repository: https://github.com/Jbishop-cyber/jay-apt
