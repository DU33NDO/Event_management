from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, reqparse
from datetime import datetime
from flask_cors import CORS


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


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
