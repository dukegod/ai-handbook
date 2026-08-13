#!/usr/bin/env bash
# scripts/check-links.sh —— 本地死链检查
# 用法：./scripts/check-links.sh  或  bash scripts/check-links.sh
# 依赖：lychee 0.24+（brew install lychee / cargo install lychee / docker pull lycheeverse/lychee）
# v0.4.2 升级：加 root_dir + 适配 0.24 schema（verbose 字符串、accept 数组）
# v0.4.2 升级：include/exclude 放 toml 里，避免 CLI glob 解析 bug

set -e

cd "$(dirname "$0")/.."

# 检测 lychee 是否可用
if ! command -v lychee &> /dev/null; then
    echo "❌ lychee 未安装。三种方式任选："
    echo "   1. macOS:  brew install lychee"
    echo "   2. Cargo:  cargo install lychee --locked"
    echo "   3. Docker: docker run --rm -v \$(pwd):/input lycheeverse/lychee /input"
    echo ""
    echo "详见：contributing/link-checking.md"
    exit 1
fi

# 列出要检查的 .md 文件（v0.4.2 升级：lychee 0.24 把 inputs 当 regex，用 --files-from）
MD_FILELIST="$(mktemp -t lychee-md.XXXXXX)"
trap 'rm -f "$MD_FILELIST"' EXIT

find . \
    -name "*.md" \
    -not -path "./node_modules/*" \
    -not -path "./.vitepress/*" \
    -not -path "./.lycheecache/*" \
    -not -path "./scripts/.lychee-out/*" \
    -not -path "./public/*" \
    -not -path "./assets/*" \
    > "$MD_FILELIST"

MD_COUNT=$(wc -l < "$MD_FILELIST" | tr -d ' ')
echo "扫描 $MD_COUNT 个 .md 文件..."

# 跑 lychee —— v0.4.2 升级：input 通过 --files-from 列文件
# CLI 只传 root_dir（必须显式，因为 toml 里 root_dir 在 CI 是 ${{ github.workspace }}）
lychee \
    --config lychee.toml \
    --root-dir "$(pwd)" \
    --output ./scripts/.lychee-out \
    --format detailed \
    --no-progress \
    --files-from "$MD_FILELIST"

# 失败时打印摘要
if [ $? -ne 0 ]; then
    echo ""
    echo "❌ 死链检查失败——详细见 ./scripts/.lychee-out"
    exit 1
fi

echo ""
echo "✓ 死链检查通过"
