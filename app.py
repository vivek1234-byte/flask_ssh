"""Sample Flask application for the Jenkins CI/CD pipeline."""

from flask import Flask, jsonify, render_template_string

app = Flask(__name__)

# ── HTML Templates ──────────────────────────────────────────────────────────

BASE_STYLE = """
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    min-height: 100vh;
    display: flex; align-items: center; justify-content: center;
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    color: #fff;
  }
  .card {
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.15);
    border-radius: 20px;
    padding: 50px 40px;
    max-width: 520px;
    width: 90%;
    text-align: center;
    box-shadow: 0 8px 32px rgba(0,0,0,0.4);
  }
  .card h1 { font-size: 2.2rem; margin-bottom: 10px; }
  .card .emoji { font-size: 3.5rem; margin-bottom: 18px; }
  .card p { font-size: 1.1rem; color: #ccc; line-height: 1.6; margin-bottom: 20px; }
  .badge {
    display: inline-block;
    padding: 6px 18px;
    border-radius: 50px;
    font-size: 0.85rem;
    font-weight: 600;
    letter-spacing: 0.5px;
  }
  .badge-green { background: #00c853; color: #000; }
  .badge-blue  { background: #2979ff; color: #fff; }
  .links { margin-top: 28px; }
  .links a {
    color: #90caf9;
    text-decoration: none;
    margin: 0 12px;
    font-size: 1rem;
    transition: color 0.2s;
  }
  .links a:hover { color: #fff; }
  .footer { margin-top: 30px; font-size: 0.8rem; color: #777; }
</style>
"""

INDEX_PAGE = (
    "<!DOCTYPE html><html><head><title>Flask SSH App</title>"
    + BASE_STYLE
    + """</head><body>
  <div class="card">
    <div class="emoji">🚀</div>
    <h1>Flask SSH App</h1>
    <p>Deployed via <strong>Jenkins CI/CD</strong> pipeline with SSH authentication.</p>
    <span class="badge badge-green">● Running on port 5001</span>
    <div class="links">
      <a href="/hello">👋 Say Hello</a>
      <a href="/api/status">📡 API Status</a>
    </div>
    <div class="footer">Built with Flask &bull; CI/CD by Jenkins</div>
  </div>
</body></html>"""
)

HELLO_PAGE = (
    "<!DOCTYPE html><html><head><title>Hello!</title>"
    + BASE_STYLE
    + """</head><body>
  <div class="card">
    <div class="emoji">👋</div>
    <h1>Hello There!</h1>
    <p>Welcome from the <strong>Jenkins-built Flask app</strong>.<br>
       This page was served over a secure SSH-authenticated pipeline.</p>
    <span class="badge badge-blue">Flask + Jenkins + SSH</span>
    <div class="links">
      <a href="/">🏠 Home</a>
      <a href="/api/status">📡 API Status</a>
    </div>
    <div class="footer">Built with Flask &bull; CI/CD by Jenkins</div>
  </div>
</body></html>"""
)


# ── Routes ──────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    """Landing page with styled HTML frontend."""
    return render_template_string(INDEX_PAGE)


@app.route("/hello")
def hello():
    """Greeting page."""
    return render_template_string(HELLO_PAGE)


@app.route("/api/status")
def api_status():
    """JSON health-check endpoint for the pipeline smoke test."""
    return jsonify(status="ok", message="Flask app is running!", port=5001)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
