#!/bin/bash

echo "Setting global jit dir environment variable"
# Get the current directory
CURRENT_DIR=$(pwd)

# Define the variable name
JIT_DIR="JIT_DIR"

# Check the operating system to determine the shell configuration file
if [ "$(uname)" == "Darwin" ]; then
    # macOS
    CONFIG_FILE="$HOME/.zshrc"
elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
    # Linux
    CONFIG_FILE="$HOME/.zshrc"
elif [ "$(expr substr $(uname -s) 1 10)" == "MINGW32_NT" ]; then
    # Windows
    CONFIG_FILE="$HOME/.bashrc"
else
    echo "Unsupported operating system."
    exit 1
fi

# Check if Oh My Zsh is installed
if [ -d "$HOME/.oh-my-zsh" ]; then
    # Oh My Zsh is installed, switch to it
    echo "Oh My Zsh is installed. Switching to zsh script..."
    zsh "$CURRENT_DIR/scripts/set_dir_env_zsh.sh" 
    exit
else
    # Oh My Zsh is not installed
    echo "Oh My Zsh is not installed. continuing..."
    # You can choose to install it or take other actions here
fi

echo "HERE!"
# Check if the variable is already defined in the shell configuration file
if grep -q "$JIT_DIR=" "$CONFIG_FILE"; then
    # If the variable is already defined, update its value
    sed -i "s|^$JIT_DIR=.*|$JIT_DIR=$CURRENT_DIR|" "$CONFIG_FILE"
else  
    # If the variable is not defined, add it to the file & export the variable
    echo "$JIT_DIR=$CURRENT_DIR" >> "$CONFIG_FILE"
    # Export the variable (only for Linux and macOS)
    if [ "$(expr substr $(uname -s) 1 5)" != "MINGW" ]; then
        echo "export $JIT_DIR" >> "$CONFIG_FILE"
    fi
fi

# Source the configuration file to apply changes (only for Linux and macOS)
if [ "$(expr substr $(uname -s) 1 5)" != "MINGW" ]; then
    source "$CONFIG_FILE"
fi

echo "jit install directory has been stored as $JIT_DIR."
