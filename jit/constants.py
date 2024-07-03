import os

JIT_DIR = os.path.join(os.environ['HOME'], '.jit')
CONFIG_FILE_PATH = os.path.join(JIT_DIR, 'config.yaml')


PR_TEMPLATE = """
## Description
{a brief overview of the changes}

## Changes
* {a list of the changes made}
"""

# https://github.com/angular/angular.js/blob/master/DEVELOPERS.md#type
COMMIT_MESSAGE_SPECIFICATION = """Template:
Template:
`<type>(<scope>): <subject>` or `<type>: <subject>`

Specifications:
- `scope` (optional): Specifies the place of the commit, e.g.,$file_name, $location, $browser.
- `subject`: Describes the change using:
  - Imperative mood: "change", not "changed" or "changes".
  - Lowercase initial letter.
  - No period (.) at the end.
"""