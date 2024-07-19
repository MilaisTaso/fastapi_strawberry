bind = "0.0.0.0:8000"
reload = True
demon = True
timeout = 30
proc_name = "cpp_coconala_server"
worker_class = "src.gunicorn.worker.RestartableUvicornWorker"
workers = 2
