.PHONY: setup check_deps install_mac_deps install_jit

## setup: Set up the project including virtual environment and dependencies.
setup: check_deps install_jit

## check_deps: Check for system dependencies like pip, GitHub CLI, and Ollama.
check_deps:
	@bash makefile_support_scripts/check_dependencies.sh

## install_mac_deps: Install dependencies on macOS using Homebrew.
install_mac_deps:
	@echo "Attempting to install dependencies..."
	@bash makefile_support_scripts/mac_os/brew_install_dependency.sh

## install_jit: Install the jit package.
install_jit:
	@echo "Installing jit"
	@pip install .
	@echo "jit installed successfully"
	@jit welcome
