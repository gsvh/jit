# jit

**jit** is a command-line tool designed to automate the process of creating requests for your projects. It integrates with the GitHub CLI and leverages local language models to generate meaningful PR descriptions based on your commits and diffs.

## Features

- **Automated PR Creation**: Automatically generates and pushes PRs to GitHub.

## Prerequisites

Before installing jit, ensure you have the following installed:

- Python 3.6 or higher
- `pip3` for Python package management
- Homebrew (for macOS users) to install certain dependencies

## Installation

Clone the repository and navigate to the project directory:

```bash
git clone https://github.com/yourusername/jit.git
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

## Uninstallation

To uninstall **jit** and optionally remove installed dependencies:

```bash
make uninstall_jit
```

## Contributing

Contributions to **jit** are welcome! Please refer to the CONTRIBUTING.md file for more details on how to submit pull requests, report issues, or make feature suggestions.
