bind = "0.0.0.0:8000"
workers = 3
worker_class = "uvicorn.workers.UvicornWorker"
timeout = 60
graceful_timeout = 30
loglevel = "info"
accesslog = "-"
errorlog = "-"
