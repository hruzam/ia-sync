#!/usr/bin/env python3
"""
ts-dash.py — Tailscale status HTTP dashboard
Called by _ts_dash() in system/tailscale.zsh. Auto-refreshes every 10s.
Port: $TS_DASH_PORT env var (default 9733).
"""

import http.server
import json
import os
import subprocess
from datetime import datetime

PORT = int(os.environ.get("TS_DASH_PORT", 9733))

HTML = """\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="refresh" content="10">
  <title>Tailscale — {hostname}</title>
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: 'SF Mono', 'Fira Mono', monospace;
      background: #0d1117;
      color: #c9d1d9;
      padding: 2rem;
      max-width: 680px;
      margin: auto;
    }}
    h1 {{ color: #58a6ff; font-size: 1.1rem; margin-bottom: 0.3rem; letter-spacing: 0.05em; }}
    .meta {{ color: #6e7681; font-size: 0.8rem; margin-bottom: 1.5rem; }}
    .host {{
      display: flex; align-items: center; gap: 1rem;
      padding: 0.6rem 0.8rem; margin: 0.3rem 0;
      border-radius: 6px; background: #161b22;
      border-left: 3px solid transparent;
    }}
    .host.online  {{ border-color: #3fb950; }}
    .host.offline {{ border-color: #f85149; opacity: 0.6; }}
    .host.self    {{ border-color: #58a6ff; }}
    .name {{ font-weight: bold; color: #e6edf3; min-width: 180px; }}
    .ip   {{ color: #79c0ff; font-size: 0.85rem; }}
    .state {{ color: #8b949e; font-size: 0.78rem; margin-left: auto; }}
    .footer {{ margin-top: 1.5rem; color: #6e7681; font-size: 0.75rem; }}
    .error {{ color: #f85149; padding: 1rem; background: #161b22; border-radius: 6px; }}
  </style>
</head>
<body>
  <h1>Tailscale — {hostname}</h1>
  <div class="meta">auto-refresh 10s · {ts}</div>
  {body}
  <div class="footer">ts-dash · port {port} · ts-dash-stop to kill</div>
</body>
</html>
"""


def get_status():
    try:
        raw = subprocess.check_output(
            ["tailscale", "status", "--json"], timeout=4, stderr=subprocess.DEVNULL
        )
        return json.loads(raw)
    except Exception:
        return None


def build_body(data):
    if data is None:
        return '<div class="error">tailscaled not reachable</div>'

    rows = []

    s = data.get("Self", {})
    s_host = s.get("HostName", "?")
    s_ip = (s.get("TailscaleIPs") or ["?"])[0]
    rows.append(
        f'<div class="host self">'
        f'<span class="name">{s_host}</span>'
        f'<span class="ip">{s_ip}</span>'
        f'<span class="state">self</span>'
        f"</div>"
    )

    peers = sorted(
        data.get("Peer", {}).values(),
        key=lambda p: (not p.get("Online", False), p.get("HostName", ""))
    )

    for p in peers:
        online = p.get("Online", False)
        active = p.get("Active", False)
        host = p.get("HostName", "?")
        ip = (p.get("TailscaleIPs") or ["?"])[0]
        cls = "online" if online else "offline"
        if active:
            state = "active"
        elif online:
            state = "idle"
        else:
            last = p.get("LastSeen", "")
            state = f"last seen {last[:10]}" if last else "offline"

        rows.append(
            f'<div class="host {cls}">'
            f'<span class="name">{host}</span>'
            f'<span class="ip">{ip}</span>'
            f'<span class="state">{state}</span>'
            f"</div>"
        )

    return "\n  ".join(rows)


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        data = get_status()
        body = build_body(data)
        hostname = os.uname().nodename
        ts = datetime.now().strftime("%H:%M:%S")
        html = HTML.format(hostname=hostname, ts=ts, body=body, port=PORT).encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(html)))
        self.end_headers()
        self.wfile.write(html)

    def log_message(self, *_):
        pass


if __name__ == "__main__":
    server = http.server.HTTPServer(("localhost", PORT), Handler)
    print(f"[ts-dash] http://localhost:{PORT}  (Ctrl+C to stop)", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[ts-dash] stopped")
