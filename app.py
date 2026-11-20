import os
from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def index():
    return """
    <h1>Cloud Technologies Laboratory</h1>
    <p>Lab 12 — Monitoring on Render</p>
    <p><a href="/health">/health</a> · <a href="/load">/load</a></p>
    """


@app.route("/health")
def health():
    return jsonify(status="ok", service="lab12-render")


@app.route("/load")
def load():
    """Light CPU work for load experiment."""
    total = 0
    for i in range(200_000):
        total += i * i
    return jsonify(status="loaded", result=total)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
