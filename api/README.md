# Voice Cloning : Flask API

## Getting Started 

Install the requirements for the flask server and firebase

Make sure you are in the current working directory. (i.e; the `api` directory in this repository)

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
1. [`/api/signup`](#signup-route)
2. [`/api/token`](#token-sign-in-route)
3. [`/api/userinfo`](#userinfo-route)
4. [`/api/upload`](#upload-route)
5. [`/api/generate`](#generate-route)
----

## Signup route

> endpoint `/api/signup`
> 
> Methods: `GET`


Used to create an account in the app and receive the user_id

Here is a curl example:

```bash
curl -X GET -F 'email=name@example.com' -F 'password=mypassword123' http://localhost:5000/api/signup
```

### **Responses:**

Success :

`201: Successfully created user {user_id}`

Error: 

`400: Error creating user {exception}`

----

## Token (sign in) route

> endpoint `/api/token`
> 
> Methods: `GET`

After an account has been created at `/api/signup`,
those credentials may be use to obtain an authorization token.

Here is a curl example:

```bash
curl -X GET -F 'email=name@example.com' -F 'password=mypassword123' http://localhost:5000/api/token  
```

## **Responses:**

Success :

`200: {'token': jwt}`

Error: 

`400: There was an error logging in {exception}`

----
## Userinfo route

> endpoint `/api/userinfo`
> 
> Methods: `GET`
> 
Once you have the auth token, you can view the userinfo.

Here is a curl example:
```bash
export TOKEN=<token-received-from-token-endpoint>
```

```bash
curl --location --request GET 'http://localhost:5000/api/userinfo' --header "authorization: $TOKEN"
```

### **Responses:**

Success :

`200: {'iss': 'https://securetoken.google.com/app-name', 'aud': 'app-name', 'auth_time': Number, 'user_id': 'abcdefgh123456', 'sub': 'abcdefgh123456', 'iat': Number, 'exp': 1649587348, 'email': 'name@example.com', 'email_verified': False, 'firebase': {'identities': {'email': ['name@example.com']}, 'sign_in_provider': 'password'}, 'uid': 'abcdefgh123456'}`

Error:

`400: Invalid token provided. {exception}`

## Upload Route

> endpoint `/api/upload`
> 
> Methods: `POST`

In order to generate audio from text with your cloned voice, it is necessary to upload a voice sample first (~5 seconds long).

Upload a wav recording of your voice to your account
Here is a curl example:

```bash
export TOKEN=your-jwt-token-from-authentication-step

curl -F 'file=@<FILEPATH>;type=audio/x-wav' --location --request POST 'http://localhost:5000/api/upload' --header "authorization: $TOKEN"
```

### **Responses:**

Success :

`201: Successfully uploaded`

Error: 

`400: Error creating user {exception}`

`400: Error missing file`

`401: Error not signed in`

----

## Generate Route

> endpoint `/api/generate`
> 
> Methods: `POST`

Generate the audio on the server and download it to your device.
In order to generate audio from text with your cloned voice, it is necessary to upload a voice sample first (~5 seconds long).

Once you have uploaded your voice sample as per the [previous route's documentation](#upload-route), you can POST some text to the generate route and download the audio file thus generated

Here is a curl example:
```bash
export TOKEN=<token-received-from-token-endpoint>
```

```bash
curl -X POST -F 'text=sample text' http://localhost:5000/api/generate --header "authorization: $TOKEN" --output downloaded_audio.wav
```

### **Responses:**

Success :

`201: {binary wav audio content}`

Error: 

`404: Error no voice sample file found for user {user_id}`

`400: Error fetching file. Try again.`

`400: Error generating: {exception}`

----