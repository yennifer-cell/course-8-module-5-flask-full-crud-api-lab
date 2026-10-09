from flask import Flask, jsonify, request
from werkzeug.exceptions import BadRequest

app = Flask(__name__)


class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {"id": self.id, "title": self.title}


# In-memory "database"
events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop"),
]


def get_event_by_id(event_id):
    for event in events:
        if event.id == event_id:
            return event
    return None


@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Welcome to the Event API!"})


@app.route("/events", methods=["GET"])
def list_events():
    return jsonify([event.to_dict() for event in events])


@app.route("/events", methods=["POST"])
def create_event():
    try:
        data = request.get_json()
    except BadRequest:
        return jsonify({"error": "Invalid JSON payload"}), 400

    if not isinstance(data, dict):
        return jsonify({"error": "Request body must be a JSON object"}), 400

    title = data.get("title")
    if not isinstance(title, str) or not title.strip():
        return jsonify({"error": "Title is required"}), 400

    next_id = max((event.id for event in events), default=0) + 1
    new_event = Event(next_id, title.strip())
    events.append(new_event)
    return jsonify(new_event.to_dict()), 201


@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
    try:
        data = request.get_json()
    except BadRequest:
        return jsonify({"error": "Invalid JSON payload"}), 400

    if not isinstance(data, dict):
        return jsonify({"error": "Request body must be a JSON object"}), 400

    event = get_event_by_id(event_id)
    if event is None:
        return jsonify({"error": "Event not found"}), 404

    title = data.get("title")
    if not isinstance(title, str) or not title.strip():
        return jsonify({"error": "Title is required"}), 400

    event.title = title.strip()
    return jsonify(event.to_dict())


@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    event = get_event_by_id(event_id)
    if event is None:
        return jsonify({"error": "Event not found"}), 404

    events.remove(event)
    return "", 204


if __name__ == "__main__":
    app.run(debug=True)
