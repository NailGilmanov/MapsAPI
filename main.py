import requests
import pygame as pg
import sys
import os

W, H = 600, 450
Z = 15
place = 'Казань'


def param_func(toponym, z):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": toponym,
        "format": "json"}

    res = requests.get(geocoder_api_server, params=geocoder_params)

    if not res:
        print("Ошибка выполнения запроса:")
        print(res)
        print("Http статус:", res.status_code, "(", res.reason, ")")

    # Преобразуем ответ в json-объект
    json_response = res.json()
    # Получаем первый топоним из ответа геокодера
    toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    # Координаты центра топонима:
    toponym_coodrinates = toponym["Point"]["pos"]
    # Долгота и широта:
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

    # Собираем параметры для запроса к StaticMapsAPI:
    return {
        "ll": ",".join([toponym_longitude, toponym_lattitude]),
        "z": f'{z}',
        "l": "map"
    }


def render(place, z):
    map_api_server = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(map_api_server, params=param_func(place, str(z)))

    if not response:
        print("Ошибка выполнения запроса:")
        print(map_api_server)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    pic = "map.png"
    with open(pic, "wb") as file:
        file.write(response.content)

    sc = pg.display.set_mode((W, H))
    sc.fill((100, 150, 200))

    surf = pg.image.load(pic)
    rect = surf.get_rect(bottomright=(W, H))
    sc.blit(surf, rect)


render(place, Z)
FPS = 60
clock = pg.time.Clock()

while 1:
    clock.tick(FPS)

    for i in pg.event.get():
        if i.type == pg.QUIT:
            os.remove('map.png')
            sys.exit()
        elif i.type == pg.KEYDOWN:
            if i.key == pg.K_UP:
                Z = min(Z + 1, 19)
            elif i.key == pg.K_DOWN:
                Z = max(Z - 1, 0)
            render(place, Z)

    pg.display.update()
