from faker import Faker
from random import sample
from app import app, db
from models import Guest, Episode, Appearance

fake = Faker()

with app.app_context():
    # Seed fake guests
    guests = []
    for _ in range(20):
        guest = Guest(
            name=fake.name(),
            occupation=fake.job(),
        )
        guests.append(guest)
        db.session.add(guest)

    # Seed fake episodes
    episodes = []
    for i in range(1, 21):
        episode = Episode(
            date=fake.date_this_decade(),
            number=i,
        )
        episodes.append(episode)
        db.session.add(episode)

    db.session.commit()

    # Seed appearances
    appearances = []
    guest_ids = [guest.id for guest in guests]
    episode_ids = [episode.id for episode in episodes]

    for _ in range(20):
        random_guests = sample(guest_ids, k=20)
        random_episodes = sample(episode_ids, k=20)

        for guest_id, episode_id in zip(random_guests, random_episodes):
            appearance = Appearance(
                episode_id=episode_id,
                guest_id=guest_id,
                rating=fake.random_int(min=1, max=10),
            )
            appearances.append(appearance)
            db.session.add(appearance)

    db.session.commit()
    print("Data seeded successfully.")
