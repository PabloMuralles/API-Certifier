 
# API-Certifier
API simulation of a Certifier

 
# QR GENERATOR
Need to install

    pip install qr code

# How to connect to the API Example
    import requests

    api_endpoint = "http://44.211.61.33:8000/"

    json ={
    "nit": "66306191",
    "direction": "Ciudad",
    "date": "2023-04-11",
    "currency": "Q",
    "type": "Bien",
    "products": {"Tel1":{"Telefono":"13.54"}, "Camara":{"Camara web":"54.90"}}
    }

    r = requests.post(url=api_endpoint, json=json)

    print(r.status_code)
    print(r.text)

# How to create an virtual environment WINDOWS

With the terminal we have to go to the directory of the proyect and then put the following command

    python -m venv venv
    
The common way to name the environment is venv

How to enter to the environment to install de liberies

    venv\Scripts\activate.bat

Here you can have more information for the venv of python

    https://docs.python.org/3/library/venv.html

#  How to create a gitignore
Create a document named .gitignore then go to the following page

    https://www.toptal.com/developers/gitignore/

We have to specify all the common SO and the language that we are working this for don't put the venv in the repository and other stuff

then will create the file and copy paste to the file on your computer

# How to create the requirements.txt

the virtual environment if you want to know the libraries you have to put

    pip freeze

but if you want to create the file you can use

    pip freeze > requirements.txt

# How to create the secret key

you have to run the follow command, but if you are on WINDOWS you have to download the OPENSSL on your system

    openssl rand -hex 32

On windows after install openssl you have to add the environment variable, so press windows + R wirte 

    sysdm.cpl

then go to environment variable then select path and add 

    C:\Program Files\OpenSSL-Win64\bin

# How to try and decode your JWT token

    https://jwt.io/

And go to the debugger option

 
