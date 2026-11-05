from __future__ import annotations

from flask import Flask, jsonify, request
#import time

app = Flask(__name__)

events = [
    {
        "id": 1,
        "title": "Quizaften",
        "date": "2026-11-13",
        "capacity": 3,
        "participants": ["Anna", "Bo"],
    },
    {
        "id": 2,
        "title": "Brætspilsaften",
        "date": "2026-11-20",
        "capacity": 5,
        "participants": ["Charlie"],
    },
    {
        "id": 3,
        "title": "Beerpong-turnering",
        "date": "2026-11-27",
        "capacity": 4,
        "participants": [],
    },
]


@app.route("/events", methods=["GET"])
def get_events():
    #time.sleep(5)
    return jsonify(events)


@app.route("/events/<int:event_id>", methods=["GET"])
def get_event(event_id):
    event = next((e for e in events if e["id"] == event_id), None)

    if event is None:
        return jsonify({"error": "Event not found"}), 404

    return jsonify(event)


@app.route("/events", methods=["POST"])
def create_event():
    data = request.get_json()

    new_event = {
        "id": max(event["id"] for event in events) + 1,
        "title": data["title"],
        "date": data["date"],
        "capacity": data["capacity"],
        "participants": [],
    }

    events.append(new_event)

    return jsonify(new_event), 201


@app.route("/events/<int:event_id>/signups", methods=["POST"])
def signup_for_event(event_id):
    event = next((e for e in events if e["id"] == event_id), None)

    if event is None:
        return jsonify({"error": "Event not found"}), 404

    if len(event["participants"]) >= event["capacity"]:
        return jsonify({"error": "Event is full"}), 409

    data = request.get_json()

    event["participants"].append(data["name"])

    return jsonify(event), 201


@app.route("/events/<int:event_id>/signups/<string:name>", methods=["DELETE"])
def remove_signup(event_id, name):
    event = next((e for e in events if e["id"] == event_id), None)

    if event is None:
        return jsonify({"error": "Event not found"}), 404

    if name not in event["participants"]:
        return jsonify({"error": "Participant not found"}), 404

    event["participants"].remove(name)

    return "", 204

@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    event = next((e for e in events if e["id"] == event_id), None)

    if event is None:
        return jsonify({"error": "Event not found"}), 404

    events.remove(event)

    return "", 204

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
