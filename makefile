.PHONY: setup check_deps install_mac_deps install_jit develop

## setup: Set up the project.
setup: check_deps install_jit welcome

## re-install: reinstall the project without the welcome banner
re-install: check_deps install_jit

## develop: Set up the project for development with editable install.
develop: check_deps install_jit_editable welcome

## check_deps: Check for system dependencies like pip3, GitHub CLI, and Ollama.
check_deps:
	@bash scripts/check_dependencies.sh

## welcome banner
welcome:
	@jit welcome

## install_jit: Install the jit package.
install_jit:
	@echo "Installing jit"
	@pip3 install .
	@echo "jit installed successfully"

## install_jit_editable: Install the jit package in editable mode.
install_jit_editable:
	@echo "Installing jit in editable mode"
	@pip3 install --editable .
	@echo "jit installed successfully in editable mode"


## uninstall_jit: Uninstall the jit package.
uninstall:
	@echo "Uninstalling jit"
	@bash scripts/uninstall.sh
	@echo "jit uninstalled successfully"