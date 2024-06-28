import click
import git
import os
from .config import OWNER, BASE_BRANCH
from .utils import branch_is_behind, create_pull_request_via_cli, generate_pr

@click.group()
def jit():
    """Jit - A tool to automate PR descriptions."""
    pass

@jit.command()
@click.option('--dry', is_flag=True)
def push(dry):
    """Create a PR for the current branch."""
     # Determine the repository directory (assuming current directory for simplicity)
    repo_path = os.getcwd()
    repo = git.Repo(repo_path)
    repo_name = repo.remotes.origin.url.split('/')[-1].replace('.git', '')
    branch_name = repo.active_branch.name

    print(f'Fetching the latest changes for {repo_name}...')
    # First run git fetch to ensure we have the latest changes
    repo.git.fetch()

    # Check if the current branch is behind the remote
    if branch_is_behind(repo):
        print('Please pull the latest changes before pushing.')
        return

    # Push the current branch to the remote
    print('Pushing the current branch...')
    # repo.git.push('--set-upstream', 'origin', repo.active_branch.name)
    
    # Generate PR description
    pr_description = "DEMO"
    # pr_description = generate_pr(repo)
    print('PR Description:', pr_description)
    
    # Create the PR
    if not dry:
        owner = OWNER
        repo = repo_name
        title = branch_name
        body = pr_description
        head_branch = branch_name
        base_branch = BASE_BRANCH
        
        pr_link = 'LINK'
        # pr_link = create_pull_request_via_cli(owner, repo, title, body, head_branch, base_branch)    
        print('PR Link:', pr_link)
    

if __name__ == "__main__":
    jit()