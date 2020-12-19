import os
import requests
import urllib.parse
import boto3, botocore

from flask import redirect, render_template, request, session
from functools import wraps


# Connect client to s3 service
s3 = boto3.resource('s3')

# Define a function that uploads a file to s3 bucket
def upload_file_to_s3(filename, bucket, key, acl="public-read"):
    try:
        s3.meta.client.upload_file(filename, bucket, key, ExtraArgs={"ACL": acl, "ContentType": "image/jpeg"})

    except Exception as e:
        # Catch all exeptions
        print("Something Went Wrong: ", 2)
        return e
    
    # after upload to bucket, return filename of the uploaded file
    AWS_LOCATION = 'http://{}.s3.eu-north-1.amazonaws.com/'.format(bucket)
    upload_url = "{}{}".format(AWS_LOCATION, key)
    return upload_url

# Define apology message in case of errors   
def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code

# Define login required decorator
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

