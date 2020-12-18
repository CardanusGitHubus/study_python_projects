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
        result = "Найдено {} альбомов {}: ".format(len(album_names), artist)
        result += ", ".join(album_names)
    return result


@route("/albums", method="POST")
def album_init():
    year_ = request.forms.get("year")
    if year_.isdigit() is False:
        raise ValueError("Год должен содержать только цифры")
    album_data = {
        "year": year_,
        "artist": request.forms.get("artist"),
        "genre": request.forms.get("genre"),
        "album": request.forms.get("album")
    }
    try:
        album.save_album(album_data)
    except album.CommitError as err:
        result = HTTPError(409)
        print("Invalid album data: ", err)
        return result
    else:
        print("Album saved")
        return "Данные успешно сохранены"


if __name__ == "__main__":
    run(host="localhost", port=8080, debug=True)
