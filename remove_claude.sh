#!/bin/bash
# 删除 Git 提交中的 Claude 痕迹

# 获取提交信息，删除 Claude 相关行
COMMIT_MSG=$(git log -1 --format=%B | sed '/🤖 Generated with \[Claude Code\]/d' | sed '/Co-Authored-By: Claude/d' | sed '/^$/N;/^\n$/D')

# 使用新的提交信息修改提交
git commit --amend -m "$COMMIT_MSG"
