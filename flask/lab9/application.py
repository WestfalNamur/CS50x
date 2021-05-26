import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///birthdays.db")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        # Access request data

        name = request.form.get("name")
        month = request.form.get("month")
        day = request.form.get("day")

        # Add a birthday to the database

        db.execute("INSERT INTO birthdays (name, month, day) VALUES(?, ?, ?)", name, month, day)

        # Redirect to homepage

        return redirect("/")

    else:

        # Quey db for birthdays

        birthdays = db.execute("SELECT * FROM birthdays")

        # Hydrate and render page

        return render_template("index.html", birthdays=birthdays)


