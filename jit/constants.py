import os

JIT_DIR = os.path.join(os.environ['HOME'], '.jit')
CONFIG_FILE_PATH = os.path.join(JIT_DIR, 'config.yaml')


PR_TEMPLATE = """
## Description
{a brief overview of the changes}

## Changes
* {a list of the changes made}
"""

# https://github.com/angular/angular.js/blob/master/DEVELOPERS.md#commit-message-format
COMMIT_MESSAGE_TEMPLATE = """
<type>(<scope>): <subject>
"""

# https://github.com/angular/angular.js/blob/master/DEVELOPERS.md#type
COMMIT_MESSAGE_SPECIFICATION = """
Type
Must be one of the following:
-feat: A new feature
-fix: A bug fix
-docs: Documentation only changes
-style: Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc)
-refactor: A code change that neither fixes a bug nor adds a feature
-perf: A code change that improves performance
-test: Adding missing or correcting existing tests
-chore: Changes to the build process or auxiliary tools and libraries such as documentation generation

Scope
The scope could be anything specifying place of the commit change. For example $location, $browser, $compile, $rootScope, ngHref, ngClick, ngView, etc..

Subject
The subject contains succinct description of the change:
use the imperative, present tense: "change" not "changed" nor "changes"
don't capitalize first letter
no dot (.) at the end
"""