from flask import Flask, request, redirect

app = Flask(_name_)

CANONICAL = "outbroker.app"

def _is_run_app_host(host: str) -> bool:
    return host.endswith(".run.app")

@app.before_request
def force_canonical():
    host = request.headers.get("Host", "")
    if not host:
        return
    if host.startswith("www.") and CANONICAL:
        url = request.url.replace(f"//{host}", f"//{CANONICAL}")
        return redirect(url, code=301)
    if CANONICAL and not _is_run_app_host(host) and host != CANONICAL:
        return redirect(f"https://{CANONICAL}{request.full_path}", code=301)

@app.route("/_ah/health")
def health():
    return "ok", 200

@app.route("/")
def home():
    return "OutBroker em producao!"

if _name_ == "_main_":
    app.run(host="0.0.0.0", port=8080)
