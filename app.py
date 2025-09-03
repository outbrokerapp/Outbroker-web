import os
from flask import Flask, request, jsonify, redirect

app = Flask(__name_)  # <-- aqui está certo agora

# --- Healthchecks ---
@app.get("/healthz")
def healthz():
    return jsonify(status="ok"), 200

@app.get("/health")
def health():
    return jsonify(status="ok"), 200

@app.get("/_ah/health")
def ah_health():
    return "ok", 200

# Domínio canônico (opcional)
CANONICAL = os.environ.get("CANONICAL_HOST", "").strip()

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
        target = f"https://{CANONICAL}{request.full_path}"
        return redirect(target, code=301)

# --- Rota principal ---
@app.get("/")
def index():
    return """
<!DOCTYPE html>
<html lang="pt-br">
<head>
  <meta charset="UTF-8">
  <meta _name="viewport" content="width=device-width, initial-scale=1.0">
  <title>OutBroker</title>
  <style>
    body{font-family:Arial,Helvetica,sans-serif;margin:0;background:#f9f9f9;color:#333;text-align:center}
    header{background:#1a73e8;color:#fff;padding:30px 20px}
    header h1{margin:0;font-size:2.2em}
    main{padding:40px 20px}
    a.button{display:inline-block;padding:12px 24px;font-weight:bold;border-radius:6px;
             text-decoration:none;background:#1a73e8;color:#fff}
    a.button:hover{background:#1557b0}
    footer{margin:40px 0;color:#777}
  </style>
</head>
<body>
  <header>
    <h1>OutBroker</h1>
    <p>Conectando corretores e oportunidades</p>
  </header>
  <main>
    <p>Nosso MVP está em construção 🚀<br>Deixe seu contato para participar.</p>
    <a href="https://wa.me/5511999990000" class="button">Quero participar</a>
  </main>
  <footer>&copy; 2025 OutBroker</footer>
</body>
</html>
""", 200

# --- Execução local ---
if __name_ == "_main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
EOF
