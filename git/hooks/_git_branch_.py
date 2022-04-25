import re

__REGEX_BRANCH_NAME__ = "^([a-zA-Z0-9]+)/(.+)"
__INDEX_BRANCH_TYPE__ = 1
__INDEX_BRANCH_DESC__ = 2


class GitBranch:
    def __init__(
            self,
            branch_type: str | None = None,
            branch_desc: str | None = None
    ):
        self._branch_type = branch_type
        self._branch_desc = branch_desc

    @property
    def commit_type(self):
        return self._branch_type

    @property
    def commit_desc(self):
        return re.sub("[-_]+", " ", self._branch_desc)


def parse_git_branch(branch_name) -> GitBranch:
    matches = re.match(__REGEX_BRANCH_NAME__, branch_name)
    if matches:
        return GitBranch(
            branch_type=matches[__INDEX_BRANCH_TYPE__],
            branch_desc=matches[__INDEX_BRANCH_DESC__],
        )
    else:
        return GitBranch()
