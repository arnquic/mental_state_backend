# mental_state_backend
Backend for an app for a user to input notes/thoughts/journal entires. The app then analyzes those notes and gives metrics on the user's mental state.

## Backend http routes inventory
| HTTP Verb | Route | Notes |
| --------- | ----- | -------------------------------|
| POST | /user | Create a new User |
| POST | /user/login | Login an existing User
| GET | /user/verify | Verify an existing User via the authorization token held in local storage |
| PUT | /user/update | Update user information (email and password) |
| DELETE | /user/delete | Delete user account |
| POST | /logs | Create a new Log and related Analysis, associated to the logged in user |
| GET | /logs | Retrieve all Logs that are associated to the logged in user |

## A link to your repo!
- Frontend: https://github.com/arnquic/mental_state_frontend
- Backend: https://github.com/arnquic/mental_state_backend