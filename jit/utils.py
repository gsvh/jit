import json
import logging
import os
import subprocess
import sys

import yaml

from .constants import CONFIG_FILE_PATH, JIT_DIR
from .llm import generate_commit_message, generate_pr_description

log = logging.getLogger("rich")


def make_bold(text):
    return f"\033[1m{text}\033[0m"
def make_italic(text):
    return f"\033[3m{text}\033[0m"
def make_purple(text):
    return f"\033[0;35m{text}\033[0m"

def banner():

    jit = """

     ██╗██╗████████╗
     ██║██║╚══██╔══╝
     ██║██║   ██║   
██   ██║██║   ██║   
╚█████╔╝██║   ██║   
 ╚════╝ ╚═╝   ╚═╝   
                    
    """
    jit = make_purple(jit)

    jit_lines = jit.split("\n")
    # Attempt to get terminal size, with a fallback
    try:
        terminal_width = os.get_terminal_size().columns
    except OSError:
        terminal_width = 80  # Fallback width
    banner_width = int(terminal_width / 2)
    if banner_width < 50:
        banner_width = 50
    for line in jit_lines:
        print(line.center(banner_width))

    welcome_message = """
Welcome to {bold_jit}! A tool to automate pull requests.

Here are all of the pre-requisites to have in place before you can use {bold_jit}:

\t{purple_square} You must have the GitHub CLI installed.
\t{purple_square} You must be logged in to the GitHub CLI.
\t{purple_square} You must have Ollama installed.
\t{purple_square} You must have pulled llama3 using Ollama.


{bold_jit} is intended to be used alongside {bold_git}. 
Once you have finished making changes to your branch and you have committed them, 
instead of doing {purple_git_push} to push your work to the remote, you can use {purple_jit_push} and {bold_jit} will then:

\t{purple_bullet} Check if the current branch is behind the remote.
\t{purple_bullet} Generate a PR description based on the commits and diffs.
\t{purple_bullet} Push the current branch to the remote.
\t{purple_bullet} Create a PR on GitHub and return the PR URL.

You can also use {purple_push_dry} to only create the PR description without pushing or creating the pull request.
\t* Note that the PR description will be regenerated when you run {purple_jit_push} without the {purple_dry} flag.

A config file will be created in {purple_config_path} to store the owner and base branch of each of the repositories you use {bold_jit} with.


Use {purple_help} to see all available commands.

Go on now, {italic_jit}!

""".format(
    bold_jit=make_bold("jit"), 
    purple_square=make_purple("□"),
    bold_git=make_bold("git"), 
    purple_git_push=(make_purple("git push")), 
    purple_jit_push=(make_purple("jit push")),
    purple_bullet=make_purple("•"),
    purple_push_dry=make_purple("jit push --dry"),
    purple_dry=make_purple("--dry"),
    purple_config_path=make_purple('~/.jit/config.yaml'),
    purple_help=make_purple("jit --help"),
    italic_jit=make_italic("jit")
    )
    welcome_message_lines = welcome_message.split("\n")
    for line in welcome_message_lines:
        print(f"{line}")



def get_repo_config(repo_name):
    """Gets the repository's configuration if it already exists in the config file."""
    ensure_directory_and_config()
    
    # Load the existing config data
    try:
        with open(CONFIG_FILE_PATH, 'r') as config_file:
            config = yaml.safe_load(config_file) or {}
    except FileNotFoundError:
        config = {}

    # Check if the repository is already configured
    if repo_name in config:
        log.debug(f"Configuration already exists for {repo_name}:")
        log.debug(f"Owner: {config[repo_name]['owner']}")
        log.debug(f"Base Branch: {config[repo_name]['base_branch']}")
        return (config[repo_name]['owner'], config[repo_name]['base_branch'])
    else:
        log.info(f"No existing configuration found for {repo_name}.")
        return (None, None)

def ensure_directory_and_config():
    """Ensures that the directory and config file exists."""
    if not os.path.exists(JIT_DIR):
        os.makedirs(JIT_DIR)
        log.debug(f"Created directory at {JIT_DIR}")
    if not os.path.isfile(CONFIG_FILE_PATH):
        with open(CONFIG_FILE_PATH, 'w') as config_file:
            yaml.dump({}, config_file)
        log.debug(f"Created config file at {CONFIG_FILE_PATH}")
    

