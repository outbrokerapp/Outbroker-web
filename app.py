from flask import Flask, request, redirect, jsonify
import os

app = Flask(__name__)

CANONICAL = os.environ.get("CANONICAL_HOST", "outbroker.app").strip()

def _is_run_app_host(host: str) -> bool:
    return host.endswith(".run.app")

@app.before_request
def force_canonical():
    host = request.headers.get("Host", "") or ""
    if not host or _is_run_app_host(host):
        return
    if CANONICAL and host != CANONICAL:
        return redirect(f"https://{CANONICAL}{request.full_path}", code=301)

@app.route("/_ah/health")
@app.route("/healthz")
def health():
    return "ok", 200

@app.route("/")
def home():
    return "OutBroker em produção!", 200

# ---- API de lead (pode testar depois) ----
try:
    from google.cloud import firestore
    db = firestore.Client()
except Exception:
    db = None

@app.post("/api/lead")
def api_lead():
    # DEBUG TEMPORÁRIO
    if request.args.get("debug") == "1":
        return jsonify({
            "json": request.get_json(silent=True),
            "content_type": request.headers.get("Content-Type"),
            "length": request.headers.get("Content-Length"),
        }), 200

    data = request.get_json(silent=True) or {}
    name = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip()
    phone = (data.get("phone") or "").strip()
    if not (name and (email or phone)):
        return jsonify(ok=False, error="Informe nome e (email ou telefone)."), 400
    doc = {
        "name": name, "email": email, "phone": phone,
        "ip": request.headers.get("x-forwarded-for", request.remote_addr),
        "ua": request.headers.get("user-agent","")
    }
    if db:
        db.collection("leads").add(doc)
    return jsonify(ok=True, stored=bool(db)), 201

# --- página de formulário simples em /form ---
@app.get("/form")
def form_page():
    return """<!doctype html>
<html lang="pt-br">
<meta charset="utf-8">
<title>Form Lead</title>
<h1>Enviar Lead</h1>
<form id="leadForm">
  <label>Nome* <input name="name" required></label><br>
  <label>Email <input name="email" type="email"></label><br>
  <label>Telefone <input name="phone"></label><br>
  <button type="submit">Enviar</button>
</form>
<pre id="result"></pre>
<script>
  const f = document.getElementById('leadForm');
  f.addEventListener('submit', async (e) => {
    e.preventDefault();
    const data = Object.fromEntries(new FormData(f).entries());
    const res = await fetch('/api/lead', {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify(data)
    });
    let text;
    try { text = JSON.stringify(await res.json(), null, 2); }
    catch { text = await res.text(); }
    document.getElementById('result').textContent = text;
  });
</script>
</html>"""
