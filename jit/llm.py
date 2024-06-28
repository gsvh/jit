from langchain_community.chat_models import ChatOllama
from langchain_core.messages import HumanMessage


local_llm = "llama3"
diff_summary_llm = ChatOllama(model=local_llm, json=True, temperature=0)
pr_description_llm = ChatOllama(model=local_llm, json=True, temperature=0)

pr_template = """
## Description
{a brief overview of the changes}

## Changes
{a list of the changes made}
"""

def generate_diff_summary(diff):
    print("Getting the diff summary")
    prompt = f'Your job is to give summaries of code changes. You will recieve the one diff. Only respond with the summary of the diff. Nothing else. Please summarize the following diff:\n{diff}'
    response = diff_summary_llm.invoke([HumanMessage(content=prompt)])
    return response.content

def generate_pr_description(commit_messages, diffs):
    print("Getting the PR description")
    diff_descriptions = []
    for diff in diffs:
        diff_descriptions += generate_diff_summary(diff)
    
    prompt = f'Your job is to generate a PR description based on the commit messages and diffs. You will recieve the commit messages and diffs. Only respond with the PR description. Nothing else. Please summarize the following commit messages:\n{commit_messages}\nPlease summarize the following diffs:\n{diff_descriptions} \nThe PR template is as follows:\n{pr_template}'
    response = pr_description_llm.invoke([HumanMessage(content=prompt)])
    return response.content

