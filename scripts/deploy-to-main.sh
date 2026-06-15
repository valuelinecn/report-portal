#!/bin/bash
# deploy-to-main.sh — 将 test 分支的改动合并到 main 部署上线
# 用法: bash scripts/deploy-to-main.sh [commit-message]
# 如果不传 commit message，自动生成

set -e

ORIGINAL_BRANCH=$(git branch --show-current)
COMMIT_MSG="${1:-deploy: $(date +%Y-%m-%d) test→main 上线}"

echo "🔄 当前分支: $ORIGINAL_BRANCH"
echo ""

# 1. 确保 test 分支最新
echo "📥 确保 test 分支最新..."
git fetch origin test
echo "   ✅ test 已更新"

echo ""

# 2. 切换到 main
echo "🔄 切换到 main..."
git checkout main
git fetch origin main

# 3. 合并 test
echo "🔀 合并 test → main..."
git merge test --no-edit -m "$COMMIT_MSG"

# 4. 推送
echo "📤 推送 main 上线..."
git push origin main
echo "   ✅ 已部署到生产网站"

echo ""

# 5. 切回 test 分支（保持下次工作起点）
echo "🔄 切回 test 分支..."
git checkout test
git merge main --no-edit -m "chore: sync main after deploy"

echo ""
echo "🎉 部署完成！test 分支已同步 main 的最新状态"
echo "   https://valuelinecn.github.io/report-portal/"
