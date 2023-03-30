"""Script to seed database."""

import os
import json
from random import choice, randint
from datetime import datetime

import crud
import model
import server

os.system("dropdb ratings")
os.system('createdb ratings')

model.connect_to_db(server.app)
model.db.create_all()

with open('data/movies.json') as f:
    movie_data = json.loads(f.read())


# Creates movies, stored in list w/ fake ratings
db_movies = []
for m in movie_data:
    title = m["title"]
    overview = m["overview"]
    poster_path = m["poster_path"]
    release_date = datetime.strptime(m["release_date"], "%Y-%m-%d")

    db_m = crud.create_movie(title, overview, release_date, poster_path)
    db_movies.append(db_m)

model.db.session.add_all(db_movies)
model.db.session.commit()


for i in range(10):
    email = f"email{i}@gmail.com"
    password = "password{i}"

    user = crud.create_user(email, password)
    model.db.session.add(user)

    for j in range(10):
        random_m = choice(db_movies)
        rating = crud.create_rating(user, random_m, randint(1,5))
        model.db.session.add(rating)

model.db.session.commit()


