

def join_by_newline(items):
    return '\n'.join(items)
def join_by_newline_tab(items):
    return '\t'+'\n\t'.join(items)


def get_generate_diff_summary_prompt(diff):
    return '\n'.join((
        'Your job is to give summaries of code changes. You will receive the one diff. Include valuable information, such as the type of change and file name.',
        f'Only respond with the summary of the diff. Nothing else. Please summarize the following diff:\n{diff}'
    ))

def get_generate_pr_description_prompt(commit_messages, diff_descriptions, pr_template):
    return '\n'.join((
        '---'
        'commit messages:',
        f'{join_by_newline_tab(commit_messages)}'
        '\ndiffs summaries',
        f'{join_by_newline_tab(diff_descriptions)}'
        '\npr template:',
        f'{pr_template}',
        '---',
        'Your job is to generate a PR description, here are some more details:',
        '- Generate a concise PR description based only on the commit messages and summaries of the diffs.',
        '- IMPORTANT: follow the PR template. Include all elements mentioned in the PR template.',
        '- IMPORTANT: Only respond with the PR description. Nothing else. Not even a "Here is a generated PR description" message. Respond with the PR description ONLY.',
        
    ))

