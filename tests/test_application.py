
import sys
import os

# Get this file's directory.
current = os.path.dirname(os.path.realpath(__file__))

# Get the parent directory to this file's directory.
parent = os.path.dirname(current)

# Add the parent directory to the system's path.
sys.path.append(parent)

# Import the app variable from the application.py file (we need to add the parent directory to the system path to get at this file).
from application import app

# Create an instance of the "mental_state_backend"'s Flask app as a test client.
client = app.test_client()

# Test for response 200 at the root route.
def test_health():
    # Request a GET from the client at the "/" route and store the response.
    response = client.get("/")

    # Get the JSON from the response and access the returned message.
    # ASSERT that the returned message contains the described value.
    assert response.get_json()["message"] == "Server is healthy."

    # ASSERT that the response's status code is 200.
    assert response.status_code == 200


# Test the user creation process
""" def test_user_creation():
    # Define a test user to create
    test_user = {
        "firstName": "testFirst",
        "lastName": "testLast",
        "email": "testEmail",
        "password": "12345678"
    }

    # Request a POST from the client at the "/user" route and store the response.
    response = client.post("/user", json=test_user)



    # Remove the test user
    client.delete("/user", json) """



