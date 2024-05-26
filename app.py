from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, reqparse
from datetime import datetime
from flask_cors import CORS
import hashlib


app = Flask(__name__)
CORS(app)
api = Api(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://new_user:123@localhost/Events"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Event(db.Model):
    event_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    date_of_event_start = db.Column(db.DateTime, nullable=False)
    date_of_event_end = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.String(256), nullable=False)
    address = db.Column(db.String(256), nullable=False)
    price_for_ticket = db.Column(db.Integer, nullable=True)
    type_of_event = db.Column(db.String(256), nullable=True)
    poster_url = db.Column(db.String(256), nullable=True)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    login = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'


event_parser = reqparse.RequestParser()
event_parser.add_argument(
    "name", type=str, required=True, help="Name of the event is required!!"
)
event_parser.add_argument(
    "date_of_event_start",
    type=str,
    required=True,
    help="Date_of_event_start of the event is required!!",
)
event_parser.add_argument(
    "date_of_event_end",
    type=str,
    required=True,
    help="Date_of_event_end of the event is required!!",
)
event_parser.add_argument(
    "description",
    type=str,
    required=True,
    help="Description of the event is required!!",
)
event_parser.add_argument(
    "address", type=str, required=True, help="Address of the event is required!!"
)
event_parser.add_argument(
    "price_for_ticket",
    type=int,
    required=True,
    help="Price for ticket of the event is required!!",
)
event_parser.add_argument(
    "type_of_event", type=str, required=True, help="Type of the event is required!!"
)
event_parser.add_argument(
    "poster_url", type=str, required=True, help="Poster of the event is required!!"
)


user_parser = reqparse.RequestParser()
user_parser.add_argument(
    "username", type=str, required=True, help="Username is required"
)
user_parser.add_argument(
    "login", type=str, required=True, help="Login is required"
)
user_parser.add_argument(
    "password", type=str, required=True, help="Password is required"
)

log_user_parser = reqparse.RequestParser()
log_user_parser.add_argument(
    "login", type=str, required=True, help="Login is required"
)
log_user_parser.add_argument(
    "password", type=str, required=True, help="Password is required"
)


@app.route("/events", methods=["GET"])
def get_events():
    events = Event.query.all()
    return jsonify(
        [
            {
                "event_id": event.event_id,
                "name": event.name,
                "date_of_event_start": event.date_of_event_start,
                "date_of_event_end": event.date_of_event_end,
                "description": event.description,
                "address": event.address,
                "price_for_ticket": event.price_for_ticket,
                "type_of_event": event.type_of_event,
                "poster_url": event.poster_url,
            }
            for event in events
        ]
    )


@app.route("/events/<target_type>", methods=["GET"])
def get_filtered_events(target_type):
    events = Event.query.filter_by(type_of_event=target_type).all()
    return jsonify(
        [
            {
                "event_id": event.event_id,
                "name": event.name,
                "date_of_event_start": event.date_of_event_start,
                "date_of_event_end": event.date_of_event_end,
                "description": event.description,
                "address": event.address,
                "price_for_ticket": event.price_for_ticket,
                "type_of_event": event.type_of_event,
                "poster_url": event.poster_url,
            }
            for event in events
        ]
    )


@app.route("/events/<int:target_id>", methods=["GET"])
def get_event_by_id(target_id):
    event = Event.query.filter_by(event_id=target_id).first()
    if event is None:
        return jsonify({"message": "Event not found"}), 404
    else:
        return jsonify(
            {
                "event_id": event.event_id,
                "name": event.name,
                "date_of_event_start": event.date_of_event_start,
                "date_of_event_end": event.date_of_event_end,
                "description": event.description,
                "address": event.address,
                "price_for_ticket": event.price_for_ticket,
                "type_of_event": event.type_of_event,
                "poster_url": event.poster_url,
            }
        )


@app.route("/events", methods=["POST"])
def add_event():
    args = event_parser.parse_args()
    try:
        date_of_event_start = datetime.strptime(
            args["date_of_event_start"], "%Y-%m-%d %H:%M:%S"
        )
        date_of_event_end = datetime.strptime(
            args["date_of_event_end"], "%Y-%m-%d %H:%M:%S"
        )
    except ValueError:
        return jsonify({"message": "Invalid date format. Use YYYY-MM-DD HH:MM:SS"}), 400

    new_event = Event(
        name=args["name"],
        date_of_event_start=date_of_event_start,
        date_of_event_end=date_of_event_end,
        description=args["description"],
        address=args["address"],
        price_for_ticket=args["price_for_ticket"],
        type_of_event=args["type_of_event"],
        poster_url=args["poster_url"],
    )
    db.session.add(new_event)
    db.session.commit()
    return (
        jsonify(
            {
                "event_id": new_event.event_id,
                "name": new_event.name,
                "date_of_event_start": new_event.date_of_event_start.isoformat(),
                "date_of_event_end": new_event.date_of_event_end.isoformat(),
                "description": new_event.description,
                "address": new_event.address,
                "price_for_ticket": new_event.price_for_ticket,
                "type_of_event": new_event.type_of_event,
                "poster_url": new_event.poster_url,
            }
        ),
        201,
    )


@app.route('/register', methods=['POST'])
def register_user():
    args = user_parser.parse_args()
    username = args["username"]
    login = args["login"]
    password = args["password"]

    if len(password) < 8:
        return jsonify({"message": "Пароль должен быть больше 8 символов"}), 400

    existing_user = Users.query.filter_by(login=login).first()
    if existing_user:
        return jsonify({"message": "Такой логин уже существует("}), 400

    hash_password = hashlib.sha256(password.encode())
    hash_new_password = hash_password.hexdigest()

    new_user = Users(username=username, login=login, password=hash_new_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Регистрация прошла успешно!"}), 201


@app.route('/login', methods=['POST'])
def login_user():
    args = log_user_parser.parse_args()
    login = args["login"]
    password = args["password"]

    hash_password = hashlib.sha256(password.encode())
    hash_new_password = hash_password.hexdigest()

    user = Users.query.filter_by(login=login).first()

    if user.password == hash_new_password and user:
        return jsonify({"message": "Вы вошли в аккаунт!"}), 200
    else: 
        return jsonify({"message": "Неверный пароль или логин("})


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
