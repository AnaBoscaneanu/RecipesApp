Project name: Web application for saving cooking recipes.
Used languages and tools: Python (Flask), SQLite 3 + Flask-SQLAlchemy, HTML, CSS + Bootstrap, Javascript
Development environment on local server and production environment on Heroku.

During the last few years, I have been experimenting with many new recipes for cooking. Usually, I saved the ones I liked by leaving the website in my phone's browser or bookmarking them on my computer.
After a while, I realized that I often forget about a part of them, because I do not have an interactive way to be reminded about them. With this in mind, I decided to look for a solution on my own.
The purpuse of this application is to help organizing your recipes, sort through all of them easily and never again forget they exist.
Using this web application, one can make a free account and save all the favourite recipes in the preffered way and easily look for them.

How the web application works:

When a user opens the website on the home directory, a landing page is being rendered, which presents information about the website. The user has the option to sign in or sign up.
After both signing in or signing up the user lands on his own home page, where he can start saving recipes by using a provided form.
The form can be found by clicking on the menu option Add Recipe or by clicking on the Add New Recipe button from the user's homepage.
All recipes are being saved and grouped by the categories that the user chose in the add form.
The user can find all the recipes sorted by name on the directory called My Recipes. There he has the option to go to specific categories or make a search using ingredient names.
When the user has more recipes saved, on the user's homepage he will see up to 6 most recently added recipes. On "My Recipes" he will find all saved recipes. Once a recipe is opened, the user has the options to edit or delete it.

How the application is built:

Structure:
The app code is refactored into separate files.
The project contains a folder I called app_files and several files that are not contained in that folder: .gitignore, Procfile, requirement.txt, wsgi.py and README.md
Inside the app_files folder I have the folders static and templates required for a flask app, a folder called lib for initializing a helpers.py file and the rest of the project files:
- __ini__.py
- webapp.py: entry point for the application
- views.py: contains all the routes of the app and view functions
- models.py: contains all the database models, using Flask SQLAlchemy
- helpers.py: functions build by me that are being used in the project
- recipe_app.db - SQLite database
The app is set to use SQLite when it's running locally in development mode and PostgreSQL when it's running in production mode on Heroku.

Information about front-end part:
- the website is built to be responsive, using both my own CSS and Bootstrap classes.
- all forms (login, register, add recipe) contain validation functions in Javascript (no empty fields, the password has several requirement, password and confirmation must match)
- Javascript functions for Add Recipe form:
    - replace the image field with the file uploaded by the user (size restricted to 5MB)
    - buttons for dynamically adding new fields for ingredients and for categories and the option to remove them.
- the search button is being disabled if there nothing written in the field

Information about back-end part:
- all routes except login, register and landing page contain the login_required decorator.
- register, login and add (recipe) functions contain back-end form validation, with returning a message to the user if there are errors.
- all queries to the database are written using Flask SQLAlchemy



