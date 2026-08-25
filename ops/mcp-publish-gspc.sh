#!/usr/bin/env bash
# ops/mcp-publish-gspc.sh — MCP registry 1.0.3+ publish helper (N5-10/11)
# Owner-gated: requires mcp-publisher login github (device OAuth).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SERVER_JSON="${MCP_SERVER_JSON:-$ROOT/connect/mcp/gspc/server.json}"
PUBLISHER="${MCP_PUBLISHER:-mcp-publisher}"

if ! command -v "$PUBLISHER" >/dev/null 2>&1; then
  echo "Installing mcp-publisher v1.8.1 to /tmp/mcp-publisher…" >&2
  curl -fsSL "https://github.com/modelcontextprotocol/registry/releases/download/v1.8.1/mcp-publisher_linux_amd64.tar.gz" \
    | tar xz -C /tmp mcp-publisher
  PUBLISHER=/tmp/mcp-publisher
fi

echo "=== N5-10/11: validate server.json ==="
(cd /tmp && cp "$SERVER_JSON" ./gspc-server.json && "$PUBLISHER" validate ./gspc-server.json)

if [[ ! -f "$HOME/.mcp_publisher_token" ]]; then
  echo "GATED: run '$PUBLISHER login github' first (owner OAuth device flow)" >&2
  echo "NOTE: automated OIDC publish via csoai-static-deploy2 mcp-registry-publish.yml also works (registry/gspc.json)" >&2
  exit 2
fi

echo "=== N5-10: publish 1.0.2 ==="
(cd "$(dirname "$SERVER_JSON")" && "$PUBLISHER" publish)

echo "=== N5-11: verify registry ==="
curl -fsS "https://registry.modelcontextprotocol.io/v0.1/servers?search=gspc" \
  | python3 -c "import json,sys;d=json.load(sys.stdin);print([(s['server'].get('version'),s['_meta']['io.modelcontextprotocol.registry/official'].get('isLatest')) for s in d.get('servers',[])])"
