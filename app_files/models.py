from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Model for the users table
class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable = False)
    hash = db.Column(db.String, nullable = False)

    # Defines the method that initializes the proprieties of the class in order to add a new record in the table
    def __init__(self, username, hash):
        self.username = username
        self.hash = hash

# Model for recipes table
class Recipes(db.Model):
    __tablename__ = "recipes"
    recipe_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
    name = db.Column(db.String(60), nullable = False)
    image = db.Column(db.Text)
    description = db.Column(db.String(120), nullable = False)
    prep_time = db.Column(db.String(10), nullable = False)
    cooking_time = db.Column(db.String(10), nullable = False)
    portions = db.Column(db.Integer, nullable = False)
    directions = db.Column(db.Text, nullable = False)

    def __init__(self, user_id, name, image, description, prep_time, cooking_time, portions, directions):
        self.user_id = user_id
        self.name = name
        self.image = image
        self.description = description
        self.prep_time = prep_time
        self.cooking_time = cooking_time
        self.portions = portions
        self.directions = directions

# Model for ingredients table
class Ingredients(db.Model):
    __tablename__ = "ingredients"
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.recipe_id'), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
    ingredient = db.Column(db.Text, nullable = False)

    def __init__(self, recipe_id, user_id, ingredient):
        self.recipe_id = recipe_id
        self.user_id = user_id
        self.ingredient = ingredient

# Model for categories table
class Categories(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.recipe_id'), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
    category = db.Column(db.Text, nullable = False)

    def __init__(self, recipe_id, user_id, category):
        self.recipe_id = recipe_id
        self.user_id = user_id
        self.category = category

