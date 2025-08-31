import os

# Cloud Run expõe a porta via variável de ambiente PORT
bind = f"0.0.0.0:{os.environ.get('PORT', '8080')}"

# Concurrency
workers = 2
threads = 4
worker_class = "gthread"
timeout = 120

# (optional) log mais verboso p/ diagnosticar
accesslog = "-"
errorlog = "-"