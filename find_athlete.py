import datetime

import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


DB_PATH = "sqlite:///sochi_athletes.sqlite3"
Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = sa.Column(sa.Integer, primary_key=True)
    first_name = sa.Column(sa.Text)
    last_name = sa.Column(sa.Text)
    gender = sa.Column(sa.Text)
    email = sa.Column(sa.Text)
    birthdate = sa.Column(sa.Text)
    height = sa.Column(sa.REAL)


class Athlete(Base):
    __tablename__ = 'athelete'

    id = sa.Column(sa.Integer, primary_key=True)
    age = sa.Column(sa.Integer)
    birthdate = sa.Column(sa.Text)
    gender = sa.Column(sa.Text)
    height = sa.Column(sa.REAL)
    name = sa.Column(sa.Text)
    weight = sa.Column(sa.Integer)
    gold_medals = sa.Column(sa.Integer)
    silver_medals = sa.Column(sa.Integer)
    bronze_medals = sa.Column(sa.Integer)
    total_medals = sa.Column(sa.Integer)
    sport = sa.Column(sa.Text)
    country = sa.Column(sa.Text)

    def __str__(self):
        return f'{self.id} | {self.birthdate} | {self.height} | {self.name}'


def connect_db():
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)  # creating tables
    session = sessionmaker(engine)

    return session()


def nearest_height(user, session):
    user_height = user.height
    athletes = session.query(Athlete).all()  # all athletes
    min_diff = None
    athlete_id = None

    for athlete in athletes:
        if athlete.height is None:
            continue
        diff = abs(user_height - athlete.height)
        if min_diff is None or diff < min_diff:
            min_diff = diff
            athlete_id = athlete.id

    return athlete_id


def nearest_birthdate(user, session):
    user_birthdate = datetime.date.fromisoformat(user.birthdate)
    athletes = session.query(Athlete).all()  # all athletes
    min_diff = None
    athlete_id = None

    for athlete in athletes:
        if athlete.birthdate is None:
            continue
        athlete_birthdate = datetime.date.fromisoformat(athlete.birthdate)
        diff = abs(user_birthdate - athlete_birthdate)
        if min_diff is None or diff < min_diff:
            min_diff = diff
            athlete_id = athlete.id

    return athlete_id


def main():
    session = connect_db()
    user_id = input("Input a user's id to find a user: ")
    user = session.query(User).filter(User.id == user_id).first()
    if user is None:
        print("There are no users with this ID.")
    else:
        nearest_height_id = nearest_height(user, session)
        nearest_height_athlete = session.query(Athlete).filter(Athlete.id == nearest_height_id).first()
        print("Nearest athlete by height: ", nearest_height_athlete)

        nearest_birthdate_id = nearest_birthdate(user, session)
        nearest_birthdate_athlete = session.query(Athlete).filter(Athlete.id == nearest_birthdate_id).first()
        print("Nearest athlete by birthdate: ", nearest_birthdate_athlete)


if __name__ == "__main__":
    main()
