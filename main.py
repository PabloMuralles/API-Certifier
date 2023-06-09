from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Union
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}

app = FastAPI()

# I don't understand well but this is to access to the token of the route "/token"
oauth2_scheme = OAuth2PasswordBearer("/token")

# I don't understand this well but help us to validate de encrypted password
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# this secret key need to be hide so it's not  correct to this but in this case is an example will be here but regularly this wil be a environment variable on the server
# this will help to create the tokens
SECRET_KEY = "2e49ada461a1c1b9d416a1dcd7be8d7bdca40996c8a1c334b616f209d03c0ea6"
# algorithm to encrypts and JWT function correct, it's important to mention that JWT it not for encryption it's for tokens.
# JWT create a signature to ensure that our server it's our server no other server
ALGORITHM = "HS256"

# Union[str, None] = None this means that the attribute can be string or null and for default we initialize null
class User(BaseModel):
    username: str
    full_name: Union[str, None] = None
    email: Union[str, None] = None
    disable: Union[bool, None] = None

# User inside of the parenthesis means Inherit
class UserInDB(User):
    hashed_password:str

# validate the user exist in the data base
def _get_user(db, username):
    if username in db:
        user_data = db[username]
        return UserInDB(**user_data) #this is for put the data of te list in the class

# verify the password that match with the database password
def _verify_password(plane_password, hashed_password):
    return pwd_context.verify(plane_password, hashed_password)

def _authenticate_user(db, username, password):
    user = _get_user(db, username)
    if not user :
        raise HTTPException(status_code=401, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    if not _verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    return user

def _create_token(data: dict, time_expire: Union[datetime, None] = None):
    data_copy = data.copy() #create a identically copy of data without modify the original dictionary
    if time_expire is None:
        expires = datetime.utcnow() + timedelta(minutes=15) # utcnow actual time 
    else:
        expires = datetime.utcnow() + time_expire
    data_copy.update({"exp": expires}) # update the dictionary
    token_jwt = jwt.encode(data_copy, key=SECRET_KEY, algorithm=ALGORITHM)
    return token_jwt


# @app.get("/")
# def root():
#         return "Hello"

# depends is a injection of dependence, this make that execute a function when we enter to this route
# el oauth2_scheme it the thing that help us to make private the endpoint
@app.get("/user/me")
def user(token: str = Depends(oauth2_scheme)):
    return token
 
# this endpoint is te first steps to authenticate the user to use the api then pase to the endpoint user/me
@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = _authenticate_user(fake_users_db, form_data.username, form_data.password )
    access_token_expires = timedelta(minutes=30)
    access_token_jwt = _create_token({"sub": user.username}, access_token_expires) # sub is part of oauth for the system that use JWT, it's no obligatory but it better practice. Indicates the identity of an entity in this case the user
    return {
        "access_token": access_token_jwt,
        "token_type": "bearer"
    }

