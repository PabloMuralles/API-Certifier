import requests

api_endpoint = "http://44.211.61.33:8000/"

data ={
  "nit": "66306191",
  "direction": "Ciudad",
  "date": "2023-04-11",
  "currency": "Q",
  "type": "Bien",
  "products": {"Tel1":{"Telefono":"13.54"}, "Camara":{"Camara web":"54.90"}}
}

r = requests.post(url=api_endpoint, data=data)

print(r.text)