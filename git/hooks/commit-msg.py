#!python
import sys
from subprocess import check_output

from _const_ import COMMIT_TYPE_MAPPING, EXPECTED_COMMIT_TYPES, USAGE_COMMIT_TEMPLATE
from _git_branch_ import parse_git_branch, GitBranch
from _git_commit_msg_ import parse_git_commit_msg, GitCommitMessage


def validate_and_build_commit_message(
        commit_message: GitCommitMessage,
        branch: GitBranch
) -> str:
    message_data = []
    # commit_type
    commit_type = commit_message.commit_type
    if not commit_type:
        commit_type = branch.commit_type

    if not commit_type:
        raise Exception(f"Error: commit-type should not empty!\n{USAGE_COMMIT_TEMPLATE}")
    commit_type = commit_type.lower().strip()
    commit_type = COMMIT_TYPE_MAPPING.get(commit_type, commit_type)
    if commit_type not in EXPECTED_COMMIT_TYPES:
        raise Exception(f"Error: unexpected commit-type!\n{USAGE_COMMIT_TEMPLATE}")

    # commit description
    commit_desc = commit_message.commit_desc

    if not commit_desc or len(commit_desc) == 0:
        commit_desc = branch.commit_desc

    if not commit_desc or len(commit_desc) < 3:
        raise Exception(f"Error: invalid commit-description {commit_desc}\n{USAGE_COMMIT_TEMPLATE}")
    else:
        commit_desc = commit_desc.strip()

    # first line
    commit_scope = commit_message.commit_scope
    if commit_scope:
        message_data.append(f"{commit_type}(${commit_scope.strip()}): {commit_desc}")
    else:
        message_data.append(f"{commit_type}: {commit_desc}")

    # body
    if commit_message.commit_body:
        message_data.append(commit_message.commit_body)

    # footers
    if commit_message.commit_footers:
        message_data.append(commit_message.commit_footers)

    # build commit message
    return "\n".join(message_data)


# Collect commit message file from parameters
commit_msg_filepath = sys.argv[1]
# commit message data
with open(commit_msg_filepath, "rt") as fs:
    commit_msg_data = fs.readlines()
    fs.close()
git_commit_message = parse_git_commit_msg(commit_msg_data)
# current branch name
branch_name = check_output(['git', 'symbolic-ref', '--short', 'HEAD']) \
    .decode("utf-8") \
    .strip()
print(f"branch: <{branch_name}>")

if branch_name == "master":
    raise Exception("Error: cannot commit directly to master, please create PR instead!!!")
git_branch = parse_git_branch(branch_name)

# validate and build new commit message
new_commit_message = validate_and_build_commit_message(git_commit_message, git_branch)
print(f'commit message: <{new_commit_message}>')

with open(commit_msg_filepath, 'wt') as fs:
    fs.write(new_commit_message)
    fs.flush()
    fs.close()
