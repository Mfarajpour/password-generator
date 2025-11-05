"""
Gunicorn configuration file for Password Generator
"""

import os
import multiprocessing

# ============================================================================
# Server Socket
# ============================================================================
bind = f"0.0.0.0:{os.getenv('PORT', '5000')}"
backlog = 2048

# ============================================================================
# Worker Processes
# ============================================================================
# Calculate optimal workers: (2 x CPU cores) + 1
workers = int(os.getenv('GUNICORN_WORKERS', multiprocessing.cpu_count() * 2 + 1))
worker_class = 'sync'  # Options: sync, gevent, eventlet
worker_connections = 1000
max_requests = 1000  # Restart workers after this many requests (prevents memory leaks)
max_requests_jitter = 50  # Randomize restart to avoid all workers restarting at once
timeout = 30
keepalive = 2

# ============================================================================
# Logging
# ============================================================================
accesslog = '-'  # stdout
errorlog = '-'   # stderr
loglevel = os.getenv('LOG_LEVEL', 'info')  # debug, info, warning, error, critical

# Custom access log format
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'
# %(h) - client IP
# %(l) - '-' 
# %(u) - user
# %(t) - timestamp
# %(r) - request line
# %(s) - status code
# %(b) - response size
# %(f) - referer
# %(a) - user agent
# %(D) - request time in microseconds

# ============================================================================
# Process Naming
# ============================================================================
proc_name = 'password-generator'

# ============================================================================
# Server Mechanics
# ============================================================================
daemon = False  # Don't daemonize (Docker handles this)
pidfile = None
umask = 0
user = None  # Run as current user (appuser in Docker)
group = None
tmp_upload_dir = None

# Preload app for faster worker spawn (use with caution)
preload_app = False

# ============================================================================
# Security
# ============================================================================
limit_request_line = 4096
limit_request_fields = 100
limit_request_field_size = 8190

# ============================================================================
# Development/Debug (optional)
# ============================================================================
# reload = os.getenv('DEBUG', 'False').lower() == 'true'  # Auto-reload on code change
# reload_extra_files = []  # Additional files to watch
