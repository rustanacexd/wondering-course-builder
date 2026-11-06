# Minimal Wondering MCP client: call(tool, args) -> parsed tool result.
# Token file: $WONDERING_TOKEN_FILE, default ~/.wondering-setup/token. Server: $WONDERING_MCP_URL.
import json, os, urllib.request
URL = os.environ.get("WONDERING_MCP_URL", "https://mvhwfzawowaxyivkmjdv.supabase.co/functions/v1/mcp")
TOKEN = open(os.path.expanduser(os.environ.get("WONDERING_TOKEN_FILE", "~/.wondering-setup/token"))).read().strip()
def _post(body, sid=None):
    h = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json", "Accept": "application/json, text/event-stream"}
    if sid: h["Mcp-Session-Id"] = sid
    r = urllib.request.urlopen(urllib.request.Request(URL, json.dumps(body).encode(), h))
    return r.headers.get("Mcp-Session-Id"), r.read().decode()
def call(tool, args):
    sid, _ = _post({"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"cc","version":"1"}}})
    _post({"jsonrpc":"2.0","method":"notifications/initialized"}, sid)
    _, out = _post({"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":tool,"arguments":args}}, sid)
    msg = json.loads(out)
    if "error" in msg: raise RuntimeError(msg["error"])
    return json.loads(msg["result"]["content"][0]["text"])
