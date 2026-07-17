#!/usr/bin/env bash
# Copy the governing documents into assets/ so the Railway service (root dir =
# intake-webhook) can read them. Re-run after any directive/template change,
# then redeploy: ./sync_assets.sh && railway up --detach
set -euo pipefail
cd "$(dirname "$0")"
cp ../directives/generation_spec_v2.md assets/
cp ../directives/opportunity_taxonomy.md assets/
cp ../templates/assessment_interactive.html assets/
echo "assets synced:"; ls -la assets/
