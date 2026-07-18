#!/usr/bin/env bash
# Build the Tailwind stylesheet (assets/css/app.css) from tailwind.input.css.
#
# Uses the Tailwind standalone CLI (no Node required). The binary lives in
# tools/ and is git-ignored; this script downloads it on first run.
#
# Usage:
#   scripts/build_css.sh          # one-off minified build
#   scripts/build_css.sh --watch  # rebuild on change during development
set -euo pipefail
cd "$(dirname "$0")/.."

TW_VERSION="v3.4.17"
BIN="tools/tailwindcss.exe"          # on Linux/mac use tools/tailwindcss (see below)
case "$(uname -s)" in
  Linux*)  ASSET="tailwindcss-linux-x64";   BIN="tools/tailwindcss" ;;
  Darwin*) ASSET="tailwindcss-macos-arm64"; BIN="tools/tailwindcss" ;;
  *)       ASSET="tailwindcss-windows-x64.exe" ;;
esac

if [ ! -f "$BIN" ]; then
  echo "Downloading Tailwind CLI $TW_VERSION ..."
  mkdir -p tools
  curl -sSL --ssl-no-revoke -o "$BIN" \
    "https://github.com/tailwindlabs/tailwindcss/releases/download/${TW_VERSION}/${ASSET}"
  chmod +x "$BIN"
fi

if [ "${1:-}" = "--watch" ]; then
  exec "$BIN" -c tailwind.config.js -i assets/css/tailwind.input.css -o assets/css/app.css --watch
else
  "$BIN" -c tailwind.config.js -i assets/css/tailwind.input.css -o assets/css/app.css --minify
  echo "Built assets/css/app.css"
fi
