import logging

from langchain_community.chat_models import ChatOllama
from langchain_core.messages import HumanMessage

from .constants import (COMMIT_MESSAGE_SPECIFICATION, COMMIT_MESSAGE_TEMPLATE,
                        PR_TEMPLATE)

log = logging.getLogger("rich")

local_llm = "llama3"
commit_llm = ChatOllama(model=local_llm, json=True, temperature=0)
diff_summary_llm = ChatOllama(model=local_llm, json=True, temperature=0)
pr_description_llm = ChatOllama(model=local_llm, json=True, temperature=0)

def generate_commit_message(diffs, untracked_files_contents):
    log.debug("Generating the commit message...")
    
    # Construct the prompt parts based on available data
    if diffs:
        diffs_text = "\n".join(f"{file}:\n{diff}\n" for file, diff in diffs.items())
        prompt_diffs = f'Here are the diffs:\n```\n{diffs_text}\n```'
    else:
        prompt_diffs = ""

    if untracked_files_contents:
        untracked_files_text = "\n".join(f"{file}:\n{content}\n" for file, content in untracked_files_contents.items())
        prompt_untracked = f'Here are the contents of untracked files:\n```\n{untracked_files_text}\n```'
    else:
        prompt_untracked = ""

    # Construct the base prompt
    prompt_base = "Your job is to generate a commit message based on the information provided below."
    prompt_commit_template = f""""Here is the commit message template:\n{COMMIT_MESSAGE_TEMPLATE}\n And here is the specification: \n```\n{COMMIT_MESSAGE_SPECIFICATION}\n```\n"""
    prompt_end = "Please respond with the commit message ONLY."
    
    # Assemble the full prompt with conditional inclusion of diffs and untracked files
    prompt = f"{prompt_base}\n{prompt_diffs}\n{prompt_untracked}\n{prompt_commit_template}\n{prompt_end}"
    
    # Invoke the LLM with the prompt
    response = commit_llm.invoke([HumanMessage(content=prompt)])
    log.debug(f"Generated commit message: {response.content}")
    return response.content

def validate_commit_message(commit_message):
    log.debug("Validating the commit message...")
    if not commit_message:
        return False
    
    if commit_message.count('\n') < 1:
        return False
    
    return True


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
        current_diff_summary = generate_diff_summary(diff)
        log.debug(f'Summary of diff {index + 1}: {current_diff_summary}')
        diff_descriptions.append(current_diff_summary)
    
    prompt = f'Your job is to generate a PR description based on the commit messages and diffs. You will receive the commit messages and summaries of the diffs. Here are the commit messages:\n```\n{commit_messages}\n```\nAnd here are the diffs summaries:\n```\n{diff_descriptions}\n```\nThe PR template is as follows:\n```\n{PR_TEMPLATE}\n```\nOnly respond with the PR description. Nothing else, not even a "Here is the PR description" message. Respond with the PR description ONLY.'
    log.info('Generating the PR description')
    response = pr_description_llm.invoke([HumanMessage(content=prompt)])
    return response.content