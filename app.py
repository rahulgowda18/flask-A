from flask import Flask, jsonify, render_template, request, redirect, url_for
from pymongo import MongoClient
import json

app = Flask(__name__)

# ---------------------------
# MongoDB Atlas configuration
# ---------------------------
MONGO_URI = ("mongodb+srv://dummy:1234@tram.3jglkqv.mongodb.net/?appName=tram")
client = MongoClient(MONGO_URI)
db = client["mydatabase"]
collection = db["formdata"]

# ---------------------------
# 1. API route that reads data from file
# ---------------------------
@app.route("/api", methods=["GET"])
def api():
    with open("data.json", "r") as f:
        data = json.load(f)
    return jsonify(data)

# ---------------------------
# 2. Frontend form route
# ---------------------------
@app.route("/", methods=["GET", "POST"])
def form():
    error = None

    if request.method == "POST":
        try:
            name = request.form.get("name")
            email = request.form.get("email")

            if not name or not email:
                raise ValueError("All fields are required")

            collection.insert_one({
                "name": name,
                "email": email
            })

            return redirect(url_for("success"))

        except Exception as e:
            error = str(e)

    return render_template("form.html", error=error)

# ---------------------------
# Success page
# ---------------------------
@app.route("/success")
def success():
    return render_template("success.html")


if __name__ == "__main__":
    app.run(debug=True)
