#!/usr/bin/env bash
# push_teaching_branch.sh
# Creates and pushes dev_er3t_edu branch to hong-chen/er3t
# Run from anywhere. Requires push access to github.com/hong-chen/er3t.
#
# Usage:
#   cd ~/projects/dev_er3t_edu/teaching-branch-setup
#   bash push_teaching_branch.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORK_DIR="/tmp/hong-chen-er3t-push"

echo "=== Step 1: Clone hong-chen/er3t ==="
if [ -d "$WORK_DIR" ]; then
    echo "  Found existing clone — removing and re-cloning for a clean start"
    rm -rf "$WORK_DIR"
fi
git clone https://github.com/hong-chen/er3t.git "$WORK_DIR"

echo ""
echo "=== Step 2: Create teaching branch from release/v0.2.0-alpha.1 ==="
cd "$WORK_DIR"
git checkout release/v0.2.0-alpha.1
git checkout -b dev_er3t_edu

echo ""
echo "=== Step 3: Apply patches ==="
git am "$SCRIPT_DIR"/0001-*.patch
git am "$SCRIPT_DIR"/0002-*.patch

echo ""
echo "=== Step 4: Verify ==="
git log --oneline release/v0.2.0-alpha.1..dev_er3t_edu

echo ""
echo "=== Step 5: Push to hong-chen/er3t ==="
git push origin dev_er3t_edu

echo ""
echo "Done. Branch dev_er3t_edu is now live on hong-chen/er3t."
