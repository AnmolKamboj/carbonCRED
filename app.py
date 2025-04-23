from flask import Flask, render_template

def create_app():
    print("🚀 Dummy create_app() called")
    app = Flask(__name__)

    @app.route("/")
    def home():
        return render_template("index.html")

    return app
