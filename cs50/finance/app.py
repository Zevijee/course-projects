import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")

def to_int(x):
    try:
        result = int(x)
        if result <= 0:
            return apology("shares must be more then 0", 400)
        return result
    except ValueError:
        return apology("shares must be of type int", 400)


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    users_stocks = db.execute("SELECT * FROM stocks WHERE owner = ?", session["user_id"])
    user = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
    total_value = 0
    # getting value of stocks
    for row in users_stocks:
        price_lookup = lookup(row["stock_name"])
        price = price_lookup["price"]
        row["price"] = usd(price)
        stock_value = price * row["shares_owned"]
        row["value"] = usd(stock_value)
        total_value += stock_value
    total_value_usd = usd(total_value)
    available_cash = usd(user[0]["cash"])
    return render_template("index.html", users_stocks=users_stocks, total_value=total_value_usd, available_cash=available_cash)



@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    id = session["user_id"]
    # check method
    if request.method == "POST":
        # get the info of the request stock
        symbal = request.form.get("symbol")
        stock_info = lookup(symbal)
        if stock_info:
            shares = to_int(request.form.get("shares"))
            price_per_stock = stock_info["price"]

            try:
                total_price = shares * price_per_stock
            except TypeError:
                return apology("shares must be of type int and more then 0", 400)


            cash = db.execute("SELECT cash FROM users WHERE id = ?", id)
            if cash[0]["cash"] - total_price < 0:
                return apology("you cant afford this stock", 400)
            db.execute("UPDATE users SET cash = cash - ? WHERE id = ?" , total_price,  id)
            potential_stock = db.execute("SELECT stock_name FROM stocks WHERE owner = ? AND stock_name = ?", id, symbal)

            if potential_stock:
                db.execute("UPDATE stocks SET shares_owned = shares_owned + ? WHERE owner = ?" , shares,  id)
            else:
                db.execute("INSERT INTO stocks (owner, stock_name, shares_owned) VALUES (?, ?, ?)", id, symbal, shares)

            db.execute("INSERT INTO logs (id, log_transaction, stock_name, shares, transaction_price) VALUES (?, ?, ?, ?, ?)", id, "bought", symbal, shares, price_per_stock)

            return redirect("/")

        else:
            return apology("invalid stock symbal", 400)


    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    history = db.execute("SELECT * FROM logs WHERE id = ?", session["user_id"])
    return render_template("history.html", logs=history)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

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
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
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
    # get users name
    row = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
    name = row[0]["username"]
    # check method
    if request.method == "POST":
        # get the info of the request stock
        symbal = request.form.get("symbol")
        stock_info = lookup(symbal)
        if stock_info:
            name = stock_info["name"]
            price = usd(stock_info["price"])
        else:
            return apology("invalid stock symbal", 400)

        return render_template("quote.html", stock_name=name, stock_price=price)

    else:
        return render_template("quote.html", name=name)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        re_enter_password = request.form.get("confirmation")

        # Ensure username was submitted
        if not username:
            return apology("must provide username", 400)

                # Ensure password was submitted
        elif not password:
            return apology("must provide password", 400)

        elif password != re_enter_password:
            return apology("password and re-enter password do not match", 400)

        else:
            current_usernames = db.execute("SELECT username FROM users")
            # Check if the username already exists in the current_usernames list
            for row in current_usernames:
                if row["username"] == username:
                    return apology("username already taken", 400)

            hashed_password = generate_password_hash(password)
            rows = db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hashed_password)


            # Redirect user to home page
            return redirect("/login")

    else:
        return render_template("register.html")

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        stock_name = request.form.get("symbol")
        if not stock_name:
            return apology("you must choose a stock name", 400)
        amount = to_int(request.form.get("shares"))
        if not amount:
            return apology("you must choose a amount of stock", 400)
        stock_info = lookup(stock_name)
        total_price = amount * stock_info["price"]
        stocks_owned = db.execute("SELECT shares_owned FROM stocks WHERE owner = ? AND stock_name = ?", session["user_id"], stock_name)
        stocks_owned_int = stocks_owned[0]["shares_owned"]
        if stocks_owned_int - amount < 0:
            return apology("you dont have that much stock to sell", 400)

        elif stocks_owned_int - amount == 0:
            db.execute("DELETE FROM stocks WHERE owner = ? AND stock_name = ?", session["user_id"], stock_name)

        else:
            db.execute("UPDATE stocks SET shares_owned = shares_owned - ? WHERE owner = ? AND stock_name = ?" , amount,  session["user_id"], stock_name)

        db.execute("INSERT INTO logs (id, log_transaction, stock_name, shares, transaction_price) VALUES (?, ?, ?, ?, ?)", session["user_id"], "sold", stock_name, amount, stock_info["price"])
        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?" , total_price,  session["user_id"])

        return redirect("/")

    else:
        users_stocks = db.execute("SELECT stock_name FROM stocks WHERE owner = ?", session["user_id"])
        return render_template("sell.html", stocks=users_stocks)
