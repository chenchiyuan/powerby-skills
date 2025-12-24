#!/usr/bin/env bash
set -euo pipefail

# get-next-version.sh
# Calculate the next version based on the latest git tag and commit history
# Usage: get-next-version.sh [major|minor|patch]

VERSION_TYPE="${1:-patch}"

# Get the latest tag, or use v0.0.0 if no tags exist
LATEST_TAG=$(git describe --tags --abbrev=0 2>/dev/null || echo "v0.0.0")
echo "latest_tag=$LATEST_TAG" >> $GITHUB_OUTPUT

# Extract version number
VERSION=$(echo $LATEST_TAG | sed 's/v//')
IFS='.' read -ra VERSION_PARTS <<< "$VERSION"
MAJOR=${VERSION_PARTS[0]:-0}
MINOR=${VERSION_PARTS[1]:-0}
PATCH=${VERSION_PARTS[2]:-0}

# Increment version based on type
if [ "$VERSION_TYPE" = "major" ]; then
    MAJOR=$((MAJOR + 1))
    MINOR=0
    PATCH=0
elif [ "$VERSION_TYPE" = "minor" ]; then
    MINOR=$((MINOR + 1))
    PATCH=0
else
    PATCH=$((PATCH + 1))
fi

NEW_VERSION="$MAJOR.$MINOR.$PATCH"
NEW_TAG="v$NEW_VERSION"

echo "new_version=$NEW_VERSION" >> $GITHUB_OUTPUT
echo "new_tag=$NEW_TAG" >> $GITHUB_OUTPUT
echo "version_type=$VERSION_TYPE" >> $GITHUB_OUTPUT

echo "✅ Calculated new version: $NEW_TAG (type: $VERSION_TYPE)"
