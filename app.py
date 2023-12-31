import os
import datetime
from flask import Flask, render_template, request
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()


def create_app():
    app = Flask(__name__)
    client = MongoClient(os.getenv("MONGODB_URL"))
    app.db = client.Microbase

    entries = []

    @app.route("/", methods=["GET", "POST"])
    def home():
        print([e for e in app.db.entries.find({})])
        if request.method == "POST":
            content = request.form["content"]
            formattedDate = datetime.datetime.today().strftime("%Y-%m-%d")
            entries.append((content, formattedDate))
            app.db.entries.insert_one({"content": content, "date": formattedDate})
        mongo_entries_with_date = [
            (
                e["content"],
                e["date"],
                datetime.datetime.strptime(e["date"], "%Y-%m-%d").strftime("%b %d")
            )
            for e in app.db.entries.find({})
        ]
        return render_template("home.html", entries=mongo_entries_with_date), 201

    return app
