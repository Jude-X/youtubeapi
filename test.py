import requests

BASE = "http://127.0.0.1:5000/api/v1/videos/"

response = requests.put(BASE + "2", {"name":"How to become a full backend engineer","likes":150, "views":200})

response = requests.get(BASE + "2")

response = requests.get(BASE + "6")