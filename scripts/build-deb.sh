#!/bin/bash
set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_DIR"

VERSION="0.1.0"
PACKAGE_DIR="packaging/deb"
WHEELS_DIR="packaging/wheels"
DEST_WHEELS="$PACKAGE_DIR/opt/jay/wheels"
OUTPUT_DIR="release"
OUTPUT_FILE="$OUTPUT_DIR/jay-terminal-assistant_${VERSION}_amd64.deb"

echo "Preparing dependency wheels..."
mkdir -p "$DEST_WHEELS"
rm -f "$DEST_WHEELS"/*.whl
cp "$WHEELS_DIR"/*.whl "$DEST_WHEELS/"

echo "Building Jay Debian package..."
mkdir -p "$OUTPUT_DIR"

dpkg-deb --root-owner-group --build \
    "$PACKAGE_DIR" \
    "$OUTPUT_FILE"

echo "Package created: $OUTPUT_FILE"
