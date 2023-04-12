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