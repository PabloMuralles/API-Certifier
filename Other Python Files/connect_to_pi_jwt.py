 
import requests
import json
import jwt
import time


url = "http://localhost:8000/token"
 
# client_id = 'pablo'
#client_secret = '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW'
#the password go like plain text because we need to use a certificate SSL to encrypted the traffic to the API and the compare the paint text to the hashed password 
# because hashed password prevents if some one steals

response = requests.post(url=url, data={"username": "pablo", "password": "secret", "grant_type": "password"},
                           headers={"content-type": "application/x-www-form-urlencoded"})
 

jwt_token = json.loads(response.text)["access_token"]


# region ---- verify the expiration time 
claims = jwt.decode(jwt_token,verify=False, options={'verify_signature': False} )
exp = claims['exp']

if time.time() > exp:
    print("Hola")

# endregion
 


headers = {'Authorization': "Bearer {}".format(jwt_token)}
data = {
    "items" : {"nit": "25486984",
    "name": "Everise", 
    "address": "Avenida Hincapie 7-23, Zepto",
    "date_invoice": "2023-05-18",
    "products": {"[JBE20] Jabra Evolve 20!": { "1" : "product"}}, 
    "currency": "GTQ"}
}


response = requests.post("http://localhost:8000/confirm", headers=headers, json=data)

print(response.text)

