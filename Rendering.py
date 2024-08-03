import json

from Lib import *
class Render:
    def __init__(self, screen, player, data):
        global floor, wall, furniture, interact_obj
        floor = data['map']['layer1']['floor']
        furniture = data['map']['layer1']['furniture']
        wall = data['map']['layer1']['wall']
        interact_obj = data['map']['layer1']['interact']
        self.sc = screen
        self.l1 = pg.Surface(size)
        self.player = player
        self.all_l1 = pg.sprite.Group()
        self.all_sc = pg.sprite.Group()

        self.layer = pg.Surface((scale * 96, scale * 96))
        self.layer.set_colorkey((0, 0, 0))
        self.layer_floor = pg.Surface((scale * 96, scale * 96))
        self.layer_floor.set_colorkey((0, 0, 0))
        self.office = [self.layer]
        layer1 = pg.sprite.Group()
        layer2 = pg.sprite.Group()
        layer3 = pg.sprite.Group()
        layer4 = set()
        for i in range(width):
            for j in range(height):
                if floor[j][i] != 0:
                    layer1.add(Tiles([i, j], [half_size[0], half_size[1]], 1))
                if wall[j][i] != 0:
                    layer2.add(Tiles([i, j], [half_size[0], half_size[1]], 2))
                if furniture[j][i] != 0:
                    layer3.add(Tiles([i, j], [half_size[0], half_size[1]], 3))
                if interact_obj[j][i] != 0:
                    print(interact_obj[j][i], end=" = ")
                    layer3.add(Tiles([i, j], [half_size[0], half_size[1]], 4))
                    layer4.add(self.interact_obj[j][i])
        layer1.draw(self.layer_floor)
        layer2.draw(self.layer)
        layer3.draw(self.layer)

    def rend_world(self):
        self.l1.blit(self.layer_floor, (-self.player.pos_sc[0] + half_size[0], -self.player.pos_sc[1] + half_size[1]))
        self.all_sc.draw(self.l1)
        self.l1.blit(self.office[self.player.level], (-self.player.pos_sc[0] + half_size[0], -self.player.pos_sc[1] + half_size[1]))
        self.all_l1.draw(self.l1)
        self.sc.blit(self.l1, (0,0))
    def update(self):
        self.sc.fill((0,0,0))
        self.l1.fill((0,0,0))
        self.l1.set_colorkey((0,0,0))

        self.rend_world()
        self.all_l1 = pg.sprite.Group()
        self.all_sc = pg.sprite.Group()
class Tiles(pg.sprite.Sprite):
    def __init__(self, tile_cor, pl_cor, layer):
        pg.sprite.Sprite.__init__(self)
        if layer == 1:
            t = floor[tile_cor[1]][tile_cor[0]]
        if layer == 2:
            t = wall[tile_cor[1]][tile_cor[0]]
        if layer == 3:
            t = furniture[tile_cor[1]][tile_cor[0]]
        if layer == 4:
            t = interact_obj[tile_cor[1]][tile_cor[0]]
        self.image = tiles[t]
        print(tiles[t], t)
        t = self.image.get_rect()
        self.rect = pg.rect.Rect((0, 0, t[2], scale))
        self.rect.x = tile_cor[0] * scale - pl_cor[0] + half_size[0]
        self.rect.y = tile_cor[1] * scale - pl_cor[1] + half_size[1] - t[3] + scale
with open('data.json') as f:
    data = json.load(f)
floor = 0
furniture = 0
wall = 0
interact_obj = 0