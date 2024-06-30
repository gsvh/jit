.PHONY: setup check_deps install_mac_deps install_jit develop

## setup: Set up the project.
setup: check_deps install_jit

## develop: Set up the project for development with editable install.
develop: check_deps install_jit_editable

## check_deps: Check for system dependencies like pip, GitHub CLI, and Ollama.
check_deps:
	@bash scripts/check_dependencies.sh


## install_jit: Install the jit package.
install_jit:
	@echo "Installing jit"
	@pip install .
	@echo "jit installed successfully"
	@jit welcome

## install_jit_editable: Install the jit package in editable mode.
install_jit_editable:
	@echo "Installing jit in editable mode"
	@pip install --editable .
	@echo "jit installed successfully in editable mode"
	@jit welcome


## uninstall_jit: Uninstall the jit package.
uninstall_jit:
	@echo "Uninstalling jit"
	@bash scripts/uninstall.sh
	@echo "jit uninstalled successfully"