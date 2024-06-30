#!/bin/bash

# Function to uninstall Homebrew dependencies with confirmation
uninstall_brew_deps() {
    read -p "Do you want to uninstall GitHub CLI? [y/n]: " uninstall_gh
    if [ "$uninstall_gh" = "y" ]; then
        brew uninstall gh
    fi

    read -p "Do you want to uninstall Ollama? [y/n]: " uninstall_ollama
    if [ "$uninstall_ollama" = "y" ]; then
        brew uninstall ollama
    fi
}

# Function to uninstall pip3 dependencies with options
uninstall_pip3_deps() {
    echo "Listing pip3 dependencies from requirements.txt:"
    echo "--------------------"
    cat requirements.txt
    echo ""
    echo "--------------------"
    read -p "Do you want to uninstall all pip3 dependencies? [y/n/a (ask for each)]: " resp
    if [ "$resp" = "y" ]; then
        pip3 uninstall -y -r requirements.txt
    elif [ "$resp" = "a" ]; then
        while read dep; do
            read -p "Do you want to uninstall $dep? [y/n]: " uninstall_dep
            if [ "$uninstall_dep" = "y" ]; then
                pip3 uninstall -y $dep
            fi
        done < requirements.txt
    fi
}

# Uninstall process
echo "Starting the uninstallation process..."
uninstall_brew_deps
uninstall_pip3_deps
echo "Uninstalling jit..."
pip3 uninstall -y jit
echo "Uninstallation process completed."