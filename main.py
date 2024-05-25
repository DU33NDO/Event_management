import requests


res = requests.get("http://127.0.0.1:5000/events")
print(res.json())
# data = {
#     "name": "Лепс в городе!",
#     "date_of_event": "2024-12-31 21:59:59",
#     "description": "будет круто, с 18+"
# }

# res= requests.post("http://127.0.0.1:5000/events", json=data)
# print(res.json())