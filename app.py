from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, reqparse
from datetime import datetime


app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://new_user:123@localhost/Events'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Event(db.Model):
    event_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    date_of_event = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.String(256), nullable=False)
    city = db.Column(db.String(100), nullable=False)


event_parser = reqparse.RequestParser()
event_parser.add_argument('name', type=str, required=True, help="Name of the event is required!!")
event_parser.add_argument('date_of_event', type=str, required=True, help="Date of the event is required!!")
event_parser.add_argument('description', type=str, required=True, help="Description of the event is required!!")
event_parser.add_argument('city', type=str, required=True, help="City of the event is required!!")


@app.route('/events', methods=['GET'])
def get_events():
    events = Event.query.all()
    return jsonify([
        {'event_id': event.event_id, 'name': event.name, 'date_of_event': event.date_of_event, 'description': event.description, 'city': event.city}
        for event in events])


@app.route('/events', methods=['POST'])
def add_event():
    args = event_parser.parse_args()
    try:
        date_of_event = datetime.strptime(args['date_of_event'], '%Y-%m-%d %H:%M:%S')
    except ValueError:
        return jsonify({'message': 'Invalid date format. Use YYYY-MM-DD HH:MM:SS'}), 400

    new_event = Event(name=args['name'], date_of_event=date_of_event, description=args['description'], city=args['city'])
    db.session.add(new_event)
    db.session.commit()
    return jsonify({
        'event_id': new_event.event_id,
        'name': new_event.name,
        'date_of_event': new_event.date_of_event.isoformat(),
        'description': new_event.description,
        'city': new_event.city
    }), 201


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)