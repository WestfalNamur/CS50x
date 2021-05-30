import os

import requests
import json
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
#db = SQL("sqlite:///finance.db")
db = sqlite3.connect('finance.db', check_same_thread=False)

# db.execute(    "CREATE TABLE IF NOT EXISTS portfolio( id integer PRIMARY KEY,  )")

# Add new portfolio tabel to db if not existing
return apology("you do not have enough cash for this transaction"

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks

    Complete the implementation of index in such a way that it displays an HTML
    table summarizing, for the user currently logged in, which stocks the user
    owns, the numbers of shares owned, the current price of each stock, and the
    total value of each holding (i.e., shares times price). Also display the
    user’s current cash balance along with a grand total (i.e., stocks’ total
    value plus cash).

    - Odds are you’ll want to execute multiple SELECTs. Depending on how you
    implement your table(s), you might find GROUP BY HAVING SUM and/or WHERE
    of interest.
    - Odds are you’ll want to call lookup for each stock.
    """

    # Destructure

    user_id = session["user_id"]

    # Query cash from user data

    results = db.execute(
        "SELECT cash FROM users WHERE id = :id",
        {"id": user_id}
    ).fetchall()
    cash = results[0][0]

    # Get user portfolio. Stocks owned, number of shares, current price and
    # thier the value of each holding.

    #portfolio = db.execute(
    #    ".schema"
    #).fetchall()
    #print('******************************************************')
    #print(portfolio)



    return apology("TODO")


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock

    Complete the implementation of buy in such a way that it enables a user
    to buy stocks.

    - Require that a user input a stock’s symbol, implemented as a text field
    whose name is symbol. Render an apology if the input is blank or the symbol
    does not exist (as per the return value of lookup).
    - Require that a user input a number of shares, implemented as a text field
    whose name is shares. Render an apology if the input is not a positive
    integer.
    - Submit the user’s input via POST to /buy.
    - Odds are you’ll want to call lookup to look up a stock’s current price.
    - Odds are you’ll want to SELECT how much cash the user currently has in
    users.
    - Add one or more new tables to finance.db via which to keep track of the
    purchase. Store enough information so that you know who bought what at\
    whatprice and when.
        * Use appropriate SQLite types.
        * Define UNIQUE indexes on any fields that should be unique.
        * Define (non-UNIQUE) indexes on any fields via which you will search
        (as via SELECT with WHERE).
    - Render an apology, without completing a purchase, if the user cannot
    afford the number of shares at the current price.
    - When a purchase is complete, redirect the user back to the index page.
    - You don’t need to worry about race conditions (or use transactions).
    Once you’ve implemented buy correctly, you should be able to see users’
    purchases in your new table(s) via sqlite3 or phpLiteAdmin.
    """

    # if user reached route via POST (as by submitting a form via POST)

    if request.method == "POST":

        # Destructure request data

        stock = request.form.get("stock")
        shares = request.form.get("shares")
        API_KEY = os.environ.get("API_KEY")
        user_id = session["user_id"]

        # Check if valied

        if (stock is None) or (shares is None):
            return apology("Please provide stock-symbol and number of shares")

        if not int(shares) >= 0:
            return apology("Invalid number of shares.")

        # Lookup stock data

        url = f'https://cloud.iexapis.com/stable/stock/{stock}/quote?token={API_KEY}'
        r = requests.get(url=url)
        quote = r.json()

        # Check if valid

        if quote is None:
            return apology("Stock symbol not valid.")

        # Destructure quote

        price = quote["latestPrice"]

        # Calculate Cost

        cost = int(shares) * price

        # Evaluate if user has enough cash
            
        results = db.execute(
            "SELECT cash FROM users WHERE id = :id",
            {"id": user_id}
        ).fetchall()
        user_cash = results[0][0]
        if cost > user_cash:
            return apology("Not enough cash for transaction.")
            
        # Create table when creating app
        # Continue
        
        


    # else if user reached route via GET (as by clicking a link or via redirect)

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    return apology("TODO")


@app.route("/login", methods=["GET", "POST"])
def login():

    # Forget any user_id

    session.clear()

    # User reached route via POST (as by submitting a form via POST)

    if request.method == "POST":

        # Ensure username was submitted

        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted

        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username

        rows = db.execute(
            "SELECT * FROM users WHERE username = :username",
            {"username": request.form.get("username")}
        ).fetchall()

        # Ensure username exists and password is correct

        if len(rows) != 1 or not check_password_hash(rows[0][2], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in

        session["user_id"] = rows[0][0]

        # Redirect user to home page

        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)

    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote.
    - Require that a user input a stock’s symbol, implemented as a text field
    whose name is symbol.
    - Submit the user’s input via POST to /quote.
    - Odds are you’ll want to create two new templates (e.g., quote.html and
    quoted.html). When a user visits /quote via GET, render one of those
    templates, inside of which should be an HTML form that submits to
    /quote via POST. In response to a POST, quote can render that second
    template, embedding within it one or more values from lookup.
    """

    # User reached route via POST (as by submitting a form via POST)

    if request.method == "POST":

        # Destructure POST

        stock = request.form.get("stock")

        # ensure stock data was submited

        if not stock:
            return apology("must provide stock symbol")

        # pull stock quote from yahoo finance

        stock_quote = lookup(stock)

        # Check if stock quote is valid

        if stock_quote is None:
            return apology("Stock symbol not valid, please try again")

        # If valide render template

        else:
            return render_template("quoted.html", stock_quote=stock_quote)

    # User reached route via GET (as by clicking a link or via redirect)

    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user."""

    # if user reached route via POST (as by submitting a form via POST)

    if request.method == "POST":

        # Destructure POST

        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("password")

        # Check if user has sent all required data.
        # Include if password and confirmation are the equal.

        if not username:
            return apology("Please provide as username.", 403)
        if not password:
            return apology("Please provide a password.", 403)
        if not confirmation:
            return apology("Please provide a confirmation.", 403)
        if not confirmation == password:
            return apology("Password and confirmation must be the same.", 403)

        # hash password

        pwd_hash = generate_password_hash(password)

        # Add user to db; Returns None if username already taken

        result = db.execute(
            "INSERT INTO users (username, hash) VALUES (:username, :hash)",
            {"username":username, "hash":pwd_hash}
        ).fetchall()

        # Return apology if username already taken; a.k.a result == None;

        if result is None:
            return apology("Username already exists.", 403)

        # Check if successfull added

        rows = db.execute(
            "SELECT * FROM users WHERE username = :username",
            {"username": username}
        ).fetchall()

        if not rows[0][1] == username:
            return apology("Username could not be added to db.", 403)

        # Remember user-id

        session["user_id"] = rows[0][0]

        # Redirect to homepage

        print("DONE: Registration")
        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    return apology("TODO")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
