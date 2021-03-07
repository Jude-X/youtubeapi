import requests

BASE = "http://127.0.0.1:5000/api/v1/videos/"

response = requests.post(BASE + "2", {"name":"How to become an engineer","likes":150, "views":200})

#response = requests.delete(BASE + "2")

#response = requests.get(BASE + "6")