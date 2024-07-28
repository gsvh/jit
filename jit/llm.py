import logging
from typing import Literal, TypedDict

import ollama

from .prompts import (get_generate_diff_summary_prompt,
                      get_generate_pr_description_prompt)

log = logging.getLogger("rich")

class Message(TypedDict):
    role: Literal['assistant', 'user']
    content: str

class Response(TypedDict):
    model: str
    created_at: str
    message: Message
    done_reason: str
    done: bool
    total_duration: int
    load_duration: int
    prompt_eval_count: int
    prompt_eval_duration: int
    eval_count: int
    eval_duration: int

def generate_diff_summary(diff):
    log.debug("Getting the diff summary...")
    prompt = get_generate_diff_summary_prompt(diff)
    log.debug(f'Prompt: {prompt}')
    response: Response = ollama.chat(model='llama3', messages=[{'role': 'user', 'content': prompt}])
    return response['message']['content']

def generate_pr_description(commit_messages, diffs, pr_template):
    log.debug("Generating the PR description...")
    diff_descriptions = []
    for index, diff in enumerate(diffs):
        log.info(f'Summarizing diff {index + 1}/{len(diffs)}')
        current_diff_summary = generate_diff_summary(diff)
        log.debug(f'Summary of diff {index + 1}: {current_diff_summary}')
        diff_descriptions.append(current_diff_summary)

    prompt = get_generate_pr_description_prompt(commit_messages, diff_descriptions, pr_template)
    log.debug(f'Prompt: {prompt}')
    log.info('Generating the PR description')
    response: Response = ollama.chat(model='llama3', messages=[{'role': 'user', 'content': prompt}])
    return response['message']['content']