def update_config(repo_name):
    """Updates the configuration file with the repository's owner and base branch."""
    ensure_directory_and_config()
    current_owner, current_base_branch = get_repo_config(repo_name)
    owner = input("\tEnter the repository's {purple_owner} (current: {current_owner_or_unset}): ".format(
        purple_owner=make_purple("owner"),
        current_owner_or_unset=current_owner if current_owner else 'Unset'
    ))
    base_branch = input("\tThe {purple_base_branch} is the branch that the pull request will be made to.\n\tEnter the repository's {purple_base_branch} (current: {current_branch_or_unset}): ".format(
        purple_base_branch=make_purple("base branch"),
        current_branch_or_unset=current_base_branch if current_base_branch else 'Unset'
    ))

    # Load the existing config data and update it
    with open(CONFIG_FILE_PATH, 'r') as config_file:
        config = yaml.safe_load(config_file) or {}
    config[repo_name] = {'owner': owner, 'base_branch': base_branch}

    # Write the updated configuration back to the file
    with open(CONFIG_FILE_PATH, 'w') as config_file:
        yaml.dump(config, config_file, default_flow_style=False, sort_keys=False)
    log.info(f"Updated configuration for {repo_name} in {CONFIG_FILE_PATH}.")
    return (owner, base_branch)


def branch_is_behind(repo, base_branch, dry):
    log.info("Checking if the current branch is behind the remote...")
    behind = repo.git.rev_list('--left-right', f'origin/{base_branch}...HEAD', '--count')
    behind_count = int(behind.split()[0])
    if behind_count > 0:
        log.warning(f'Current branch is behind the remote by {behind_count} commits.')
        
        # If ran in dry mode, don't return True
        if not dry:
            return True
        else:
            return False

    log.info("Current branch is up-to-date with the remote.")
    return False

def parse_diffs(diffs):
    log.debug("Parsing diffs...")
    diff_list = diffs.split('\n')
    individual_diffs = []
    current_diff = []
    
    for line in diff_list:
        if line.startswith('diff --git'):
            if current_diff:
                individual_diffs.append('\n'.join(current_diff))
                current_diff = []
        current_diff.append(line)
    
    if current_diff:
        individual_diffs.append('\n'.join(current_diff))
    
    log.debug(f"Parsed {len(individual_diffs)} diffs.")
    return individual_diffs


def get_staged_diffs(repo):
    log.info('Finding the staged diffs...')
    raw_staged_diffs = repo.git.diff("HEAD", "--staged" )
    diffs = parse_diffs(raw_staged_diffs)
    log.info(f'Number of diffs found: {len(diffs)}')
    return diffs
   


def generate_commit(repo, commit_type):
    log.debug("Generating the commit message...")
    
    diffs = get_staged_diffs(repo)
    if not diffs:
        log.error("No changes found to commit.")
        sys.exit(1)
    
    commit_message = generate_commit_message(diffs, commit_type)
    return commit_message


def generate_pr(repo, base_branch):
    log.info('Finding the latest commits from the current branch...')
    commits = list(repo.iter_commits(f'{base_branch}...HEAD'))
    if not commits:
        log.error('No commits found from the current branch.')
        sys.exit(1)

    log.info(f'Number of commits found: {len(commits)}')
    commit_messages = [commit.message for commit in commits]
    
    log.info(f'Finding diffs between the current branch and {base_branch}...')
    diffs = parse_diffs(repo.git.diff(base_branch, 'HEAD'))
    log.info(f'Number of diffs found: {len(diffs)}')
    
    pr_description = generate_pr_description(commit_messages, diffs)
    log.info('Generated PR description successfully.')
    return pr_description


def create_pull_request_via_cli(owner, repo, title, body, head_branch, base_branch):
    log.info("Creating a pull request via GitHub CLI...")
    command = [
        "gh", "api",
        "--method", "POST",
        "-H", "Accept: application/vnd.github+json",
        "-H", "X-GitHub-Api-Version: 2022-11-28",
        f"/repos/{owner}/{repo}/pulls",
        "-f", f"title={title}",
        "-f", f"body={body}",
        "-f", f"head={head_branch}",
        "-f", f"base={base_branch}"
    ]
    
    result = subprocess.run(command, text=True, capture_output=True)
    if result.returncode == 0:
        log.info("Pull request created successfully.")
        try:
            response = json.loads(result.stdout)
            log.debug(f"Pull request URL: {response['html_url']}")
            return response['html_url']
        except (json.JSONDecodeError, KeyError) as e:
            log.error("Failed to parse response from GitHub API.")
            log.debug(e)
            return 'Failed to parse response.'
    else:
        log.error("Failed to create pull request.")
        log.debug(result.stderr)
        return ''