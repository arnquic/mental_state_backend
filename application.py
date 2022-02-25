# -------------------------------------------------
# Imports and initilizations
# -------------------------------------------------
import models
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from logging import log
import os
import re
from alembic.op import create_table
import sqlalchemy
import jwt
from datetime import datetime, timezone

from flask import Flask, request
app = Flask(__name__)

CORS(app)

bcrypt = Bcrypt(app)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

models.db.init_app(app)

# -------------------------------------------------
# Routes and Route Functions
# -------------------------------------------------

# -----------------------------------------------
# Server Health Status


def health_status():
    try:
        # Return a status of 200 if this route is reached.
        return {"message": "Server is healthy."}, 200
    except Exception as e:
        print(e)
        return {"message": "The server is facing and exception."}, 400


app.route("/", methods=["GET"])(health_status)

# -----------------------------------------------
# Create a new User.


def create_user():
    try:
        # Search for a pre-existing user with the given email.
        existing_user = models.User.query.filter_by(
            email=request.json["email"]).first()
        # Handle the presence of an existing user.
        if existing_user:
            return {"message": "An account already exists with that email."}
        # Hash the password for the new user.
        hashed_pw = bcrypt.generate_password_hash(
            request.json["password"]).decode("utf-8")
        # Create the new user.
        new_user = models.User(
            firstName=request.json["first_name"],
            lastName=request.json["last_name"],
            email=request.json["email"],
            password=hashed_pw
        )
        print(new_user.to_json())
        # Add the new user to the database.
        models.db.session.add(new_user)
        # Commit the database updates.
        models.db.session.commit()
        # Create an encrypted authorization token before returning it to the client.
        encrypted_id = jwt.encode({"user_id": new_user.id}, os.environ.get(
            "JWT_SECRET"), algorithm="HS256")
        # Return the user data to the client.
        return {
            "user_info": new_user.to_json(),
            "summit_auth": encrypted_id
        }
    except sqlalchemy.exc.IntegrityError as err:
        print(err)
        return {"message": "All values must be provided."}, 400
    except Exception as err:
        print(err)
        return {"message": "Something unknown went wrong."}, 400


app.route("/user", methods=["POST"])(create_user)


# ------------------------------------------------
# Login an existing User.
def login_user():
    try:
        # Look for a user with the given email.
        user = models.User.query.filter_by(email=request.json["email"]).first()
        # Handle whether or not a user was found.
        if user:
            # Compare the found user's password to the given password.
            if (bcrypt.check_password_hash(user.password, request.json["password"])):
                # Create an encrypted authorization token before returning it to the client.
                encrypted_id = jwt.encode({"user_id": user.id}, os.environ.get(
                    "JWT_SECRET"), algorithm="HS256")
                # Return the user data to the client.
                return {
                    "user_info": user.to_json(),
                    "summit_auth": encrypted_id
                }
            else:
                # Return a message if the password is incorrect.
                return {"message": "The email/password combination was incorrect."}, 401
        else:
            # Return a message if no user is found.
            return {"message": "The email/password combination was incorrect."}, 404
    except Exception as err:
        print(err)
        return {"message": "Something unknown went wrong."}, 400


app.route("/user/login", methods=["POST"])(login_user)


# -------------------------------------------------
# Verify a returning User's authorization token.
def verify_user():
    try:
        # Decrypt the incoming authorization header.
        decrypted_id = jwt.decode(request.headers["Authorization"], os.environ.get(
            "JWT_SECRET"), algorithms=["HS256"])["user_id"]
        # Look for a user with the decrypted user id.
        user = models.User.query.filter_by(id=decrypted_id).first()
        # Handle whether a user was found.
        if user:
            # Create an encrypted authorization token before returning it to the client.
            encrypted_id = jwt.encode({"user_id": user.id}, os.environ.get(
                "JWT_SECRET"), algorithm="HS256")
            # Return the user data to the client.
            return {
                "user_info": user.to_json(),
                "summit_auth": encrypted_id
            }
        else:
            # Return a message if no user is found.
            return {"message": "Authorization failed."}, 404
    except Exception as err:
        print(err)
        return {"message": "Something unknown went wrong."}, 400


app.route("/user/verify", methods=["GET"])(verify_user)


