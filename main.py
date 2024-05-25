import requests
from datetime import datetime, date
import json


# res = requests.get("http://127.0.0.1:5000/events")
# print(res.json())

dates = []


# def convert_data_to_json(date_needed: datetime):
#     date_needed = date_needed.strftime("%Y-%m-%d %H:%M:%S")
#     data = {"date_of_event_start": date_needed}
#     try:
#         json_date = json.dumps(data)
#     except TypeError as e:
#         print("Error:", e)
#     data["date_of_event_start"] = date_needed
#     json_date = json.dumps(data)
#     return json_date


def format_date(date_time):
    return date_time.strftime("%Y-%m-%d %H:%M:%S")


data_1 = {
    "name": "Мастер-класс: «Холст, акриловые краски»",
    "date_of_event_start": '2024-06-10 12:00:00',
    "date_of_event_end": '2024-06-10 18:00:00',
    "description": "Создать шедевр и оставить свой след в искусстве, даже если никогда не рисовал \n\n Art Lab приглашает вас на мастер класс с Акриловыми красками на холсте. Сюжет и размер картины полностью под ваш выбор.\n\nТакой выходной - это лучший способ, чтобы поднять себе настроение, интересно провести время и научится чему-то новому",
    "address": "Сыганак 25",
    "price_for_ticket": 3000,
    "type_of_event": "art",
    "poster_url": "https://celes.club/uploads/posts/2022-10/1667239193_1-celes-club-p-art-vecherinka-kholst-i-vino-krasivo-1.jpg",
}
# res = requests.post("http://127.0.0.1:5000/events", json=data_1)
# print(res.json())
