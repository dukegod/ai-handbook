#!/bin/sh
# 安装 Git hooks 到 .git/hooks/
# 由 pnpm install 自动调用（package.json postinstall）

HOOKS_DIR="$(git rev-parse --show-toplevel)/.git/hooks"
SCRIPT_DIR="$(cd "$(dirname "$0")/hooks" && pwd)"

for hook in "$SCRIPT_DIR"/*; do
  name=$(basename "$hook")
  cp "$hook" "$HOOKS_DIR/$name"
  chmod +x "$HOOKS_DIR/$name"
  echo "installed hook: $name"
done
