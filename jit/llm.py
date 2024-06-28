import logging
from langchain_community.chat_models import ChatOllama
from langchain_core.messages import HumanMessage
log = logging.getLogger("rich")

local_llm = "llama3"
diff_summary_llm = ChatOllama(model=local_llm, json=True, temperature=0)
pr_description_llm = ChatOllama(model=local_llm, json=True, temperature=0)

pr_template = """
## Description
{a brief overview of the changes}

## Changes
* {a list of the changes made}
"""

def generate_diff_summary(diff):
    log.debug("Getting the diff summary...")
    prompt = f'Your job is to give summaries of code changes. You will receive the one diff. Only respond with the summary of the diff. Nothing else. Please summarize the following diff:\n{diff}'
    response = diff_summary_llm.invoke([HumanMessage(content=prompt)])
    return response.content

def generate_pr_description(commit_messages, diffs):
    log.debug("Generating the PR description...")
    diff_descriptions = []
    for index, diff in enumerate(diffs):
        log.info(f'Summarizing diff {index + 1}/{len(diffs)}')
        diff_descriptions.append(generate_diff_summary(diff))
    
    prompt = f'Your job is to generate a PR description based on the commit messages and diffs. You will receive the commit messages and summaries of the diffs. Here are the commit messages:\n```\n{commit_messages}\n```\nAnd here are the diffs summaries:\n```\n{diff_descriptions}\n```\nThe PR template is as follows:\n```\n{pr_template}\n```\nOnly respond with the PR description. Nothing else, not even a "Here is the PR description" message. Respond with the PR description ONLY.'
    log.info('Generating the PR description')
    response = pr_description_llm.invoke([HumanMessage(content=prompt)])
    return response.content