import os
import ssl
import urllib.request

protocol = "https" if os.environ.get("SECURE_CONNECTION") == "1" else "http"
port = int(os.environ.get("WEBUI_PORT", "5800"))
context = ssl._create_unverified_context() if protocol == "https" else None
with urllib.request.urlopen(f"{protocol}://127.0.0.1:{port}/health", context=context, timeout=8) as response:
    if response.status != 200:
        raise SystemExit(1)
