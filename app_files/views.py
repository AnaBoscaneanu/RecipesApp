import os

from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

from app_files.lib.helpers import apology, login_required

from . import app

from flask_sqlalchemy import SQLAlchemy

from app_files.models import Users, Recipes, Ingredients, Categories


# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure the max size for requests to be up to 5MB in size: 
app.config['MAX_CONTENT_LENGTH'] = 5120 * 5120
# Configure the list of approved file extensions:
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']
# Configure the upload path
app.config['UPLOAD_PATH'] = 'app_files/static/uploads'

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


db = SQLAlchemy()

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
@login_required
def add():
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        
        # Ensure the user submitted a recipe name
        recipeName = request.form.get("recipeName")   # Add check that the recipe name is not already in use
        if not recipeName:
            flash("You must provide a recipe name!")
            redirect("/add") 
        # Ensure the user submitted a short description
        recipeShort = request.form.get("recipeShort")
        if not recipeShort:
            flash("You must provide a short description")
            redirect("/add")
        # Ensure the user submitted  prep time and cooking time
        recipePrepTime = request.form.get("recipePrepTime")
        recipeCookingTime = request.form.get("recipeCookingTime")
        if not recipePrepTime or not recipeCookingTime:
            flash("You must provide both prepararion and cooking time!")
            redirect("/add")
        # Ensure the user submitted portions
        recipePortions = request.form.get("recipePortions")
        if int(recipePortions) < 1:
            flash("You must provide a valid number of portions")
            redirect("/add")        
        # Ensure the user submitted the first ingredient
        ingredient0 = request.form.get("ingredient0")
        if not ingredient0:
            flash("You must submit the first ingredient")
            redirect("/add")
        # Store the other submitted ingredients in a list
        ingredients = request.form.getlist("recipeIngredients")
        # Append ingredient0 to the list
        ingredients.append(ingredient0)        
        # Ensure the user submitted the directions
        recipeDirections = request.form.get("recipeDirections")
        if not recipeDirections:
            flash("You must submit directions of cooking!")
            redirect("/add")

        #Store the submitted categories
        categories = request.form.getlist("recipeCategory") 

        # Insert all input into database table Recipes (except image url)
        user_id = session["user_id"]
        record = Recipes(user_id, recipeName, "", recipeShort, recipePrepTime, recipeCookingTime, recipePortions, recipeDirections)
        db.session.add(record)
        db.session.commit()

        # Query for recipe_id
        recipe_rows = Recipes.query.filter_by(user_id=session["user_id"], name=recipeName).all()
        recipe_id = recipe_rows[0].recipe_id
        # Insert all input into database table Ingredients 
        for i in ingredients:
            record_ingredients = Ingredients(recipe_id, user_id, i)
            db.session.add(record_ingredients)
            db.session.commit()
        # Insert all input into database table Ingredients 
        for i in categories:
            record_categories = Categories(recipe_id, user_id, i)
            db.session.add(record_categories)
            db.session.commit()
        
        # Store the secured image on disk
        uploaded_file = request.files["recipeImage"]
        filename = secure_filename(uploaded_file.filename)
        if filename != '':
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in app.config['UPLOAD_EXTENSIONS']:
                abort(400)        
            uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], str(recipe_id) + ".jpg")) # rename the file with the recipe_id and save in folder static/uploads


        # Redirect user 
        flash("Recipe Added!")
        return redirect("/add")
    
    # User reached route via GET (as by clicking a link or via redirect)
    else:   
        rows = Users.query.filter_by(id=session["user_id"]).all()  
        return render_template("add.html", username=rows[0].username)
    
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
