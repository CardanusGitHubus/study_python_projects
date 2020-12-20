from bottle import route
from bottle import run
from bottle import HTTPError
from bottle import request

import album


@route("/albums/<artist>")
def albums(artist):
    albums_list = album.find(artist)
    if not albums_list:
        message = "Альбомов {} не найдено".format(artist)
        result = HTTPError(404, message)
    else:
        album_names = [album.album for album in albums_list]
        result = "Найдено {} альбомов {}:<br>".format(len(album_names), artist)
        result += "<br>".join(album_names)
    return result


@route("/albums", method="POST")
def album_init():
    year = request.forms.get("year")
    artist = request.forms.get("artist")
    genre = request.forms.get("genre")
    album_name = request.forms.get("album")

    try:
        year = int(year)
    except ValueError:
        return HTTPError(400, "Год альбома должен состоять из цифр")

    try:
        album.save_album(year, artist, genre, album_name)
    except album.AlreadyExists as err:
        result = HTTPError(409, err)
    except album.CommitError as err:
        result = HTTPError(400, err)
    else:
        result = "Данные успешно сохранены"
        print("Album saved")
    return result


if __name__ == "__main__":
    run(host="localhost", port=8080, debug=True)
