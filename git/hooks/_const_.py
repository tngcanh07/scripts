EXPECTED_COMMIT_TYPES = [
    "build",
    "ci",
    "chore",
    "docs",
    "feat",
    "fix",
    "perf",
    "refactor",
    "revert",
    "style",
    "test",
]

COMMIT_TYPE_MAPPING = {
    "feature": "feat",
    "documentations": "docs"
}

USAGE_COMMIT_TEMPLATE = f"""
Usage: commit message must follow this template:
    <type>(optional scope): <description>
    [optional body]
    [optional footer(s)]

    <type>: must be one of {EXPECTED_COMMIT_TYPES}
"""
