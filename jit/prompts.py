from .constants import COMMIT_MESSAGE_SPECIFICATION, PR_TEMPLATE


def join_by_newline(items):
    return '\n'.join(items)


def get_generate_diff_summary_prompt(diff):
    return f'Your job is to give summaries of code changes. You will receive the one diff. Include valuable information, such as the type of change and file name. Only respond with the summary of the diff. Nothing else. Please summarize the following diff:\n{diff}'

def get_generate_commit_message_prompt(diffs, commit_type):
    return (
        f"Generate a detailed and specific commit message that concisely summarizes the changes shown in the diffs. "
        f"Commit type: {commit_type}.\n"
        f"Here are the diffs:\n"
        f"```\n{join_by_newline(diffs)}\n```\n"
        f"Follow these commit message specifications:\n"
        f"```\n{COMMIT_MESSAGE_SPECIFICATION}\n```\n"
        "Ensure the message captures all key changes. Respond with the commit message ONLY."
    )

def get_generate_pr_description_prompt(commit_messages, diff_descriptions):
    return f'Your job is to generate a PR description based on the commit messages and diffs. You will receive the commit messages and summaries of the diffs. Here are the commit messages:\n```\n{join_by_newline(commit_messages)}\n```\nAnd here are the diffs summaries:\n```\n{join_by_newline(diff_descriptions)}\n```\nThe PR template is as follows:\n```\n{PR_TEMPLATE}\n```\nOnly respond with the PR description. Nothing else, not even a "Here is the PR description" message. Respond with the PR description ONLY.'