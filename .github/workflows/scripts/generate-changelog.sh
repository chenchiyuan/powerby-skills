#!/usr/bin/env bash
set -euo pipefail

# generate-changelog.sh
# Generate changelog from git history
# Usage: generate-changelog.sh <new_version> <last_tag>

if [[ $# -ne 2 ]]; then
    echo "Usage: $0 <new_version> <last_tag>" >&2
    exit 1
fi

NEW_VERSION="$1"
LAST_TAG="$2"

echo "📝 Generating changelog for $NEW_VERSION (since $LAST_TAG)"

# Get commits since last tag
if [ "$LAST_TAG" = "v0.0.0" ]; then
    # First release - include all commits or last 10
    COMMIT_COUNT=$(git rev-list --count HEAD 2>/dev/null || echo "0")
    if [ "$COMMIT_COUNT" -gt 10 ]; then
        COMMITS=$(git log --oneline --pretty=format:"- %s (%h)" HEAD~10..HEAD)
        COMMITS_COUNT="10+"
    else
        COMMITS=$(git log --oneline --pretty=format:"- %s (%h)" HEAD~$COMMIT_COUNT 2>/dev/null || echo "- Initial commit")
        COMMITS_COUNT="$COMMIT_COUNT"
    fi
else
    COMMITS=$(git log --oneline --pretty=format:"- %s (%h)" $LAST_TAG..HEAD)
    COMMITS_COUNT=$(git rev-list --count $LAST_TAG..HEAD 2>/dev/null || echo "0")
fi

# Categorize commits
FEATURES=$(echo "$COMMITS" | grep -E "feat|feature" || echo "")
FIXES=$(echo "$COMMITS" | grep -E "fix|bug" || echo "")
DOCS=$(echo "$COMMITS" | grep -E "docs|doc" || echo "")
REFACTORS=$(echo "$COMMITS" | grep -E "refactor|refactor" || echo "")
TESTS=$(echo "$COMMITS" | grep -E "test" || echo "")
CHORES=$(echo "$COMMITS" | grep -E "chore|ci" || echo "")

# Get affected skills
AFFECTED_SKILLS=$(git log --oneline --name-only --pretty=format: $LAST_TAG..HEAD 2>/dev/null | grep "skills/powerby-" | sed 's|skills/||' | cut -d'/' -f1 | sort -u || echo "")

# Create changelog
cat > CHANGELOG.md << EOF
# Changelog

All notable changes to PowerBy Skills will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v$NEW_VERSION] - $(date +%Y-%m-%d)

### Added
$(echo "$FEATURES" || echo "- No new features")
EOF

if [ -n "$FIXES" ]; then
    cat >> CHANGELOG.md << EOF

### Fixed
$FIXES
EOF
fi

if [ -n "$DOCS" ]; then
    cat >> CHANGELOG.md << EOF

### Changed
$DOCS
EOF
fi

if [ -n "$REFACTORS" ]; then
    cat >> CHANGELOG.md << EOF

### Refactored
$REFACTORS
EOF
fi

if [ -n "$TESTS" ]; then
    cat >> CHANGELOG.md << EOF

### Testing
$TESTS
EOF
fi

if [ -n "$CHORES" ]; then
    cat >> CHANGELOG.md << EOF

### Chores
$CHORES
EOF
fi

if [ -n "$AFFECTED_SKILLS" ]; then
    cat >> CHANGELOG.md << EOF

### Skills Updated
$(echo "$AFFECTED_SKILLS" | sed 's/^/- /')
EOF
fi

cat >> CHANGELOG.md << EOF

### Commits
Total commits: $COMMITS_COUNT

### Contributors
$(git log --format='%an' $LAST_TAG..HEAD 2>/dev/null | sort -u | sed 's/^/- /' || echo "- Core Team")

---

**Release Notes Generated**: $(date)
**Version Type**: $2
**Repository**: ${{ github.repository }}
EOF

echo "✅ Changelog generated successfully"
echo ""
cat CHANGELOG.md
