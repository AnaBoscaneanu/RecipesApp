import os
import sys

import datetime

from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

from app_files.lib.helpers import apology, login_required, upload_file_to_s3

from . import app

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc

from app_files.models import Users, Recipes, Ingredients, Categories


# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure the max size for requests to be up to 5MB in size: 
app.config['MAX_CONTENT_LENGTH'] = 5120 * 5120
# Configure the list of approved file extensions:
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif', '.jpeg']
# Configure the upload path and s3 bucket
app.config['UPLOAD_PATH'] = 'app_files/static/uploads'
BUCKET='recipeimages'

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

current_year = datetime.datetime.now().year

# Define all the routes

@app.route("/")
def landing_page():
    
    return render_template("landing.html", current_year=current_year)

@app.route("/myhome")
@login_required
def myhome():
    # Query database for username
    rows = Users.query.filter_by(id=session["user_id"]).all()       

    # Query for all distinct categories of the user
    categories = Categories.query.with_entities(Categories.category.distinct()).filter_by(user_id=session["user_id"]).all()

    # Query for recipe information
    recipes = Recipes.query.filter_by(user_id=session["user_id"]).order_by(Recipes.recipe_id.desc()).limit(6)

    # Render template
    return render_template("myhome.html", current_year=current_year, categories=categories, recipes=recipes)

@app.route("/myrecipes", methods=["GET", "POST"])
@login_required
def myrecipes():
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Save the input from search
        search_ingr = request.form.get("searchIngredient")
        
        # Redirect the user to the search results
        return redirect("/search/" + search_ingr)

    # User reached route via GET (as by clicking a link or via redirect)
    else:    
        # Query database for username
        rows = Users.query.filter_by(id=session["user_id"]).all()   

        # Query for all distinct categories of the user
        categories = Categories.query.with_entities(Categories.category.distinct()).filter_by(user_id=session["user_id"]).all()

        # Query for recipe information
        recipes = Recipes.query.filter_by(user_id=session["user_id"]).order_by(Recipes.name).all()

        # Render template
        return render_template("myrecipes.html", current_year=current_year, categories=categories, recipes=recipes, recipe_nr=len(recipes))

@app.route("/myrecipes/<int:recipe_id>", methods=["GET", "POST"])
@login_required
def recipepage(recipe_id):
    # User reached route via POST for deleting a recipe
    if request.method == "POST":
        # Delete ingredients for the recipe
        ingredients = Ingredients.query.filter_by(recipe_id=recipe_id).all()
        for ingredient in ingredients:
            record = db.session.query(Ingredients).filter_by(recipe_id=recipe_id, ingredient=ingredient.ingredient).first()
            db.session.delete(record)
            db.session.commit()
        # Delete categories for the recipe
        categories = Categories.query.filter_by(recipe_id=recipe_id).all()
        for category in categories:
            record = db.session.query(Categories).filter_by(recipe_id=recipe_id, category=category.category).first()
            db.session.delete(record)
            db.session.commit()
        # Delete recipe record from the table Recipes
        recipe_record = db.session.query(Recipes).filter_by(recipe_id=recipe_id).first()
        db.session.delete(recipe_record)
        db.session.commit()

        # Redirect user to home page
        flash("Recipe Deleted!")
        return redirect('/myhome')
    # User reached route via GET
    else:
        # Query for recipe information
        recipe = Recipes.query.filter_by(recipe_id=recipe_id).all()
        ingredients = Ingredients.query.filter_by(recipe_id=recipe_id).all()
        categories = Categories.query.filter_by(recipe_id=recipe_id).all()

        # Render template
        return render_template("recipepage.html", current_year=current_year, recipe_id= recipe_id, recipe_name=recipe[0].name, recipe_image=recipe[0].image, description=recipe[0].description, prep_time=recipe[0].prep_time, cook_time=recipe[0].cooking_time, portions = recipe[0].portions, directions=recipe[0].directions, ingredients=ingredients, categories=categories)

