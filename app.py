import os
from datetime import datetime, timezone
from flask import Flask, request, jsonify, redirect
from google.cloud import firestore

app = Flask(__name__)

# Domínio canônico (sem www)
CANONICAL = os.environ.get("CANONICAL_HOST", "outbroker.app")

# Firestore client (credenciais do Cloud Run)
db = firestore.Client()

# --- SEO: força www -> raiz (301) ---
@app.before_request
def force_canonical():
    host = request.headers.get("Host", "")
    if host.startswith("www.") and CANONICAL and host != CANONICAL:
        url = request.url.replace(f"//{host}", f"//{CANONICAL}")
        return redirect(url, code=301)

# Healthcheck
@app.get("/healthz")
def healthz():
    return jsonify(status="ok")

# Landing bem simples (HTML)
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
            body {
                font-family: Arial, Helvetica, sans-serif;
                margin: 0;
                padding: 0;
                background: #f9f9f9;
                color: #333;
                text-align: center;
            }
            header {
                background: #1a73e8;
                color: white;
                padding: 30px 20px;
            }
            header h1 {
                margin: 0;
                font-size: 2.5em;
            }
            header p {
                margin-top: 10px;
                font-size: 1.2em;
            }
            main {
                padding: 40px 20px;
            }
            main p {
                font-size: 1.2em;
                margin-bottom: 20px;
            }
            a.button {
                display: inline-block;
                padding: 12px 25px;
                font-size: 1.1em;
                font-weight: bold;
                background: #1a73e8;
                color: white;
                border-radius: 6px;
                text-decoration: none;
                transition: background 0.3s;
            }
            a.button:hover {
                background: #1557b0;
            }
            footer {
                margin-top: 40px;
                padding: 20px;
                font-size: 0.9em;
                color: #777;
            }
        </style>
    </head>
    <body>
        <header>
            <h1>OutBroker</h1>
            <p>Conectando corretores e oportunidades</p>
        </header>
        <main>
            <p>Nosso MVP está em construção 🚀<br>
            Deixe seu contato para participar.</p>
            <a href="https://wa.me/5511999990000" class="button">Quero participar</a>
        </main>
        <footer>
            &copy; 2025 OutBroker
        </footer>
    </body>
    </html>
    """,200