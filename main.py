import os
from datetime import datetime, timezone
from flask import Flask, request, jsonify, redirect

app = Flask(_name_)

# --- Healthchecks ---
@app.get("/healthz")
def healthz():
    return jsonify(status="ok"), 200

@app.get("/health")
def health():
    return jsonify(status="ok"), 200

# compatível com checagens padrão do GCP/AppEngine
@app.get("/_ah/health")
def ah_health():
    return "ok", 200

# Domínio canônico (sem www). Se vazio, não força nada.
CANONICAL = os.environ.get("CANONICAL_HOST", "").strip()

def _is_run_app_host(host: str) -> bool:
    # Não forçar canônico quando acessado pela URL padrão do Cloud Run
    return host.endswith(".run.app")

# --- SEO/host canônico: força www -> domínio raiz e host canônico fora do run.app ---
@app.before_request
def force_canonical():
    host = request.headers.get("Host", "")
    if not host:
        return  # nada a fazer

    # Se tiver www, remove e redireciona
    if host.startswith("www.") and CANONICAL:
        url = request.url.replace(f"//{host}", f"//{CANONICAL}")
        return redirect(url, code=301)

    # Se CANONICAL estiver definido e NÃO for host do Cloud Run, força canônico
    if CANONICAL and not _is_run_app_host(host) and host != CANONICAL:
        target = f"https://{CANONICAL}{request.full_path}"
        return redirect(target, code=301)

# --- Firestore: inicialização preguiçosa e tolerante a erro ---
db = None
def get_db():
    global db
    if db is None:
        try:
            from google.cloud import firestore  # importa só quando precisar
            db = firestore.Client()
        except Exception as e:
            # Não derruba o app se Firestore não estiver pronto/permissão faltando
            print("Firestore init skipped:", e)
            db = None
    return db

# --- Rota principal ---
@app.get("/")
def index():
    return """
<!DOCTYPE html>
<html lang="pt-br">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
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

# Fallback local (rodando python main.py)
if _name_ == "_main_":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)