import os
PORT = os.environ.get("PORT", "8080")
bind = f"0.0.0.0:{PORT}"
workers = 2
threads = 4
timeout = 120
graceful_timeout = 30
keepalive = 5