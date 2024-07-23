# jit

**jit** is a command-line tool designed to automate the process of creating pull requests for your projects. 
It integrates with git, and GitHub CLI and leverages local language models to generate meaningful PR descriptions based on your commits and diffs.

## Features

- **Automated PR Creation**: Automatically generates PR description, and creates PR on GitHub.

## Prerequisites

Before installing jit, ensure you have the following installed:

- [Python](https://www.python.org/downloads/) 3.6 or higher
- `pip3` for Python package management
- [Homebrew](https://brew.sh/) (for macOS users) to install certain dependencies

The installation process will prompt you to download the following:

- [Github CLI](https://cli.github.com/)
- [Ollama](https://ollama.com/) - with the llama3 model

## Installation

Clone the repository and navigate to the project directory:

```bash
git clone https://github.com/gsvh/jit.git
cd jit
```

To install **jit**, simply run:

```bash
make setup
```

## Usage

Once **jit** is installed, you can start using it to manage your pull requests. Here’s how to get started:

### Creating Pull Requests

To create a pull request for the current branch:

```bash
jit push
```

To run in dry mode (generate PR description without creating a PR):

```bash
jit push --dry
```

### Viewing Welcome Message

To view the welcome message and get started:

```bash
jit welcome
```

### Updating jit

To update jit to the latest stable version:

```bash
jit update
```

## Uninstallation

To uninstall **jit** and optionally remove installed dependencies:

```bash
make uninstall
```

# Roadmap

- [ ] Add mark as draft feature 📝
- [ ] Add PR template compatibility 🧑‍🍳
- [ ] Make installable using a package manger (no more cloning 🎉)
- [ ] Add tests 🧪
- More to come! 🏃

## Contributing

Contributions to **jit** are welcome! Please refer to the CONTRIBUTING.md file for more details on how to submit pull requests, report issues, or make feature suggestions.
