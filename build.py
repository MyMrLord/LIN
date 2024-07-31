from Lavr import Player
import Rendering
from Lib import *

pg.init()

pg.event.set_allowed([pg.QUIT])

screen = pg.display.set_mode(size)
pg.display.set_caption('LIN')
clock = pg.time.Clock()

player = Player.Player([1000, 1030])
PLayer_init()

rendering = Rendering.Render(screen, player)
player.render = rendering

run = True
while run:
    for i in pg.event.get():
        if i.type == pg.QUIT:
            run = False
    player.update()

    rendering.render()

    pg.display.flip()
    clock.tick(fps)
pg.quit()