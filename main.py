from fastapi import FastAPI, Depends, HTTPException, Body, Header
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Union, Annotated
from passlib.context import CryptContext
from datetime import datetime, timedelta, date
from jose import jwt, JWTError
import uvicorn
import random
 
 

fake_users_db = {
    "pablo": {
        "username": "pablo",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}

app = FastAPI()

# region ----- API Business Logic

class InvoiceItem(BaseModel):
    nit: str 
    name: str 
    address: str
    date_invoice: date
    products: dict = {}
    currency: str

class InvoiceDocs(BaseModel):
    authorization: str
    serial: str
    DTE: str
    invoice_date: datetime
    certification_date: datetime
    qty_products: int

def _randN(N):
	min = pow(10, N-1)
	max = pow(10, N) - 1
	return str(random.randint(min, max))

# endregion

#region ----- API JWT

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
# Time that live the token
ACCESS_TOKEN_EXPIRE_MINUTES = 30

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

# validate the token and user, and with tis decode automatically check the expiration time of the token 
def _get_user_current(token: str = Depends(oauth2_scheme)):
    try:
        token_decode = jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])
        user_name = token_decode.get("sub")
        if user_name == None:
            raise HTTPException(status_code=401, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

    #validate if the user exist in the db
    user = _get_user(fake_users_db, user_name)
    if not user:
        raise HTTPException(status_code=401, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    return user

# validate if the token is valid 
def _get_user_disable_current(user: User = Depends(_get_user_current)):
    if user.disable:
        raise HTTPException(status_code=400, detail="Inactive User")
    return user


# depends is a injection of dependence, this make that execute a function when we enter to this route
# el oauth2_scheme it the thing that help us to make private the endpoint
@app.get("/user/me")
def user(user: User = Depends(_get_user_disable_current)):
    return user
 
# this endpoint is te first steps to authenticate the user to use the api then pase to the endpoint user/me
# in this route we have to send the user and password to make te validation to the api
@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = _authenticate_user(fake_users_db, form_data.username, form_data.password )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token_jwt = _create_token({"sub": user.username}, access_token_expires) # sub is part of oauth for the system that use JWT, it's no obligatory but it better practice. Indicates the identity of an entity in this case the user
    return {
        "access_token": access_token_jwt,
        "token_type": "bearer"
    }

#endregion

#region ----- API Business Logic

#fastapi automatically transform the dictionary to a json    UserInDB(**user_data) importance: Annotated[int, Body()
@app.post("/confirm")
async def confirm_invoice(user: User = Depends(_get_user_disable_current), items: InvoiceItem = Body(embed=True)):
    if items.nit and items.name and items.address and items.date_invoice and items.products and items.currency:
        if len(items.nit) >= 8:
            certifier_data = InvoiceDocs(authorization=_randN(36), serial=_randN(8), DTE=_randN(10), invoice_date=datetime.today(), certification_date=datetime.today(), qty_products=len(items.products))
            return certifier_data
            #json_compatible_item_data = jsonable_encoder(return_data)
            #return JSONResponse(content=json_compatible_item_data)
        else:
            raise HTTPException(status_code=404, detail="Invalid NIT")
    else:
        raise HTTPException(status_code=404, detail="Missing Data")
    
@app.post("/annul")
async def annul_invoice(user: User = Depends(_get_user_disable_current), items: InvoiceDocs= Body(embed=True)):
    if items.authorization and items.serial and items.DTE and items.invoice_date and items.certification_date and items.qty_products:
        delta_days = items.certification_date.date() - date.today()
        delta_days = delta_days.days
        if (0 >= delta_days <= 30):
            return {"date": f"{datetime.today()}"}
        else:
           raise HTTPException(status_code=404, detail="The date exceeds 30 days")
    else:
        raise HTTPException(status_code=404, detail="Missing Data")
    
#endregion

if __name__ == "__main__":
    uvicorn.run(app,host="0.0.0.0", port=8000)