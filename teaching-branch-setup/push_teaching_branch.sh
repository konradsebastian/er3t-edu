#!/usr/bin/env bash
# push_teaching_branch.sh
# Creates and pushes teaching/summer-school-2026 branch to hong-chen/er3t
# Run from anywhere. Requires push access to github.com/hong-chen/er3t.
#
# Usage:
#   cd ~/projects/er3t-edu/teaching-branch-setup
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
git checkout -b teaching/summer-school-2026

echo ""
echo "=== Step 3: Apply patches ==="
git am "$SCRIPT_DIR"/0001-*.patch
git am "$SCRIPT_DIR"/0002-*.patch

echo ""
echo "=== Step 4: Verify ==="
git log --oneline release/v0.2.0-alpha.1..teaching/summer-school-2026

echo ""
echo "=== Step 5: Push to hong-chen/er3t ==="
git push origin teaching/summer-school-2026

echo ""
echo "Done. Branch teaching/summer-school-2026 is now live on hong-chen/er3t."
