import uuid
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


def connect_db():
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)  # creating tables
    session = sessionmaker(engine)

    return session()


def valid_email(email):
    if email.count("@") == 1 and email.rfind(".") > email.rfind("@"):
        return True
    else:
        return False


def valid_date(birthdate):
    if len(birthdate) == 10 and birthdate[4] == '-' and birthdate[7] == '-':
        for item in birthdate.split('-'):
            if item.isdigit() is False:
                return False
        if int(birthdate.split('-')[1]) > 12 or int(birthdate.split('-')[2]) > 31:
            return False
        return True
    else:
        return False


def valid_height(height):
    for item in height.split('.'):
        if item.isdigit() is False:
            return False
        else:
            return True


def request_data():
    print("Please input your data")
    first_name = input("Input first name: ").capitalize()
    last_name = input("Input last name: ").capitalize()
    gender = input("Input your gender: ").capitalize()
    email = input("Input your email: ")
    while valid_email(email) is False:
        print("Invalid email, please try again: ")
        email = input("Input your email: ")
    birthdate = input("Input your date of birth, YYYY-MM-DD: ")
    while valid_date(birthdate) is False:
        print("Invalid birthdate, please try again: ")
        birthdate = input("Input your date of birth, YYYY-MM-DD: ")
    height = input("Input your height, m: ")
    while valid_height(height) is False:
        print("Invalid height, please try again: ")
        height = input("Input your height, m: ")

    user = User(
        first_name=first_name,
        last_name=last_name,
        gender=gender,
        email=email,
        birthdate=birthdate,
        height=height
    )
    return user


def main():
    session = connect_db()
    user = request_data()
    session.add(user)
    session.commit()
    print("Thank You, your data are saved.")


if __name__ == "__main__":
    main()
