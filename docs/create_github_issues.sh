#!/usr/bin/env bash
# Create GitHub issues from docs/sprint-tasks-export.csv using gh CLI
# Usage: ./create_github_issues.sh owner/repo
# Requires: gh CLI installed and authenticated (gh auth login)

set -euo pipefail

if [ "$#" -lt 1 ]; then
  echo "Usage: $0 owner/repo"
  echo "Example: $0 diogo/To_Exercises"
  exit 1
fi

REPO="$1"
CSV="docs/sprint-tasks-export.csv"

if [ ! -f "$CSV" ]; then
  echo "CSV file not found: $CSV"
  exit 2
fi

# Read CSV skipping header
tail -n +2 "$CSV" | while IFS=, read -r id title description priority status owner estimate; do
  # Trim possible surrounding quotes (simple)
  title=$(echo "$title" | sed 's/^"//;s/"$//')
  description=$(echo "$description" | sed 's/^"//;s/"$//')
  priority=$(echo "$priority" | sed 's/^"//;s/"$//')
  owner=$(echo "$owner" | sed 's/^"//;s/"$//')
  estimate=$(echo "$estimate" | sed 's/^"//;s/"$//')

  body="**Task ID:** $id\n\n$description\n\n**Priority:** $priority\n**Owner:** $owner\n**Estimate:** $estimate"

  labels="$priority"

  echo "Creating issue: $title (labels: $labels, assignee: $owner)"
  # Create the issue (ignore failure to assign if assignee not in repo)
  if [ -z "$owner" ] || [ "$owner" == "" ]; then
    gh issue create --repo "$REPO" --title "$title" --body "$body" --label "$labels"
  else
    gh issue create --repo "$REPO" --title "$title" --body "$body" --label "$labels" --assignee "$owner" || gh issue create --repo "$REPO" --title "$title" --body "$body" --label "$labels"
  fi

  sleep 0.2
done

echo "Done. Review created issues in https://github.com/$REPO/issues"
