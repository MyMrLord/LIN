import pygame as pg

def PLayer_init():
    pass
#Параметры константы
fps = 30
size = (480 * 2, 360 * 2)
half_size = (size[0] // 2, size[1] // 2)
scale = 48
rad_grip = 3
translater = {f'{(0, -1)}': 1, f'{(1, -1)}': 2, f'{(1, 0)}': 3, f'{(1, 1)}': 4, f'{(0, 1)}': 5, f'{(-1, 1)}': 6, f'{(-1, 0)}': 7, f'{(-1, -1)}': 8}
#Картинки
player_anim = {}
for i in range(0, 32):
    x = pg.image.load(f'img/player_anim/{i // 4 + 1}.{i % 4}.png')
    if not(f'{i // 4 + 1}' in player_anim):
        player_anim[f'{i // 4 + 1}'] = []
    x = pg.transform.scale(x, (scale, scale))
    x.set_colorkey((48,104,80), 10)
    player_anim[f'{i // 4 + 1}'].append(x)
tiles = [0]
pg.display.init()
for i in range(93):
    try:
        t = pg.image.load(f'img/tiles/{i+1}.png')
        tiles.append(pg.transform.scale(t, (t.get_rect()[2] * (scale // 16), t.get_rect()[3] * (scale // 16))))
    except FileNotFoundError:
        tiles.append(0)
height = 96
width = 96