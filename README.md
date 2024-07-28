# jit

**jit** is a command-line tool designed to automate the process of creating pull requests for your projects.
It integrates with git, and GitHub CLI and leverages local language models to generate meaningful PR descriptions based on your commits and diffs.

## Features

- **Automated PR Creation**: Automatically generates PR description, and creates PR on GitHub.

## Prerequisites

- [Python](https://www.python.org/downloads/) 3.11 or higher
- [Github CLI](https://cli.github.com/)

## Installation

```bash
pip install jit-cli
```

## Usage

Once **jit** is installed, you need to download the LLM model.

```bash
jit pull-model
```

NOTE: The current model (llama3) is about ~4.7GB, so this step will take some time

### Creating Pull Requests

To create a pull request (draft) for the current branch:

```bash
jit push
```

To skip the draft stage and create a live pull request, use the `--yolo` flag:

```bash
jit push --yolo
```

### Viewing Welcome Message

To view the welcome message and get started:

```bash
jit welcome
```

## Uninstallation

```bash
pip uninstall jit-cli
```

# Roadmap

- [x] ~~Add mark as draft feature~~ Mark PRs as draft by default and add flag to bypass 📝
- [x] Add PR template compatibility 🧑‍🍳
- [x] Make installable using a package manger (no more cloning 🎉)
- [ ] Add tests 🧪
- More to come! 🏃

## Contributing

Contributions to **jit** are welcome! Please refer to the CONTRIBUTING.md file for more details on how to submit pull requests, report issues, or make feature suggestions.
