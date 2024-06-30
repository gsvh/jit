#!/bin/bash

# Check for GitHub CLI
echo "Checking if GitHub CLI is installed"
if ! command -v gh &>/dev/null; then
    echo "GitHub CLI not installed"
    read -p "Install using Homebrew on macOS? (y/n): " choice
    if [[ "$choice" == "y" ]]; then
         bash scripts/mac_os/brew_install_dependency.sh gh
    else
        echo "Please install GitHub CLI manually."
        exit 1
    fi
else
    echo "GitHub CLI installed. Nice"
fi



# Check for Ollama
if ! command -v ollama &>/dev/null; then
    echo "Ollama not installed."
    read -p "Install using Homebrew on macOS? (y/n): " choice
    if [[ "$choice" == "y" ]]; then
        bash scripts/mac_os/brew_install_dependency.sh ollama
        # After installation, ask to pull the model
        echo "Ollama installed. Do you want to download the llama3 model now? (y/n)"
        read model_choice
        if [[ "$model_choice" == "y" ]]; then
            echo "Starting Ollama"
            ollama serve
            echo "Pulling llama3 model. Strap in, this might take a while."
            ollama pull llama3
            echo "llama3 model downloaded."
        else
            echo "Please run 'ollama pull llama3' before using jit."
        fi
    else
        echo "Please install Ollama manually."
        exit 1
    fi
else
    echo "Ollama is installed."
    echo "Checking for llama3 model"
    # Use the $HOME variable to reference the user-specific model directory
    if ! [ -d "$HOME/.ollama/models/manifests/registry.ollama.ai/library/llama3" ]; then
        echo "llama3 model not found. Do you want to download it now? (y/n)"
        read model_choice
        if [[ "$model_choice" == "y" ]]; then
            ollama pull llama3
            echo "llama3 model downloaded."
        else
            echo "Please run 'ollama pull llama3' before using jit."
        fi
    else
        echo "llama3 model is downloaded. Fucking legend."
    fi
fi

# Check for pip3
if ! command -v pip3 &>/dev/null; then
    echo "pip3 not installed."
    echo "Please install pip3."
fi



