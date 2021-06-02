import os
import requests
from datetime import datetime

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, session, request
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

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
db = SQL("sqlite:///finance.db")

# check if user is in users table
def user_in_table(username):

    query_res = db.execute(
        "SELECT * FROM users WHERE username=:username", username=username
    )
    print(f"user_in_table-query_res: {query_res}")

    try:
        if query_res[0]["username"] == username:
            print(f"{username} already in users table.")
            return True
    except Exception as e:
        print(f"{username} not in users table.")
        return False


# add a user to the users table
def register_user(username, pwd_hash):

    # Check if user already in table
    if user_in_table(username):
        return False

    add_res = db.execute(
        "INSERT INTO users (username, hash) VALUES (:username, :hash)",
        username=username,
        hash=pwd_hash,
    )
    if not add_res:
        return False

    query_res = db.execute(
        "SELECT * FROM users WHERE username=:username", username=username
    )

    if query_res[0]["username"] != username:
        return False
    else:
        return query_res[0]["id"]


def get_user_cash(user_id):
    result = db.execute("SELECT cash FROM users WHERE id=:id", id=session["user_id"])
    return result[0]["cash"]


def get_quote(stock_key):
    try:
        API_KEY = os.environ.get("API_KEY")
        url = (
            f"https://cloud.iexapis.com/stable/stock/{stock_key}/quote?token={API_KEY}"
        )
        res = requests.get(url=url)
        print(f"Got stock quote for {stock_key}")
        return res.json()
    except:
        return False


def update_user_cash(user_id, cost):
    original_cash = db.execute(
        "SELECT cash FROM users WHERE id=:id", id=session["user_id"]
    )
    db.execute(
        "UPDATE users SET cash=cash-:cost WHERE id=:id",
        cost=cost,
        id=user_id,
    )
    updated_cash = db.execute(
        "SELECT cash FROM users WHERE id=:id", id=session["user_id"]
    )
    cash_t0 = original_cash[0]["cash"]
    cash_t1 = updated_cash[0]["cash"]
    print(f"user cash was: {cash_t0} is now {cash_t1}")
    if cash_t0 != cash_t1:
        return False
    else:
        return True


def get_user_shares_of_stock(user_id, stock):
    quantity = db.execute(
        "SELECT quantity FROM portfolio WHERE user_id=:user_id AND stock=:stock",
        user_id=user_id,
        stock=stock,
    )
    return quantity[0]["quantity"]


def add_stocks_2_portfolio(user_id, stock, quantity):

    # Log portfolio before adding new shares
    portfolio = db.execute("SELECT * FROM portfolio")
    print(f"/buy portfolio is:{portfolio}")

    # Get quantity of shares in portfolio
    user_shares = db.execute(
        "SELECT quantity FROM portfolio WHERE stock=:stock AND user_id=:user_id",
        stock=stock,
        user_id=user_id,
    )

    # Add new stocks to user portfolio
    if not user_shares:
        db.execute(
            "INSERT INTO portfolio (user_id, stock, quantity) VALUES (:user_id, :stock, :quantity)",
            user_id=user_id,
            stock=stock,
            quantity=quantity,
        )
    # or update existing ones
    else:
        db.execute(
            "UPDATE portfolio SET quantity=quantity + :quantity WHERE user_id = :user_id AND stock = :stock",
            user_id=user_id,
            stock=stock,
            quantity=quantity,
        )

    # Log portfolio before adding new shares
    portfolio = db.execute("SELECT * FROM portfolio")
    print(f"/buy portfolio is:{portfolio}")


# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    # Destructure
    user_id = session["user_id"]
    API_KEY = os.environ.get("API_KEY")

    # Get portfolio of user
    user_portfolio = db.execute(
        "SELECT * FROM portfolio WHERE user_id=:user_id", user_id=user_id
    )
    print(f"/ user_portfolio: {user_portfolio}")

    # Get user cash
    user_cash = get_user_cash(user_id)

    # Process portfolio
    portfolio_value = 0
    user_stocks = []
    for stock in user_portfolio:
        stock_key = stock["stock"]
        quantity = stock["quantity"]
        quote = get_quote(stock_key)
        price = quote["latestPrice"]
        total = price * quantity
        portfolio_value += total
        print(f"Process {stock_key} data")
        user_stocks.append(
            {"stock": stock_key, "quantity": quantity, "price": price, "total": total}
        )

    return render_template(
        "index.html", stocks=user_stocks, cash=user_cash, total=portfolio_value
    )


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    if request.method == "POST":

        # Destructure request data
        stock = request.form.get("symbol")
        shares = request.form.get("shares")
        API_KEY = os.environ.get("API_KEY")
        user_id = session["user_id"]

        # Check if valied
        if (stock is None) or (shares is None):
            return apology("Please provide stock-symbol and number of shares")
        try:
            shares = int(shares)
            if not int(shares) >= 0:
                return apology("Invalid number of shares.")
        except:
            return apology("Invalid type.")

        # Lookup stock data
        quote = get_quote(stock)

        # Check if valid
        if not quote:
            return apology("Stock symbol not valid.")

        # Destructure quote
        price = quote["latestPrice"]

        # Calculate Cost
        cost = shares * price

        # Evaluate if user has enough cash
        user_cash = get_user_cash(user_id)
        if cost > user_cash:
            return apology("Not enough cash for transaction.")

        # Update user cash
        update_user_cash(user_id=user_id, cost=cost)

        # Add transaction to transactions table
        transactions_add = db.execute(
            "INSERT INTO transactions (user_id, stock, quantity, price, date) VALUES (:user_id, :stock, :quantity, :price, :date)",
            user_id=user_id,
            stock=stock,
            quantity=shares,
            price=price,
            date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )

        # Add stocks to portfolio
        add_stocks_2_portfolio(user_id=user_id, stock=stock, quantity=shares)

        return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    return apology("TODO")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Destructure
        username = request.form.get("username")
        password = request.form.get("password")

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        # Ensure username exists and password is correct
        # if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
        #    return apology("invalid username and/or password", 403)
        if len(rows) != 1 or not (rows[0]["hash"] == password):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

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
    """Get stock quote."""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Destructure POST
        stock = request.form.get("symbol")

        # ensure stock data was submited
        if not stock:
            return apology("must provide stock symbol")

        # pull stock quote from yahoo finance
        stock_quote_raw = get_quote(stock_key=stock)
        if not stock_quote_raw:
            return apology("Stock symbol not valid, please try again")
        print(f"stock_quote_raw: {stock_quote_raw}")

        try:
            stock_quote = {}
            stock_quote["symbol"] = stock_quote_raw["symbol"]
            stock_quote["price"] = stock_quote_raw["latestPrice"]
        except:
            return apology("Stock symbol not valid, please try another.")

        # If valide render template
        else:
            return render_template("quoted.html", stock_quote=stock_quote)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":

        # Destructure
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Check post-args
        if not username:
            return apology("Please provide as username.", 400)
        if not password:
            return apology("Please provide a password.", 400)
        if not confirmation:
            return apology("Please provide a confirmation.", 400)
        if not confirmation == password:
            return apology("Password and confirmation must be the same.", 400)
        print(f"/register POST parameter are valide.")

        # Gen pwd-hash
        # pwd_hash = generate_password_hash(password)
        pwd_hash = password

        # Add user to db
        user_id = register_user(username=username, pwd_hash=pwd_hash)

        # Reject is something went wrong or user exists
        if not user_id:
            return apology("User exists.")

        # Remember user-id
        session["user_id"] = user_id

        # Redirect to homepage
        print(f"User: {username} registered and loged in.")
        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":

        # Destructure
        API_KEY = os.environ.get("API_KEY")
        user_id = session["user_id"]
        stock = request.form.get("symbol")
        shares = int(request.form.get("shares"))

        # Ensure both are valid
        if (not stock) or (not shares):
            return apology("Provide stock symbol and number of shares.")
        if shares <= 0:
            return apology("Number of shares must be large then 0.")

        # Get available shares for sale
        n_available_shares = get_user_shares_of_stock(user_id, stock)

        # Check if quantity of shares is large eneough
        if n_available_shares < shares:
            return apology("Not enough shares.")

        # Check if stock is tradable
        quote = get_quote(stock)
        if not quote:
            return apology("Share not traded.")

        # Calc cash yield of transaction
        price = quote["latestPrice"]
        cash_yield = price * shares

        # Update cash ammount in users table
        db.execute(
            "UPDATE users SET cash=cash-:cash_yield WHERE id=:id",
            cash_yield=cash_yield,
            id=user_id,
        )

        # Add transaction to transactions table
        transactions_add = db.execute(
            "INSERT INTO transactions (user_id, stock, quantity, price, date) VALUES (:user_id, :stock, :quantity, :price, :date)",
            user_id=user_id,
            stock=stock,
            quantity=shares,
            price=price,
            date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )

        # update share qunatity
        db.execute(
            "UPDATE portfolio SET quantity=quantity - :quantity WHERE user_id = :user_id AND stock = :stock",
            quantity=shares,
            user_id=user_id,
            stock=stock,
        )

        # Redirect to index
        return redirect("/")

    else:

        user_id = session["user_id"]
        portfolio_user = db.execute(
            "SELECT stock FROM portfolio WHERE user_id=:user_id", user_id=user_id
        )
        print(" ")
        print(portfolio_user)
        stocks = [stock["stock"] for stock in portfolio_user]

        return render_template("sell.html", stocks=stocks)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
