import os
import time
from flask import Flask, jsonify

try:
    import psutil
except ImportError:  # pragma: no cover
    psutil = None

app = Flask(__name__)


@app.route("/")
def index():
    return """
    <h1>Cloud Technologies Laboratory</h1>
    <p>Lab 12 — Monitoring on Render</p>
    <p>
      <a href="/health">/health</a> ·
      <a href="/stats">/stats</a> ·
      <a href="/load">/load</a>
    </p>
    """


@app.route("/health")
def health():
    return jsonify(status="ok", service="lab12-render")


@app.route("/stats")
def stats():
    """Collect CPU/RAM/disk/process metrics without SSH (for Free plan)."""
    if psutil is None:
        return jsonify(error="psutil not installed"), 500

    cpu_percent = psutil.cpu_percent(interval=0.3)
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage("/")
    net = psutil.net_io_counters()
    return jsonify(
        {
            "host": os.uname().nodename if hasattr(os, "uname") else "render",
            "cpu_percent": cpu_percent,
            "cpu_count": psutil.cpu_count(),
            "ram": {
                "total_mb": round(mem.total / 1024 / 1024, 1),
                "used_mb": round(mem.used / 1024 / 1024, 1),
                "percent": mem.percent,
            },
            "disk": {
                "total_gb": round(disk.total / 1024 / 1024 / 1024, 2),
                "used_gb": round(disk.used / 1024 / 1024 / 1024, 2),
                "percent": disk.percent,
            },
            "network": {
                "bytes_sent": net.bytes_sent,
                "bytes_recv": net.bytes_recv,
            },
            "processes": len(psutil.pids()),
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        }
    )


@app.route("/load")
def load():
    """CPU work for load experiment."""
    total = 0
    for i in range(400_000):
        total += i * i
    return jsonify(status="loaded", result=total)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
