# Voice Cloning : Flask API


Install the requirements for the flask server and firebase

```bash
pip3 install -r requirements.txt
```
Create a Firebase App -> Create a firebase web-app and paste the SDK configuration into a new file `fbconfig.json`

Example Shape for `fbconfig.json` 
```json
{
  "apiKey": "api-key-from-firebase",
  "authDomain": "some-name.firebaseapp.com",
  "projectId": "some-name",
  "storageBucket": "some-name.appspot.com",
  "messagingSenderId": "number",
  "appId": "x:num:web:hex",
  "measurementId": "G-SOMETHING",
  "databaseURL": "" //leave it blank
}
```
Create a service account inside the web-app on firebase and download the private config into a file called fbAdminConfig.json

Example Shape for `fbAdminConfig.json` 
```json
{
  "type": "service_account",
  "project_id": "project name",
  "private_key_id": "PRIVATE KEY ID",
  "private_key": "SECRET PRIVATE KEY !!DO NOT EXPOSE",
  "client_email": "ADDRESS-FOR-@-serviceaccount.com",
  "client_id": "NUMBER",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "certificate-url"
}
```
Once configured properly, go ahead and run it like so 
```bash 
flask run
```
# API Documentation 

API routes supported
- `/api/signup`
- `/api/token`
- `/api/userinfo`
- `/api/upload`
----

## Signup route

Used to create an account in the app.
Here is a curl example:

```bash
curl -X GET -F 'email=name@example.com' -F 'password=mypassword123' http://localhost:5000/api/signup
```

### **Responses:**

Success :
`201: Successfully created user {user_id}`

Error: `400: Error creating user {exception}`

----

## Token (sign in) route

After an account has been created at `/api/signup`,
those credentials may be use to obtain an authorization token.

Here is a curl example:

```bash
curl -X GET -F 'email=name@example.com' -F 'password=mypassword123' http://localhost:5000/api/token  
```

## **Responses:**

Success :
`200: {'token': jwt}`

Error: `400: There was an error logging in {exception}`

----
## Userinfo route
Once you have the auth token, you can view the userinfo.

Here is a curl example:

```bash

export TOKEN=<PASTE TOKEN HERE>

 curl --location --request GET 'http://localhost:5000/api/userinfo' \                                      
--header 'authorization: $TOKEN'
```

### **Responses:**

Success :
`201: {'iss': 'https://securetoken.google.com/app-name', 'aud': 'app-name', 'auth_time': Number, 'user_id': 'abcdefgh123456', 'sub': 'abcdefgh123456', 'iat': Number, 'exp': 1649587348, 'email': 'name@example.com', 'email_verified': False, 'firebase': {'identities': {'email': ['name@example.com']}, 'sign_in_provider': 'password'}, 'uid': 'abcdefgh123456'}`

Error: `400: Invalid token provided. {exception}`