@app.route("/myrecipes/<int:recipe_id>/edit", methods=["GET", "POST"])
@login_required
def editrecipe(recipe_id):
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        user_id = session["user_id"]

        # Ensure the user submitted a recipe name
        recipeName = request.form.get("recipeName")              
        if not recipeName:
            flash("You must provide a recipe name!")
            redirect(url_for('editrecipe', recipe_id=recipe_id)) 
        # Ensure the user submitted a short description
        recipeShort = request.form.get("recipeShort")
        if not recipeShort:
            flash("You must provide a short description")
            redirect(url_for('editrecipe', recipe_id=recipe_id))
        # Ensure the user submitted  prep time and cooking time
        recipePrepTime = request.form.get("recipePrepTime")
        recipeCookingTime = request.form.get("recipeCookingTime")
        if not recipePrepTime or not recipeCookingTime:
            flash("You must provide both preparation and cooking time!")
            redirect(url_for('editrecipe', recipe_id=recipe_id))
        # Ensure the user submitted portions
        recipePortions = request.form.get("recipePortions")
        if int(recipePortions) < 1:
            flash("You must provide a valid number of portions")
            redirect(url_for('editrecipe', recipe_id=recipe_id))
        # Store the submitted ingredients in a list
        ingredients = request.form.getlist("recipeIngredients")    
        # Ensure the user submitted the directions
        recipeDirections = request.form.get("recipeDirections")
        if not recipeDirections:
            flash("You must submit directions of cooking!")
            redirect(url_for('editrecipe', recipe_id=recipe_id))

        # Store the submitted categories
        categories = request.form.getlist("recipeCategory") 

        # Store the secured image on disk, upload in AWS S3 and save url in a variable
        file = request.files["recipeImage"]
                
        if file.filename != '':
            
            file_ext = os.path.splitext(file.filename)[1]
            if file_ext not in app.config['UPLOAD_EXTENSIONS']:
                # abort(400) 
                sys.exit('invalid file')
            filename = secure_filename(file.filename)
            newname = recipeName + str(user_id) + ".jpg" # change filename to recipe name+user id
            file.save(os.path.join(app.config['UPLOAD_PATH'], newname)) # to rename the file  save in folder static/uploads
            # Upload file to s3 bucket and get the file url
            url = upload_file_to_s3(f"app_files/static/uploads/{newname}", BUCKET, newname)

        # Update all the fields for the recipe in the database
        # Insert all input into database table Recipes
        recipe = db.session.query(Recipes).filter_by(recipe_id=recipe_id).first()                     
        recipe.name = recipeName            
        if file.filename != '':
            recipe.image = url
        recipe.description = recipeShort
        recipe.prep_time = recipePrepTime
        recipe.cooking_time = recipeCookingTime
        recipe.portions = recipePortions
        recipe.directions = recipeDirections    
        db.session.commit()
       
        # Delete old ingredients for the recipe and insert the new ones into table Ingredients 
        ingredients_current = Ingredients.query.filter_by(recipe_id=recipe_id).all()
        for ingredient in ingredients_current:
            record = db.session.query(Ingredients).filter_by(recipe_id=recipe_id, ingredient=ingredient.ingredient).first()
            db.session.delete(record)
            db.session.commit()

        for i in ingredients:
            record_ingredients = Ingredients(recipe_id, user_id, i)
            db.session.add(record_ingredients)
            db.session.commit()

        # Delete old categories for the recipe and insert the new ones into database table Categories 
        categories_current = Categories.query.filter_by(recipe_id=recipe_id).all()
        for category in categories_current:
            record = db.session.query(Categories).filter_by(recipe_id=recipe_id, category=category.category).first()
            db.session.delete(record)
            db.session.commit()
        for i in categories:
            record_categories = Categories(recipe_id, user_id, i)
            db.session.add(record_categories)
            db.session.commit() 
        

        # Redirect user 
        flash("Recipe Updated!")
        return redirect(url_for('recipepage', recipe_id=recipe_id))

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        # Query database for username
        rows = Users.query.filter_by(id=session["user_id"]).all()

        # Query for recipe information
        recipe = Recipes.query.filter_by(recipe_id=recipe_id).all()
        ingredients = Ingredients.query.filter_by(recipe_id=recipe_id).all()
        result_recipe_categories = Categories.query.filter_by(recipe_id=recipe_id).all()

        recipe_categories = []
        for i in result_recipe_categories:
            recipe_categories.append(i.category)

        # Query for all the categories the user has
        category_list = ["Breakfast", "Soups", "Salads", "Fish", "Meat", "Chicken", "Vegetables", "Appetizers", "Side Dishes", "Pasta", "Sauces", "Desserts"]
        user_categories = Categories.query.with_entities(Categories.category.distinct()).filter_by(user_id=session["user_id"]).all()
        new_categories = []
        for i in user_categories:
            if i[0] not in category_list:
                category_list.append(i[0])
        # Render template
        return render_template("editrecipe.html", current_year=current_year, recipe_id= recipe_id, recipe_name=recipe[0].name, recipe_image=recipe[0].image, description=recipe[0].description, prep_time=recipe[0].prep_time, cook_time=recipe[0].cooking_time, portions = recipe[0].portions, directions=recipe[0].directions, ingredients=ingredients, category_list=category_list, recipe_categories=recipe_categories)

