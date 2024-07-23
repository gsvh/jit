import os

JIT_DIR = os.path.join(os.environ['HOME'], '.jit')
CONFIG_FILE_PATH = os.path.join(JIT_DIR, 'config.yaml')


DEFAULT_PR_TEMPLATE = """
## Description
{a brief overview of the changes}

## Changes
* {a list of the changes made}
"""
