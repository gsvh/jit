#!/bin/zsh

# Check if the variable is already defined in the shell configuration file
if grep -q "$JIT_DIR=" ~/.zshrc; then
  # If the variable is already defined, update its value
  sed "s|^$VAR_NAME=.*|$VAR_NAME=$CURRENT_DIR|" ~/.zshrc > ~/.zshrc.tmp && mv ~/.zshrc.tmp ~/.zshrc
else
  # If the variable is not defined, add it to the file & export the variable
  echo "$JIT_DIR=$CURRENT_DIR" >> ~/.zshrc
  # Export the variable
  echo "export $JIT_DIR" >> ~/.zshrc
fi

# Source the configuration file to apply changes
source ~/.zshrc

echo "jit install directory has been stored as $JIT_DIR."