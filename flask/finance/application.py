import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
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
        "SELECT * FROM users WHERE username=:username",
        username=username)
    print(f'user_in_table-query_res: {query_res}')

    try:
        if query_res[0]["username"] == username:
            print(f'{username} already in users table.')
            return True
    except Exception as e:
        print(f'{username} not in users table.')
        return False


# add a user to the users table
def register_user(username, pwd_hash):

    # Check if user already in table
    if user_in_table(username):
        return False

    add_res = db.execute(
        "INSERT INTO users (username, hash) VALUES (:username, :hash)",
        username=username, hash=pwd_hash)
    if not add_res:
        return False

    query_res = db.execute(
        "SELECT * FROM users WHERE username=:username",
        username=username)

    if query_res[0]["username"] != username:
        return False
    else:
        return query_res[0]["id"]

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

    # Query cash from user data
    query_res = db.execute(
        "SELECT cash FROM users WHERE id=:id",
        id=session["user_id"])
    print(f'/ cash-query_res: {query_res}')

    # Get portfolio of user
    user_portfolio = db.execute(
        "SELECT * FROM portfolio WHERE user_id=:user_id",
        user_id=user_id
    )
    print(f'/ user_portfolio: {user_portfolio}')

    if not user_portfolio:
        return apology("Sorry, no user portfolio present.", 200)

    # Process portfolio_user
    value_all = 0
    stocks = []
    for stock in portfolio_user:
        # destructure
        stock_key = stock[1]
        quantity = stock[2]
        # get current price
        url = (
            f"https://cloud.iexapis.com/stable/stock/{stock_key}/quote?token={API_KEY}"
        )
        res = requests.get(url=url)
        quote = res.json()
        price = quote["latestPrice"]
        # Total stock value
        total = price * quantity
        # Add to stocks
        stocks.append(
            {"stock": stock_key, "quantity": quantity, "price": price, "total": total}
        )
        # Increment total value
        value_all += stock[2] * price

    # return render_template("index.html", stocks=portfolio, cash=cash, total=grand_total)
    return apology("Sorry, no user portfolio present.", 200)



@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    return apology("TODO")


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
        #if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
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
    return apology("TODO")


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
        print(f'/register POST parameter are valide.')

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
        print(f'User: {username} registered and loged in.')
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
