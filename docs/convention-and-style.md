# Commit and Pull Request Guidelines

## Branches

For all work related to tickets, please branch off of `master` or a corresponding base branch.  
Include the purpose when naming your branch, e.g. "feature" or "fix", and Github project issue ID if applicable.

```
# Acceptable branch names
feature/123-create-new-feature
fix/123-fix-bugs

# Unacceptable branch names
myBranch # missing purpose
```

## Commits

1. Follow Conventional Commits.
2. Commit title should be all lowercase.
3. Commit title should be written in the imperative, e.g. "fix", not "fixed" or "fixes".
4. Commit title length should not exceed 100 characters.
5. Scopes (when applicable) should be all lowercase, e.g. `feat(mini mode):`, `fix(profile sync):`
6. Keep commits small.
7. Each commit should contain one logical unit of change. Avoid unrelated changes in a commit.

## Pull Requests

1. Keep pull requests small.
2. Keep the commit history linear. See [Merging vs. Rebasing](https://www.atlassian.com/git/tutorials/merging-vs-rebasing)
3. Capitalize the first letter in the title.
4. Include the related Github project issue ID(s) in the pull request branch name or merge commit message if applicable.

# Style Guide

## General

This project follows Google's [Python](https://google.github.io/styleguide/pyguide.html) style guides fairly close.
