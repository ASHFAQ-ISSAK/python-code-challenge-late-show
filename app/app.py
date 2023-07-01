# from flask import Flask
# from flask_restful import Api, Resource
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate

# app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# db = SQLAlchemy(app)
# migrate = Migrate(app, db)
# api = Api(app)


# class Appearance(db.Model):
#     __tablename__ = "appearances"
#     id = db.Column(db.Integer, primary_key=True)
#     episode_id = db.Column(db.Integer, db.ForeignKey("episodes.id"), nullable=False)
#     guest_id = db.Column(db.Integer, db.ForeignKey("guests.id"), nullable=False)
#     rating = db.Column(db.Integer, nullable=False)
#     created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
#     updated_at = db.Column(
#         db.DateTime,
#         default=db.func.current_timestamp(),
#         onupdate=db.func.current_timestamp(),
#     )


# class Guest(db.Model):
#     __tablename__ = "guests"
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     occupation = db.Column(db.String(100), nullable=False)
#     created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
#     updated_at = db.Column(
#         db.DateTime,
#         default=db.func.current_timestamp(),
#         onupdate=db.func.current_timestamp(),
#     )


# class Episode(db.Model):
#     __tablename__ = "episodes"
#     id = db.Column(db.Integer, primary_key=True)
#     date = db.Column(db.DateTime, nullable=False)
#     number = db.Column(db.Integer, nullable=False)
#     created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
#     updated_at = db.Column(
#         db.DateTime,
#         default=db.func.current_timestamp(),
#         onupdate=db.func.current_timestamp(),
#     )


# class GuestResource(Resource):
#     def get(self):
#         guests = Guest.query.all()
#         data = [
#             {"id": guest.id, "name": guest.name, "occupation": guest.occupation}
#             for guest in guests
#         ]
#         return data


# class SingleGuestResource(Resource):
#     def get(self, guest_id):
#         guest = Guest.query.get(guest_id)
#         if guest:
#             data = {"id": guest.id, "name": guest.name, "occupation": guest.occupation}
#             return data
#         else:
#             return {"error": "Guest not found"}, 404


# class AppearanceResource(Resource):
#     def get(self):
#         appearances = Appearance.query.all()
#         data = [
#             {
#                 "id": appearance.id,
#                 "episode_id": appearance.episode_id,
#                 "guest_id": appearance.guest_id,
#                 "rating": appearance.rating,
#             }
#             for appearance in appearances
#         ]
#         return data


# class SingleAppearanceResource(Resource):
#     def get(self, appearance_id):
#         appearance = Appearance.query.get(appearance_id)
#         if appearance:
#             data = {
#                 "id": appearance.id,
#                 "episode_id": appearance.episode_id,
#                 "guest_id": appearance.guest_id,
#                 "rating": appearance.rating,
#             }
#             return data
#         else:
#             return {"error": "Appearance not found"}, 404


# class EpisodeResource(Resource):
#     def get(self):
#         episodes = Episode.query.all()
#         data = [
#             {"id": episode.id, "date": episode.date, "number": episode.number}
#             for episode in episodes
#         ]
#         return data


# class SingleEpisodeResource(Resource):
#     def get(self, episode_id):
#         episode = Episode.query.get(episode_id)
#         if episode:
#             data = {"id": episode.id, "date": episode.date, "number": episode.number}
#             return data
#         else:
#             return {"error": "Episode not found"}, 404

#     def delete(self, episode_id):
#         episode = Episode.query.get(episode_id)
#         if episode:
#             db.session.delete(episode)
#             db.session.commit()
#             return {"message": "Episode deleted successfully"}
#         else:
#             return {"error": "Episode not found"}, 404


# api.add_resource(EpisodeResource, "/episodes")
# api.add_resource(SingleEpisodeResource, "/episodes/<int:episode_id>")
# api.add_resource(GuestResource, "/guests")
# api.add_resource(SingleGuestResource, "/guests/<int:guest_id>")
# api.add_resource(AppearanceResource, "/appearances")
# api.add_resource(SingleAppearanceResource, "/appearances/<int:appearance_id>")


# if __name__ == "__main__":
#     app.run(port=5555)

from flask import Flask, request
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import requests
import json

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api(app)


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


class GuestResource(Resource):
    def get(self):
        guests = Guest.query.all()
        data = [
            {"id": guest.id, "name": guest.name, "occupation": guest.occupation}
            for guest in guests
        ]
        return data


class SingleGuestResource(Resource):
    def get(self, guest_id):
        guest = Guest.query.get(guest_id)
        if guest:
            data = {"id": guest.id, "name": guest.name, "occupation": guest.occupation}
            return data
        else:
            return {"error": "Guest not found"}, 404


class AppearanceResource(Resource):
    def get(self):
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
        return data

    def post(self):
        # Get the data from the request body
        data = request.get_json()

        # Extract the required properties
        episode_id = data.get("episode_id")
        guest_id = data.get("guest_id")
        rating = data.get("rating")

        # Create a new Appearance object
        appearance = Appearance(episode_id=episode_id, guest_id=guest_id, rating=rating)

        # Add the object to the database session
        db.session.add(appearance)
        db.session.commit()

        return {"message": "Appearance created successfully"}, 201


class SingleAppearanceResource(Resource):
    def get(self, appearance_id):
        appearance = Appearance.query.get(appearance_id)
        if appearance:
            data = {
                "id": appearance.id,
                "episode_id": appearance.episode_id,
                "guest_id": appearance.guest_id,
                "rating": appearance.rating,
            }
            return data
        else:
            return {"error": "Appearance not found"}, 404


class EpisodeResource(Resource):
    def get(self):
        episodes = Episode.query.all()
        data = [
            {"id": episode.id, "date": episode.date, "number": episode.number}
            for episode in episodes
        ]
        return data


class SingleEpisodeResource(Resource):
    def get(self, episode_id):
        episode = Episode.query.get(episode_id)
        if episode:
            data = {"id": episode.id, "date": episode.date, "number": episode.number}
            return data
        else:
            return {"error": "Episode not found"}, 404

    def delete(self, episode_id):
        episode = Episode.query.get(episode_id)
        if episode:
            db.session.delete(episode)
            db.session.commit()
            return {"message": "Episode deleted successfully"}
        else:
            return {"error": "Episode not found"}, 404


api.add_resource(EpisodeResource, "/episodes")
api.add_resource(SingleEpisodeResource, "/episodes/<int:episode_id>")
api.add_resource(GuestResource, "/guests")
api.add_resource(SingleGuestResource, "/guests/<int:guest_id>")
api.add_resource(AppearanceResource, "/appearances")
api.add_resource(SingleAppearanceResource, "/appearances/<int:appearance_id>")


if __name__ == "__main__":
    app.run(port=5555)
