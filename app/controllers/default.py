from app import app


@app.route("/")
def index():
    return "<h1>teste teste teste</h1>"
