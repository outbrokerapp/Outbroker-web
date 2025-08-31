from flask import Flask, jsonify, request, redirect
import os

app = Flask(__name__)

CANONICAL = os.environ.get("CANONICAL_HOST", "outbroker.app")  # domínio final

# (opcional) força canonicalização: www -> raiz (ou troque p/ raiz -> www)
@app.before_request
def force_canonical():
    host = request.headers.get("Host", "")
    if host and host != CANONICAL:
        # 301 para SEO
        url = request.url.replace(f"//{host}", f"//{CANONICAL}")
        return redirect(url, code=301)

@app.get("/healthz")
def healthz():
    return jsonify(status="ok")

@app.get("/")
def index():
    return """
<!doctype html>
<html lang="pt-br">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>OutBroker — Backend base</title>
<style>
  body{font-family:system-ui,Arial;margin:0;background:#0f172a;color:#e2e8f0;line-height:1.6}
  .wrap{max-width:820px;margin:0 auto;padding:48px 24px}
  .card{background:#111827;border:1px solid #1f2937;border-radius:16px;padding:32px}
  h1{margin:0 0 8px;font-size:28px} code{background:#1f2937;padding:2px 6px;border-radius:6px}
</style>
</head>
<body>
  <div class="wrap">
    <div class="card">
      <h1>OutBroker — serviço base</h1>
      <p>OK! Seu serviço definitivo está rodando no Cloud Run. Endpoints:</p>
      <ul>
        <li><code>/</code> — esta página</li>
        <li><code>/healthz</code> — health check (retorna status=ok)</li>
      </ul>
      <p>Agora podemos começar a construir o MVP (rotas, banco, auth) por cima deste serviço.</p>
    </div>
  </div>
</body>
</html>
""", 200
