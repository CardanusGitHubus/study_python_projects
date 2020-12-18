import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


DB_PATH = "sqlite:///albums.sqlite3"
Base = declarative_base()


class Album(Base):
    """
    Описывает структуру таблицы album для хранения записей музыкальной библиотеки
    """

    __tablename__ = "album"

    id = sa.Column(sa.INTEGER, primary_key=True)
    year = sa.Column(sa.INTEGER)
    artist = sa.Column(sa.TEXT)
    genre = sa.Column(sa.TEXT)
    album = sa.Column(sa.TEXT)


class CommitError(Exception):
    """
    Исключение в случае, если добавляемый альбом уже существует в базе данных
    """
    pass


def connect_db():
    """
    Устанавливает соединение к базе данных, создает таблицы, если их еще нет и возвращает объект сессии
    """
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()


def find(artist):
    """
    Находит все альбомы в базе данных по заданному артисту
    """
    session = connect_db()
    albums = session.query(Album).filter(Album.artist == artist).all()
    return albums


def save_album(album):
    """
    Добавляет данные из словаря в объект альбома и сохраняет альбом в базу данных, если альбома
    с таким названием и исполнителем еще нет
    """
    session = connect_db()
    album = Album(
        year=album["year"],
        artist=album["artist"],
        genre=album["genre"],
        album=album["album"]
    )
    is_albums = session.query(Album).filter(Album.artist == album.artist, Album.album == album.album).all()
    if is_albums:
        raise CommitError("Such album is already exists")
    session.add(album)
    session.commit()
