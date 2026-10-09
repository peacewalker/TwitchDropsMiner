import json
import time
import urllib.error
import urllib.request

base = "http://127.0.0.1:5800"
deadline = time.monotonic() + 60
while time.monotonic() < deadline:
    try:
        with urllib.request.urlopen(base + "/health", timeout=3) as response:
            status = json.load(response)
        if status.get("status") == "ok":
            break
    except (OSError, ValueError):
        pass
    time.sleep(1)
else:
    raise SystemExit("The WebUI did not become healthy within 60 seconds.")
with urllib.request.urlopen(base, timeout=5) as response:
    assert response.status == 200
for path in ("/browser-login/novnc/vnc.html", "/browser-login/view/fixture"):
    try:
        urllib.request.urlopen(base + path, timeout=5)
    except urllib.error.HTTPError as error:
        assert error.code == 404, (path, error.code)
    else:
        raise AssertionError("A browser login route is unexpectedly available")
print("WebUI and health endpoint work; browser login routes are absent.")
