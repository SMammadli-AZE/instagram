from flask import Flask, request, jsonify, send_from_directory
import os

app = Flask(__name__)
DB_PATH = os.path.join(os.path.dirname(__file__), "database.txt")

def load_users():
    """Read database.txt into a dict: {username: password}"""
    users = {}
    if os.path.exists(DB_PATH):
        with open(DB_PATH) as f:
            for line in f:
                line = line.strip()
                if ":" in line:
                    username, password = line.split(":", 1)
                    users[username] = password
    return users

@app.route("/")
def serve_login_page():
    return send_from_directory(os.path.dirname(__file__), "login.html")

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username", "")
    password = data.get("password", "")

    users = load_users()
    if username in users and users[username] == password:
        return jsonify({"success": True, "message": f"Welcome, {username}!"})
    else:
        return jsonify({"success": False, "message": "Incorrect username or password."}), 401

if __name__ == "__main__":
    app.run(debug=True, port=5000)