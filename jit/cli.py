import logging
import os
import shutil
import subprocess

import click
import git
from rich.logging import RichHandler

from .utils import (banner, branch_is_behind, create_pull_request_via_cli,
                    ensure_directory_and_config, generate_pr, get_repo_config,
                    update_config)

FORMAT = "%(message)s"





@click.group()
@click.option('--debug', is_flag=True, help="Enable debug logging.")
def jit(debug):
    """jit - A tool to automate PRs."""
    if debug:
        logging.basicConfig(level=logging.DEBUG, format=FORMAT, datefmt="[%X]", handlers=[RichHandler()])
    else:
        logging.basicConfig(level=logging.INFO, format=FORMAT, datefmt="[%X]", handlers=[RichHandler()])

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
    logging.basicConfig(level=logging.INFO, format=FORMAT, datefmt="[%X]", handlers=[RichHandler()])
    if not repo_name:
      # Get the repo name 
        repo_path = os.getcwd()
        repo = git.Repo(repo_path)
        repo_name = repo.remotes.origin.url.split('/')[-1].replace('.git', '')
    update_config(repo_name)

@jit.command()
def update():
    """Fetch the latest changes from the repo and re-install jit."""
    logging.basicConfig(level=logging.INFO, format=FORMAT, datefmt="[%X]", handlers=[RichHandler()])
    log = logging.getLogger("rich")

    # Capture the original working directory
    original_dir = os.getcwd()

    # Get the JIT_DIR environment variable
    repo_path = os.getenv('JIT_DIR')
    
    if not repo_path:
        log.error("JIT_DIR environment variable is not set.")
        return

    try:
        os.chdir(repo_path)
        repo = git.Repo(repo_path)
        branch = repo.active_branch

        log.info(f"Current branch: {branch.name}")

        # Check if the branch has an upstream set
        if not branch.tracking_branch():
            # Set upstream to the default remote branch (origin/main or origin/master)
            try:
                remote_branch = repo.remotes.origin.refs.main
            except AttributeError:
                remote_branch = repo.remotes.origin.refs.master

            log.info(f"Setting upstream to {remote_branch}")
            repo.git.branch('--set-upstream-to', remote_branch, branch.name)

        # Fetch the latest changes from the remote
        repo.remotes.origin.fetch()

        # Check if there are any new changes
        commits_behind = repo.iter_commits(f'{branch.name}..origin/{branch.name}')
        if not list(commits_behind):
            log.info("You are already on the latest version 🤘")
            return

        log.info("Fetching the latest changes from the branch...")
        repo.git.pull()

        log.info("Re-installing the tool using the Makefile...")
        env = os.environ.copy()
        env["COLUMNS"] = str(shutil.get_terminal_size().columns)
        env["PYTHONUNBUFFERED"] = "1"  # Ensures that Python output is not buffered
        env["FORCE_COLOR"] = "1"  # Force enable ANSI colors

        process = subprocess.Popen(
            ["make", "update"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=env  # Pass the modified environment
        )

        # Wait for the process to complete and get the return code
        return_code = process.wait()

        if return_code == 0:
            # Log stdout and stderr directly after waiting for the process to complete
            stdout, stderr = process.communicate()
            log.info(stdout)
            log.info("jit has been updated and re-installed successfully 🎉")
        else:
            # Log stderr directly after waiting for the process to complete
            stdout, stderr = process.communicate()
            log.error(stderr)
            log.error("An error occurred while updating jit.")     
    finally:
        # Change back to the original directory
        os.chdir(original_dir)

