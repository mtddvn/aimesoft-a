#!/bin/bash
# deploy.sh <a|b>  : push site-<x>/ to the GitHub repo mtddvn/aimesoft-<x> (GitHub Pages, custom domain aimesoft-<x>.ciaosoft.vn).
# Creates the repo and enables Pages on first run; later runs just push a new commit. No `cd`: every path is absolute.
set -euo pipefail
X="$1"
ROOT="/Users/ciaosoft/Claude/BRvault/Projects/Aimesoft website 2.0/home-v2"
SITE="$ROOT/site-$X"
REPO="aimesoft-$X"
DOMAIN="aimesoft-$X.ciaosoft.vn"
SCR="/private/tmp/claude-503/-Users-ciaosoft-Claude-BRvault/9c58c75c-aeaf-462f-a626-890935ba223c/scratchpad"
VER="${2:-0.1.0}"
XU=$(echo "$X" | tr a-z A-Z)

[ "$(cat "$SITE/CNAME")" = "$DOMAIN" ] || { echo "CNAME mismatch"; exit 1; }
D=$(mktemp -d "$SCR/deploy-$X.XXXXXX")
rsync -a --delete --exclude '.git' "$SITE/" "$D/"
git -C "$D" init -q -b main
git -C "$D" config user.name "mtddvn"
git -C "$D" config user.email "info@ciaosoft.vn"
git -C "$D" add -A
git -C "$D" commit -q -m "Aimesoft 2.0 home page, direction $XU v$VER" -m "Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01PikJdBn7XLbT4sDaovuNrG"

if ! gh repo view "mtddvn/$REPO" >/dev/null 2>&1; then
  gh repo create "mtddvn/$REPO" --public --description "Aimesoft 2.0 home page, direction $XU" >/dev/null
  echo "repo created"
fi
git -C "$D" remote add origin "https://github.com/mtddvn/$REPO.git"
git -C "$D" -c credential.helper='!gh auth git-credential' push -q -f origin main
echo "pushed $(git -C "$D" rev-parse --short HEAD)"

if ! gh api "repos/mtddvn/$REPO/pages" >/dev/null 2>&1; then
  gh api -X POST "repos/mtddvn/$REPO/pages" -f "source[branch]=main" -f "source[path]=/" >/dev/null
  echo "pages enabled"
fi
gh api -X PUT "repos/mtddvn/$REPO/pages" -f "cname=$DOMAIN" >/dev/null 2>&1 || echo "cname put: see below"
gh api "repos/mtddvn/$REPO/pages" --jq '{url:.html_url,cname:.cname,status:.status,https:.https_enforced}'
