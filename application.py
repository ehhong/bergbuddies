from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, timedelta
from datetime import date, time
from pytz import timezone

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
# TODO
db = SQL("sqlite:///bergbuddies.db")

@app.route("/")
def home():
    """Show home page with berg layout"""
    return render_template("home.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        # check that all fields are filled
        if not request.form.get("name"):
            return apology("must provide name")
        if not request.form.get("username"):
            return apology("must provide username")

        if not request.form.get("password"):
            return apology("must provide password")
        # check that confirmation is entered
        if not request.form.get("confirmation"):
            return apology("must provide confirmation")
        # check that password matches confirmation
        if request.form.get("password") != request.form.get("confirmation"):
            return apology("confirmation must match password")

        # remember hashed form of password
        hashPass = generate_password_hash(request.form.get("password"))

        # input new user info into table users
        result = db.execute("INSERT INTO users (name, username, hash) VALUES (:name, :username, :hashPass)",
                            name=request.form.get("name"), username=request.form.get("username"), hashPass=hashPass)

        # usernames are a unique field in users, return error if username already exists (execute will fail)
        if not result:
            return apology("username already taken")

        # store user_id in session (to keep user logged in)
        session["user_id"] = result
        session["logged_in"] = True

        return redirect("/")
    else: # if get method
        return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password")

        # Remember which user has logged in
        session["user_id"] = rows[0]["userID"]
        session["logged_in"] = True

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

@app.route("/checkin", methods=["GET", "POST"])
@login_required
def checkin():
    """check user into berg table (user is in berg)"""
    if request.method == "POST":
        if not request.form.get("tableRow"):
            return apology("must provide table row")
        if not request.form.get("tableCol"):
            return apology("must provide table column")

        tableID = request.form.get("tableRow") + str(request.form.get("tableCol"))

        # add user to berg table
        currentTime = datetime.now(timezone('US/Eastern')).time()
        result = db.execute("INSERT INTO berg (userID, tableID, checkInTime) VALUES (:userID, :tableID, :checkInTime)",
                            userID=session["user_id"], tableID=tableID, checkInTime=currentTime)
        # userIDs are a unique field in berg (user cannot check in twice simultaneously), return error if userID already exists (execute will fail)
        if not result:
            return apology("user already checked in")

        # update tables table
        tableUpdate = db.execute("UPDATE tables SET count = count + 1 WHERE tableID=:tableID", tableID=tableID)
        if not tableUpdate:
            # if tableID not in tables, add it
            db.execute("INSERT INTO tables (tableID, count) VALUES (:tableID, :count)", tableID=tableID, count=1)

        # return to home page
        return redirect("/")
    else:
        return render_template("checkin.html")

@app.route("/checkout", methods=["GET", "POST"])
@login_required
def checkout():
    # record when the user entered annenberg
    start_time_dictionary = db.execute("SELECT checkInTime FROM berg WHERE userID=:userID", userID=session["user_id"])
    if not start_time_dictionary:
        return apology("user isn't checked in")
    FMT = '%H:%M:%S'
    start_time_string = start_time_dictionary[0]["checkInTime"]
    start_times = datetime.strptime(start_time_string, FMT)
    start_time = timedelta(hours=start_times.hour, minutes=start_times.minute, seconds=start_times.second)

    # record current time as endtime and calculate elapsed time
    end_time_time = datetime.now(timezone('US/Eastern')).time().strftime(FMT)
    end_time_formatted = datetime.strptime(end_time_time, FMT)
    end_time = timedelta(hours=end_time_formatted.hour, minutes=end_time_formatted.minute, seconds=end_time_formatted.second)
    elapsed_time = end_time - start_time # timedelta

    # using user_id, update users table by adding current elapsed time to the total eating time and incrementing numMeals
    # get the current total eating time for the user from the database (timedelta)
    total_elapsed_time_string1 = db.execute("SELECT totalEatingTime FROM users WHERE userID=:userID", userID=session["user_id"])
    if total_elapsed_time_string1[0]["totalEatingTime"] == None:
        total_elapsed_time = timedelta(hours=0, minutes=0, seconds=0)
    else:
        total_elapsed_time_string2 = datetime.strptime(total_elapsed_time_string1[0]["totalEatingTime"], "%H:%M:%S")
        total_elapsed_time = timedelta(hours=total_elapsed_time_string2.hour, minutes=total_elapsed_time_string2.minute, seconds=total_elapsed_time_string2.second)
    total_elapsed_time = total_elapsed_time + elapsed_time
    formatted_total_string = str(total_elapsed_time)
    db.execute("UPDATE users SET totalEatingTime=:total_elapsed_time WHERE userID=:userID", userID=session["user_id"], total_elapsed_time=formatted_total_string)

    # increment number of meals
    current_meals_db = db.execute("SELECT numMeals FROM users WHERE userID=:userID", userID=session["user_id"])
    # if this is the user's first meal, set the amount of current meals to 1 (i.e. incrementing from 0)
    if current_meals_db[0]["numMeals"] == None:
        current_meals = 1
    else:
        current_meals = current_meals_db[0]["numMeals"]
        current_meals = current_meals + 1
    #update the database to increment current number of meals
    db.execute("UPDATE users SET numMeals=:current_meals WHERE userID=:userID", userID=session["user_id"], current_meals=current_meals)

    # using user_id, update users table by recalculating the user's average eating time in seconds
    eating_duration = total_elapsed_time.total_seconds()
    avg_eating_time = (total_elapsed_time/current_meals).total_seconds()
    db.execute("UPDATE users SET eatingTime=:avg_eating_time WHERE userID=:userID", userID=session["user_id"], avg_eating_time=avg_eating_time)

    # get user's table number
    tableID = db.execute("SELECT tableID FROM berg WHERE userID = :userID", userID=session["user_id"])[0]["tableID"]
    # decrease count on user's table by 1
    tableUpdate = db.execute("UPDATE tables SET count = count - 1 WHERE tableID=:tableID", tableID=tableID)
    if not tableUpdate:
        return apology("user isn't checked in (not sitting @ a table)")

    # remove user from berg table (user is no longer in berg)
    db.execute("DELETE FROM berg WHERE userID = :userID", userID=session["user_id"])
    start_time = start_time_dictionary[0]["checkInTime"]

    return redirect("/")

@app.route("/mealstage", methods=["GET", "POST"])
def mealstage():
    # called on-click when user clicks a certain table
    # calculate how far all the users at the table are into their meal
    tableID = "A1" #TEMPORARY. Assume user clicked on table "A1"
    all_users = db.execute("SELECT berg.userID, users.name FROM berg INNER JOIN users ON berg.userID=users.userID WHERE tableID = :tableID", tableID=tableID)
    for user in all_users:
        name = user["name"]
        userID = user["userID"]
        FMT = '%H:%M:%S'
        # find time since user entered Annenberg in datetime format
        checkinTime_db = db.execute("SELECT checkInTime FROM berg WHERE userID=:userID", userID=userID)
        checkinTime = datetime.strptime(checkinTime_db[0]["checkInTime"], FMT)
        checkinTime_delta = timedelta(hours=checkinTime.hour, minutes=checkinTime.minute, seconds=checkinTime.second)
        # find current time in datetime format
        currentTime = datetime.now(timezone('US/Eastern'))
        currentTime_delta = timedelta(hours=currentTime.hour, minutes=currentTime.minute, seconds=currentTime.second)
        # find difference between user check-in time and current time
        diff = currentTime_delta - checkinTime_delta
        # find user's average meal time
        avg_time_db = db.execute("SELECT eatingTime FROM users WHERE userID=:userID", userID=userID)
        avg_time = avg_time_db[0]["eatingTime"]
        # find meal-completion percentage
        percentage = (diff.total_seconds()/avg_time)*100

@app.route("/tableview", methods=["GET", "POST"])
@login_required
def tableview():
    """display list of users in berg as a table"""
    all_users = db.execute("SELECT berg.userID, users.name, users.eatingTime, berg.checkInTime, berg.tableID FROM berg INNER JOIN users ON berg.userID = users.userID")
    return render_template("table.html", all_users=all_users)

def errorhandler(e):
    """Handle error"""
    # dunno how to do this or what this is for
    return None

# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)