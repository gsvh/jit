from .llm import generate_pr_description
import subprocess
import json

def branch_is_behind(repo):
    # Check if the current branch is behind the remote
    behind = repo.git.rev_list('--left-right', 'origin/develop...HEAD', '--count')
    behind_count = int(behind.split()[0])
    print(behind)
    if behind_count > 0:
        print(f'Current branch is behind the remote by {behind_count} commits.')
        return True
    return False
    

def parse_diffs(diffs):
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
    
    return individual_diffs


def generate_pr(repo):
    
    print('Getting the latest commits on the current branch...')
    # Get latest commits on the current branch vs main/master
    commits = list(repo.iter_commits('develop..HEAD'))
    commit_messages = [commit.message for commit in commits]

    print('Number of commits:', len(commit_messages))
    
    print('Getting the diffs between the current branch and develop...')
    # Get diffs
    diffs = parse_diffs(repo.git.diff('develop', 'HEAD'))
    print('Number of diffs:', len(diffs))
    
    # Generate PR description
    pr_description = generate_pr_description(commit_messages, diffs)
        
    return pr_description



def create_pull_request_via_cli(owner, repo, title, body, head_branch, base_branch):
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
        print("Pull request created successfully.")
        try:
            response = json.loads(result.stdout)
            return response['url']
        except (json.JSONDecodeError, KeyError):
            return 'Failed to parse response.'
    else:
        print("Failed to create pull request.")
        return ''
