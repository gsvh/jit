import click
import git
import os
import logging
from .config import OWNER, BASE_BRANCH
from .utils import branch_is_behind, create_pull_request_via_cli, generate_pr
from rich.logging import RichHandler

FORMAT = "%(message)s"




@click.group()
def jit():
    """Jit - A tool to automate PRs."""
    pass

@jit.command()
@click.option('--dry', is_flag=True, help="Run the command without creating the PR.")
@click.option('--debug', is_flag=True, help="Enable debug logging.")
def push(dry, debug):
    """Create a PR for the current branch."""
    if debug:
        logging.basicConfig(level=logging.DEBUG, format=FORMAT, datefmt="[%X]", handlers=[RichHandler()])
    else:
        logging.basicConfig(level=logging.INFO, format=FORMAT, datefmt="[%X]", handlers=[RichHandler()])
    
    log = logging.getLogger("rich")

    log.debug("Starting the push command...")
    repo_path = os.getcwd()
    repo = git.Repo(repo_path)
    repo_name = repo.remotes.origin.url.split('/')[-1].replace('.git', '')
    branch_name = repo.active_branch.name

    log.info(f'Fetching the latest changes for {repo_name}...')
    repo.git.fetch()

    if branch_is_behind(repo, dry):
        log.warning('Please pull the latest changes before pushing.')
        return

    if not dry:
        log.info('Pushing the current branch...')
        repo.git.push('--set-upstream', 'origin', repo.active_branch.name)  
    
    pr_description = generate_pr(repo)
    
    if dry: 
        log.info('PR Description: {}'.format(pr_description))
    else: 
        log.debug('PR Description: {}'.format(pr_description))
    
    if not dry:
        owner = OWNER
        repo = repo_name
        title = branch_name
        body = pr_description
        head_branch = branch_name
        base_branch = BASE_BRANCH
        
        pr_link = create_pull_request_via_cli(owner, repo, title, body, head_branch, base_branch)
        log.info('PR Link: {}'.format(pr_link))
