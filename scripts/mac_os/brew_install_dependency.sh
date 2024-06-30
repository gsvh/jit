#!/bin/bash

# General approach to install a tool
install_tool() {
    echo "Installing $1..."
    brew install $1
}

# Install specific tool based on passed argument
TOOL=$1
if [ -n "$TOOL" ]; then
    install_tool $TOOL
else
    echo "No tool specified for installation."
    exit 1
fi