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
    Исключение в случае, если заполнены не все поля данных при сохранении альбома
    """
    pass


class AlreadyExists(CommitError):
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


def save_album(year, artist, genre, album_name):
    """
    Добавляет данные из словаря в объект альбома и сохраняет альбом в базу данных, если альбома
    с таким названием и исполнителем еще нет
    """
    if not isinstance(artist, str) or not isinstance(genre, str) or not isinstance(album_name, str):
        raise CommitError("Заполнены не все поля данных")
    else:
        session = connect_db()
        album = Album(
            year=year,
            artist=artist,
            genre=genre,
            album=album_name
        )
        is_album = session.query(Album).filter(Album.artist == album.artist, Album.album == album.album).first()
        if is_album:
            raise AlreadyExists("Such album is already exists")
        session.add(album)
        session.commit()

