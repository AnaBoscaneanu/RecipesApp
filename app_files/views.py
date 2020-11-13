import os
import helpers

from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps

from . import app

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

# Define decorator
def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


# Define all the routes

@app.route("/")
def landing_page():
    return render_template("landing.html")
    
@app.route("/login", methods=["GET", "POST"])
def login():

    # Forget any user_id
    session.clear()
    # User reached route via GET (as by clicking a link or via redirect)
    if request.method == "GET":
        return render_template("login.html")


        
@app.route("/logout")
def logout():
    # Forget any user_id
    session.clear()

    # Redirect user to landing page
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
        
    # Forget any user_id
    session.clear()

    # User reached route via GET (as by clicking a link or via redirect)
    if request.method == "GET":
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