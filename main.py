import requests
import pygame as pg
import sys
import os

pg.font.init()


def start_coordinates(toponym):
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
    return toponym_coodrinates.split(" ")


def param_func(x, y, z, map_type):
    # Собираем параметры для запроса к StaticMapsAPI:
    return {
        "ll": ",".join([x, y]),
        "z": f'{z}',
        "l": {map_type},
        "size": "650,450"
    }


def render(x, y, z):
    map_api_server = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(map_api_server, params=param_func(x, y, str(z), maptype))

    if not response:
        print("Ошибка выполнения запроса:")
        print(map_api_server)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    pic = "map.png"
    with open(pic, "wb") as file:
        file.write(response.content)

    sc = pg.display.set_mode((W, H))
    sc.fill((120, 170, 200))

    surf = pg.image.load(pic)
    rect = surf.get_rect(bottomright=(W, H))

    f1 = pg.font.Font(None, 36)
    text1 = f1.render('Yandex.Maps', True,
                      (0, 0, 0))

    f2 = pg.font.SysFont('serif', 48)
    text2 = f2.render("World Мир", False,
                      (0, 0, 0))

    f3 = pg.font.SysFont(None, 32)
    text3 = f3.render('"L" - переключить', True,
                      (0, 0, 0))
    text4 = f3.render('режим карты.', True,
                      (0, 0, 0))

    sc.blit(text1, (10, 50))
    sc.blit(text2, (10, 100))
    sc.blit(text3, (10, 400))
    sc.blit(text4, (13, 423))

    sc.blit(surf, rect)


maptype = 'map'
LAT_STEP = 0.008  # Шаги при движении карты по широте и долготе
LON_STEP = 0.002
W, H = 900, 450
Z = 15
place = 'Казань'
longitude, lattitude = start_coordinates(place)
render(longitude, lattitude, Z)
FPS = 60
clock = pg.time.Clock()

while 1:
    clock.tick(FPS)

    for i in pg.event.get():
        if i.type == pg.QUIT:
            os.remove('map.png')
            sys.exit()
        elif i.type == pg.KEYDOWN:
            if i.key == pg.K_PAGEUP:
                Z = min(Z + 1, 19)
            elif i.key == pg.K_PAGEDOWN:
                Z = max(Z - 1, 0)
            elif i.key == pg.K_UP:
                lattitude = str(float(lattitude) + LON_STEP)
            elif i.key == pg.K_DOWN:
                lattitude = str(float(lattitude) - LON_STEP)
            elif i.key == pg.K_RIGHT:
                longitude = str(float(longitude) + LAT_STEP)
            elif i.key == pg.K_LEFT:
                longitude = str(float(longitude) - LAT_STEP)
            elif i.key == pg.K_l:
                if maptype == 'map':
                    maptype = 'sat'
                elif maptype == 'sat':
                    maptype = 'sat,skl'
                else:
                    maptype = 'map'

            render(longitude, lattitude, Z)

    pg.display.update()
