from flask import Flask, request, jsonify
from flask import session
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, reqparse
from datetime import datetime
from flask_cors import CORS
import hashlib


app = Flask(__name__)
CORS(app, supports_credentials=True)
api = Api(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://new_user:123@localhost/Events"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY'] = 'dogs'
db = SQLAlchemy(app)


class Event(db.Model):
    event_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    date_of_event_start = db.Column(db.DateTime, nullable=False)
    date_of_event_end = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.String(256), nullable=False)
    address = db.Column(db.String(256), nullable=False)
    price_for_ticket = db.Column(db.Integer, nullable=False)
    type_of_event = db.Column(db.String(256), nullable=False)
    poster_url = db.Column(db.String(256), nullable=False)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    login = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    is_in_account = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f'<User {self.username}>'


class Ticket(db.Model):
    ticket_id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.event_id'), nullable=False)
    is_purchased = db.Column(db.Boolean, nullable=False, default=False)


class Purchase(db.Model):
    purchase_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    tickets = db.relationship('Ticket', secondary='ticket_purchase_association', backref='purchases')


ticket_purchase_association = db.Table(
    'ticket_purchase_association',
    db.Column('ticket_id', db.Integer, db.ForeignKey('ticket.ticket_id')),
    db.Column('purchase_id', db.Integer, db.ForeignKey('purchase.purchase_id'))
)


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

@app.route("/purchase/<int:target_id>", methods=["GET"])
def get_event_purchase_by_id(target_id):
    tickets = Ticket.query.filter_by(event_id=target_id).all()
    if tickets is None:
        return jsonify({"message": "Tickets not found"}), 404
    else:
        return jsonify([
            {
                "ticket_id": ticket.ticket_id,
                "event_id": ticket.event_id,
                "is_purchased": ticket.is_purchased
            } for ticket in tickets
            ]
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
        session['user_id'] = user.id 
        user.is_in_account = True  
        db.session.commit()
        return jsonify({"message": "Вы вошли в аккаунт!"}), 200
    else: 
        return jsonify({"message": "Неверный пароль или логин("})


@app.route('/logout', methods=['POST'])
def logout_user():
    user_id = session.get('user_id')
    if user_id:
        user = Users.query.get(user_id)
        user.is_in_account = False  
        db.session.commit()
        session.pop('user_id') 
        return jsonify({"message": "Вы вышли из аккаунта"}), 200
    else:
        return jsonify({"message": "Вы не вошли в аккаунт"}), 400


@app.route('/is_logged_in', methods=['GET'])
def is_logged_in():
    if 'user_id' in session:
        return jsonify({"logged_in": True}), 200
    else:
        return jsonify({"logged_in": False}), 200
    
    
@app.route("/tickets/count/<int:event_id>", methods=["GET"])
def get_tickets_count(event_id):
    tickets_count = Ticket.query.filter_by(event_id=event_id).count()
    return jsonify({"tickets_count": tickets_count}), 200


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
