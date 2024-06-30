#!/bin/bash

# Check for GitHub CLI
echo "Checking if GitHub CLI is installed"
if ! command -v gh &>/dev/null; then
    echo "GitHub CLI not installed"
    read -p "Install using Homebrew on macOS? (y/n): " choice
    if [[ "$choice" == "y" ]]; then
        make install_mac_deps TOOL=gh
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
        make install_mac_deps TOOL=ollama
        # After installation, ask to pull the model
        echo "Ollama installed. Do you want to download the llama3 model now? (y/n)"
        read model_choice
        if [[ "$model_choice" == "y" ]]; then
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

# Check for pip
if ! command -v pip &>/dev/null; then
    echo "Pip not installed."
    echo "Please install pip."
fi



