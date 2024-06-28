from .llm import generate_pr_description
import subprocess
import json
import logging
log = logging.getLogger("rich")


def branch_is_behind(repo, dry):
    log.info("Checking if the current branch is behind the remote...")
    behind = repo.git.rev_list('--left-right', 'origin/develop...HEAD', '--count')
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


def generate_pr(repo):
    log.info('Finding the latest commits from the current branch...')
    commits = list(repo.iter_commits('develop..HEAD'))
    commit_messages = [commit.message for commit in commits]

    log.info(f'Number of commits found: {len(commit_messages)}')
    
    log.info('Finding diffs between the current branch and develop...')
    diffs = parse_diffs(repo.git.diff('develop', 'HEAD'))
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