from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Episode(db.Model):
    __tablename__ = "episodes"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    number = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp(),
    )


class Appearance(db.Model):
    __tablename__ = "appearances"
    id = db.Column(db.Integer, primary_key=True)
    episode_id = db.Column(db.Integer, db.ForeignKey("episodes.id"), nullable=False)
    guest_id = db.Column(db.Integer, db.ForeignKey("guests.id"), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp(),
    )


class Guest(db.Model):
    __tablename__ = "guests"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    occupation = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp(),
    )


@app.route("/")
def home():
    return "Welcome to the Late Show!"


@app.route("/episodes", methods=["GET"])
def get_episodes():
    episodes = Episode.query.all()
    data = [
        {"id": episode.id, "date": episode.date, "number": episode.number}
        for episode in episodes
    ]
    return jsonify(data)


@app.route("/episodes/<int:episode_id>", methods=["GET"])
def get_episode(episode_id):
    episode = Episode.query.get(episode_id)
    if episode:
        data = {"id": episode.id, "date": episode.date, "number": episode.number}
        return jsonify(data)
    else:
        return jsonify({"error": "Episode not found"}), 404


@app.route("/guests", methods=["GET"])
def get_guests():
    guests = Guest.query.all()
    data = [
        {"id": guest.id, "name": guest.name, "occupation": guest.occupation}
        for guest in guests
    ]
    return jsonify(data)


@app.route("/guests/<int:guest_id>", methods=["GET"])
def get_guest(guest_id):
    guest = Guest.query.get(guest_id)
    if guest:
        data = {"id": guest.id, "name": guest.name, "occupation": guest.occupation}
        return jsonify(data)
    else:
        return jsonify({"error": "Guest not found"}), 404


@app.route("/appearances", methods=["GET"])
def get_appearances():
    appearances = Appearance.query.all()
    data = [
        {
            "id": appearance.id,
            "episode_id": appearance.episode_id,
            "guest_id": appearance.guest_id,
            "rating": appearance.rating,
        }
        for appearance in appearances
    ]
    return jsonify(data)


@app.route("/appearances/<int:appearance_id>", methods=["GET"])
def get_appearance(appearance_id):
    appearance = Appearance.query.get(appearance_id)
    if appearance:
        data = {
            "id": appearance.id,
            "episode_id": appearance.episode_id,
            "guest_id": appearance.guest_id,
            "rating": appearance.rating,
        }
        return jsonify(data)
    else:
        return jsonify({"error": "Appearance not found"}), 404


if __name__ == "__main__":
    app.run(port=5555)
