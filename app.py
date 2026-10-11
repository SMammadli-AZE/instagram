from flask import Flask, request, jsonify, send_from_directory
import os

app = Flask(__name__)
DB_PATH = os.path.join(os.path.dirname(__file__), "database.txt")

def exact_match_exists(username, password):
    if not os.path.exists(DB_PATH):
        return False
    with open(DB_PATH) as f:
        for line in f:
            line = line.strip()
            if line == f"{username}:{password}":
                return True
    return False

def add_account(username, password):
    with open(DB_PATH, "a") as f:
        f.write(f"{username}:{password}\n")

@app.route("/")
def serve_login_page():
    return send_from_directory(os.path.dirname(__file__), "login.html")

@app.route("/<path:filename>")
def serve_static_file(filename):
    return send_from_directory(os.path.dirname(__file__), filename)

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username", "")
    password = data.get("password", "")

    if not username or not password:
        return jsonify({"success": False, "message": "Enter a username and password."}), 400

    if exact_match_exists(username, password):
        return jsonify({"success": True, "message": f"Welcome back, {username}!", "created": False})
    else:
        add_account(username, password)
        return jsonify({"success": True, "message": f"New account created for {username}.", "created": True})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
