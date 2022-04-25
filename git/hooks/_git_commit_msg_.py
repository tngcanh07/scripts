import re

__REGEX_MSG_HEADER__ = r"^(([a-zA-Z0-9]+)(\((.+)\))?:)?(.+)$"
__INDEX_MSG_HEADER_TYPE__ = 2
__INDEX_MSG_HEADER_SCOPE__ = 4
__INDEX_MSG_HEADER_DESC__ = 5


class GitCommitMessage:
    def __init__(
            self,
            commit_type: str | None = None,
            commit_scope: str | None = None,
            commit_desc: str | None = None,
            commit_body: str | None = None,
            commit_footers: str | None = None,
    ):
        self.commit_type = commit_type
        self.commit_scope = commit_scope
        self.commit_desc = commit_desc
        self.commit_body = commit_body
        self.commit_footers = commit_footers


def parse_git_commit_msg(commit_msg: list[str]) -> GitCommitMessage:
    count = len(commit_msg)
    if count == 0:
        return GitCommitMessage()
    header = re.match(__REGEX_MSG_HEADER__, commit_msg[0])
    if not header:
        return GitCommitMessage()
    commit_body = "\n".join(commit_msg[1: len(commit_msg)])
    commit_footers = None
    return GitCommitMessage(
        commit_type=header[__INDEX_MSG_HEADER_TYPE__],
        commit_scope=header[__INDEX_MSG_HEADER_SCOPE__],
        commit_desc=header[__INDEX_MSG_HEADER_DESC__],
        commit_body=commit_body,
        commit_footers=commit_footers,
    )
