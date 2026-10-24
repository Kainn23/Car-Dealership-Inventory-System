#!/usr/bin/env bash
# scripts/check_coauthors.sh
# Audits Git commit history to report commits with and without Co-authored-by trailers.

set -euo pipefail

echo "=== AI Co-Authorship Audit ==="
echo ""
echo "--- Commits WITH Co-authored-by trailer ---"
git log --grep="Co-authored-by:" --format="%h %s" || true
echo ""
echo "--- Commits WITHOUT Co-authored-by trailer (human-only or missing trailer) ---"
git log --invert-grep --grep="Co-authored-by:" --format="%h %s" || true
echo ""
echo "Audit complete."
