import logging
import os
import shutil
import subprocess

import click
import git
from rich.logging import RichHandler

from .utils import (banner, branch_is_behind, check_github_cli_installed,
                    check_model_downloaded, create_pull_request_via_cli,
                    download_model, ensure_directory_and_config, generate_pr,
                    get_repo_config, update_config)

FORMAT = "%(message)s"





@click.group()
@click.option('--debug', is_flag=True, help="Enable debug logging.")
def jit(debug):
    """jit - A tool to automate PRs."""
    if debug:
        logging.basicConfig(level=logging.DEBUG, format=FORMAT, datefmt="[%X]", handlers=[RichHandler()])
    else:
        logging.basicConfig(level=logging.INFO, format=FORMAT, datefmt="[%X]", handlers=[RichHandler()])
    if check_model_downloaded("llama3"):
        logging.debug("Model llama3 is downloaded.")
    else:
        logging.warning("Model llama3 is not downloaded. Please download the model before proceeding.")
        logging.info("Run the following command to download the model: jit pull-model")
        exit(1)
    check_github_cli_installed()

@jit.command()
@click.option('--dry', is_flag=True, help="Run the command without creating the PR.")
@click.option('--yolo', is_flag=True, help="Doesn't mark the PR as draft.")
def push(dry, yolo):
    """Create a PR for the current branch."""
    log = logging.getLogger("rich")
    log.debug("Starting the push command...")

    # Get the repo name and branch name
    repo_path = os.getcwd()
    repo = git.Repo(repo_path)
    repo_name = repo.remotes.origin.url.split('/')[-1].replace('.git', '')
    branch_name = repo.active_branch.name

    # Ensure the config directory and yaml file exists
    ensure_directory_and_config()
    # Check if the repo's configuration exists
    owner, base_branch = get_repo_config(repo_name)
    if not owner or not base_branch:
        owner, base_branch = update_config(repo_name)

    log.info(f'Fetching the latest changes for {repo_name}...')
    repo.git.fetch()

    if branch_is_behind(repo, base_branch, dry):
        log.warning('Please pull the latest changes before pushing.')
        return
    
    pr_description = generate_pr(repo, base_branch)

    if not dry:
        log.info('Pushing the current branch...')
        repo.git.push('--set-upstream', 'origin', repo.active_branch.name)  
    
    if dry: 
        log.info('PR Description: {}'.format(pr_description))
    else: 
        log.debug('PR Description: {}'.format(pr_description))
    
    if not dry:
        repo = repo_name
        title = branch_name
        body = pr_description
        head_branch = branch_name
        
        pr_link = create_pull_request_via_cli(owner, repo, title, body, head_branch, base_branch, yolo)
        log.info('PR Link: {}'.format(pr_link))

@jit.command()
def welcome():
    """Shows the welcome banner."""
    banner()

@jit.command()
@click.option('--repo_name', default=None, help="The name of the repository.")
def config(repo_name):
    """Update the repository configuration."""
    if not repo_name:
      # Get the repo name 
        repo_path = os.getcwd()
        repo = git.Repo(repo_path)
        repo_name = repo.remotes.origin.url.split('/')[-1].replace('.git', '')
    update_config(repo_name)

@jit.command()
def pull_model():
    """Pull the llama3 model."""
    log = logging.getLogger("rich")
    if check_model_downloaded("llama3"):
        logging.debug("Model llama3 is already downloaded.")
        exit(0)
    else: 
        log.info("Downloading the llama3 model...")
        download_model("llama3")
    