@app.route("/categories/<string:category>")
@login_required
def categorypage(category):

    # Query database for username
    rows = Users.query.filter_by(id=session["user_id"]).all()

    # Query for all distinct categories of the user
    categories = Categories.query.with_entities(Categories.category.distinct()).filter_by(user_id=session["user_id"]).all()

    # Query for recipes in the chosen category
    recipes_row = db.session.query(Recipes.recipe_id, Recipes.name, Recipes.description, Recipes.image).filter(Recipes.user_id==session["user_id"]).join(Categories).filter(Categories.category==category).all()

    # Render template
    return render_template("categorypage.html", current_year=current_year, categories=categories, recipes=recipes_row, category=category, recipe_nr=len(recipes_row))


@app.route("/search/<string:ingredient>")
@login_required
def search(ingredient):
    # Query for all distinct categories of the user
    categories = Categories.query.with_entities(Categories.category.distinct()).filter_by(user_id=session["user_id"]).all()

    # Query for recipes with the chosen ingredient
    recipes_row = db.session.query(Recipes.recipe_id, Recipes.name, Recipes.image, Recipes.description).distinct(Recipes.recipe_id).filter(Recipes.user_id==session["user_id"]).join(Ingredients).filter(Ingredients.ingredient.ilike("%" + ingredient.lower() + "%")).all()

    # Render template
    return render_template("categorypage.html", current_year=current_year, categories=categories, recipes=recipes_row, category=ingredient, recipe_nr=len(recipes_row))

@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        user_id = session["user_id"]
        
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
            flash("You must provide both preparation and cooking time!")
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

        # Store the submitted categories
        categories = request.form.getlist("recipeCategory") 

        # Store the secured image on disk, upload in AWS S3 and save url in a variable
        file = request.files["recipeImage"]
                
        if file.filename != '':
            
            file_ext = os.path.splitext(file.filename)[1]
            if file_ext not in app.config['UPLOAD_EXTENSIONS']:
                #abort(400) 
                sys.exit('invalid file')
            filename = secure_filename(file.filename)
            newname = recipeName + str(user_id) + ".jpg" # change filename to recipe name+user id
            file.save(os.path.join(app.config['UPLOAD_PATH'], newname)) # to rename the file  save in folder static/uploads
            # Upload file to s3 bucket and get the file url
            url = upload_file_to_s3(f"app_files/static/uploads/{newname}", BUCKET, newname)

        # Insert all input into database table Recipes
        
        record = Recipes(user_id, recipeName, url, recipeShort, recipePrepTime, recipeCookingTime, recipePortions, recipeDirections)
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
        # Insert all input into database table Categories 
        for i in categories:
            record_categories = Categories(recipe_id, user_id, i)
            db.session.add(record_categories)
            db.session.commit() 
        

        # Redirect user 
        flash("Recipe Added!")
        return redirect("/add")
    
    # User reached route via GET (as by clicking a link or via redirect)
    else:   
        rows = Users.query.filter_by(id=session["user_id"]).all()  
        # Query for the categories added by the user
        category_list = ["Breakfast", "Soups", "Salads", "Fish", "Meat", "Chicken", "Vegetables", "Appetizers", "Side Dishes", "Pasta", "Sauces", "Desserts"]
        categories = Categories.query.with_entities(Categories.category.distinct()).filter_by(user_id=session["user_id"]).all()
        new_categories = []
        for i in categories:
            if i[0] not in category_list:
                new_categories.append(i[0])

        return render_template("add.html", current_year=current_year, new_categories=new_categories, nr_new_categories= len(new_categories))
    
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
            return render_template("login.html", no_user=1, current_year=current_year)

        # Remember which user has logged in
        session["user_id"] = rows[0].id

        # Redirect user to home page
        return redirect("/myhome")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html", current_year=current_year)

        
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
        return render_template("register.html", current_year=current_year)
        


# Define error handler
def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError() 
    return apology(e.name, e.code) 

# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
