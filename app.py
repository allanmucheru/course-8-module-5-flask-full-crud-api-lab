from flask import Flask, jsonify, request

app = Flask(__name__)


# Event model class expected by the tests
class Event:

    def __init__(self, id, title, location="", date=""):
        self.id = id
        self.title = title
        self.location = location
        self.date = date

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "location": self.location,
            "date": self.date,
        }


# Sample in-memory database using Event instances
events = [
    Event(
        id=1,
        title="Tech Conference 2026",
        location="Nairobi",
        date="2026-10-15",
    ),
    Event(id=2, title="Flask Workshop", location="Online", date="2026-11-01"),
]


# Helper function to find an event by ID
def find_event(event_id):
    return next((e for e in events if e.id == event_id), None)


# 1. Root Route - Welcome Message
@app.route("/", methods=["GET"])
def welcome():
    return jsonify({"message": "Welcome to the Events API!"}), 200


# 2. GET /events - Retrieve all events
@app.route("/events", methods=["GET"])
def get_events():
    return jsonify([e.to_dict() for e in events]), 200


# 3. GET /events/<id> - Retrieve a single event
@app.route("/events/<int:event_id>", methods=["GET"])
def get_event(event_id):
    event = find_event(event_id)
    if not event:
        return jsonify({"error": "Event not found"}), 404
    return jsonify(event.to_dict()), 200


# 4. POST /events - Create a new event
@app.route("/events", methods=["POST"])
def create_event():
    data = request.get_json()

    if not data or "title" not in data or not str(data.get("title")).strip():
        return jsonify({"error": "Bad Request: 'title' is required"}), 400

    new_id = max([e.id for e in events], default=0) + 1
    new_event = Event(
        id=new_id,
        title=data["title"],
        location=data.get("location", ""),
        date=data.get("date", ""),
    )

    events.append(new_event)
    return jsonify(new_event.to_dict()), 201


# 5. PATCH /events/<id> - Update specific fields of an event
@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
    event = find_event(event_id)
    if not event:
        return jsonify({"error": "Event not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "Bad Request: No JSON data provided"}), 400

    if "title" in data:
        event.title = data["title"]
    if "location" in data:
        event.location = data["location"]
    if "date" in data:
        event.date = data["date"]

    return jsonify(event.to_dict()), 200


# 6. DELETE /events/<id> - Delete an event
@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    event = find_event(event_id)
    if not event:
        return jsonify({"error": "Event not found"}), 404

    events.remove(event)
    return "", 204  # Return empty response body with 204 status code