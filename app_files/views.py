import os

from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from app_files.lib.helpers import apology, login_required

from . import app

from flask_sqlalchemy import SQLAlchemy


# Configure the app to use SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipe_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app) # this variable, db, will be used for all SQLAlchemy commands

#Model for the users table
class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    hash = db.Column(db.String)

    # Defines the method that initializes the proprieties of the class in order to add a new record in the table
    def __init__(self, username, hash):
        self.username = username
        self.hash = hash


# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
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

# Define all the routes

@app.route("/")
def landing_page():
    return render_template("landing.html")

@app.route("/myhome")
@login_required
def myhome():
    # Query database for username
    rows = Users.query.filter_by(id=session["user_id"]).all()    
    return render_template("myhome.html", username=rows[0].username)

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "GET":         
        return render_template("add.html")
    
@app.route("/login", methods=["GET", "POST"])
def login():

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        username = request.form.get("username")
        if not username:
            flash("You must provide a username!")
            return redirect("/login")
        # Ensure password was submitted
        password = request.form.get("password")
        if not password:
            flash("You must provide a password")
            return redirect("/login")

        # Query database for username
        rows = Users.query.filter_by(username=username).all()    

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0].hash , request.form.get("password")):
            return render_template("login.html", no_user=1)

        # Remember which user has logged in
        session["user_id"] = rows[0].id

        # Redirect user to home page
        return redirect("/myhome")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

        
@app.route("/logout")
@login_required
def logout():
    # Forget any user_id
    session.clear()

    # Redirect user to landing page
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
        
    # Forget any user_id
    session.clear()
    
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        username = request.form.get("username")
        if not username:
            flash("You must provide a username!")
            return redirect("/register")
        # Ensure the username doesn't already exist
        rows_users = Users.query.filter_by(username=username).all()
        if len(rows_users) != 0:
            return render_template("register.html", taken_username=1)
        # Ensure password was submitted
        password = request.form.get("password")
        if not password:
            flash("You must provide a password")
            return redirect("/register")
        # Ensure password confirmation was submitted
        confirmation = request.form.get("confirmation")
        if not confirmation:
            flash("You must confirm your password!")
            return redirect("/register")
        # Ensure the password and confirmation match
        if password != confirmation:
            flash("Your password does not match!")
            return redirect("/register")
        
        # Hash the password
        hash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)

        # Insert new user into the database
        record = Users(username, hash)
        db.session.add(record)
        db.session.commit()

        # Query database for username
        rows = Users.query.filter_by(username=username).all()
        session["user_id"] = rows[0].id

        # Redirect to users homepage and flash an alert
        flash("Registered")
        return redirect("/myhome")
    
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")
        


# Define error handler !! TO BE REVIEWED !!
def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError() 
    return apology(e.name, e.code) #change the way the error notifications are being returned to the user

# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