# -------------------------------------------------
# Update an existing user's email and/or password information.
def update_user():
    try:
        # Decrypt the incoming authorization header.
        decrypted_id = jwt.decode(request.headers["Authorization"], os.environ.get(
            "JWT_SECRET"), algorithms=["HS256"])["user_id"]
        # Look for a user with the decrypted user id.
        user = models.User.query.filter_by(id=decrypted_id).first()
        # Handle whether a user was found.
        if user:
            # Check if the user's email address is being updated.
            if request.json.get("email"):
                # Check if the user's current password matches what has been passed.
                if bcrypt.check_password_hash(user.password, request.json["current_password"]):
                    print("Password check passed for email password check.")
                    # Check if another user already has that email address.
                    existing_user = models.User.query.filter_by(
                        email=request.json["email"]).first()
                    # Handle existing user.
                    if existing_user:
                        return{"message": "An account already exists with that email."}
                    else:
                        # Update the user's email address.
                        user.email = request.json["email"]
                else:
                    # Return a message if the password does not match.
                    return{"message": "The current password is incorrect. Unable to update user information."}, 401
            # Check if the user's password is being updated.
            if request.json.get("new_password"):
                print("new_password check came back as true.")
                # Check if the user's current password matches what has been passed.
                if bcrypt.check_password_hash(user.password, request.json["current_password"]):
                    # Update the user's password.
                    user.password = bcrypt.generate_password_hash(
                        request.json["new_password"]).decode("utf-8")
                else:
                    # Return a message if the password does not match.
                    return{"message": "The current password is incorrect. Unable to update user information."}, 401
            # Update the user within the database.
            models.db.session.add(user)
            # Commit the database updates.
            models.db.session.commit()
            # Create an encrypted authorization token before returning it to the client.
            encrypted_id = jwt.encode({"user_id": user.id}, os.environ.get(
                "JWT_SECRET"), algorithm="HS256")
            # Return the updated user data to the client.
            return {
                "user_info": user.to_json(),
                "summit_auth": encrypted_id
            }
        else:
            # Return a message if no user is found.
            return {"message": "Invalid user. Unable to update user information."}, 404
    except Exception as err:
        print("err", err)
        return {"message": "Something unknown went wrong."}, 400


app.route("/user/update", methods=["PUT"])(update_user)


# -------------------------------------------------
# Delete user account
def delete_user():
    try:
        # Decrypt the incoming authorization header.
        decrypted_id = jwt.decode(request.headers["Authorization"], os.environ.get(
            "JWT_SECRET"), algorithms=["HS256"])["user_id"]
        # Look for a user with the decrypted user id.
        user = models.User.query.filter_by(id=decrypted_id).first()
        # Handle whether a user was found.
        if user:
            # Check if the user's current password matches what has been passed.
            if bcrypt.check_password_hash(user.password, request.json["password"]):
                # Delete the user.
                models.db.session.delete(user)
                # Commit the database updates.
                models.db.session.commit()
                # Return a successful deletion message.
                return {"code": 0}
            else:
                # Return a message if the password does not match.
                return{"message": "The entered password is incorrect. Unable to delete user."}, 401
        else:
            # Return a message if no user is found.
            return {"message": "Invalid user. Unable to update user information."}, 404
    except Exception as err:
        print(err)
        return {"message": "Something unknown went wrong."}, 400


app.route("/user/delete", methods=["DELETE"])(delete_user)


# -------------------------------------------------
# Two routes in one.
def logs_func():
    # POST: Create a new Log, associated to the logged in user.
    if request.method == "POST":
        try:
            # Decrypt the incoming authorization header.
            decrypted_id = jwt.decode(request.headers["Authorization"], os.environ.get(
                "JWT_SECRET"), algorithms=["HS256"])["user_id"]
            # Look for a user with the decrypted user id.
            user = models.User.query.filter_by(id=decrypted_id).first()
            # Handle whether a user was found.
            if user:
                # Create a new Log.
                new_log = models.Log(
                    content=request.json["content"],
                    dateTime=datetime.now(timezone.utc),
                    analysis=request.json["analysis"]
                )
                # Associate the new log to the user.
                user.logs.append(new_log)
                # Add the new Log to the database.
                models.db.session.add(new_log)
                # Update the user within the database.
                models.db.session.add(user)
                # Commit the database updates.
                models.db.session.commit()
                return {"new_log": new_log.to_json()}
            else:
                # Return a message if no user is found.
                return {"message": "Invalid user. Unable to create new log."}, 404
        except Exception as err:
            print(err)
            return {"message": "Something unknown went wrong."}, 400
    # GET: Retrieve all of the logged in user's Logs.
    elif request.method == "GET":
        try:
            # Decrypt the incoming authorization header.
            decrypted_id = jwt.decode(request.headers["Authorization"], os.environ.get(
                "JWT_SECRET"), algorithms=["HS256"])["user_id"]
            # Look for a user with the decrypted user id.
            user = models.User.query.filter_by(id=decrypted_id).first()
            # Handle whether a user was found.
            if user:
                # Return the user's Logs.
                return {"logs": [l.to_json() for l in user.logs]}
            else:
                # Return a message if no user is found.
                return {"message": "Invalid user. Unable to retrieve logs."}, 404
        except Exception as err:
            print(err)
            return {"message": "Something unknown went wrong."}, 400


app.route("/logs", methods=["POST", "GET"])(logs_func)


# Set the Flask app to run.
if __name__ == "__main__":
    port = os.environ.get("PORT") or 5000
    app.run('0.0.0.0', port=port, debug=True)
