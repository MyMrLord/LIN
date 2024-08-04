import json
import xml.etree.ElementTree as ET

from Lib import *
class Render:
    def __init__(self, screen, player, data):
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
                print(len(floor))
                if floor[j][i] != 0:
                    layer1.add(Tiles([i, j], [half_size[0], half_size[1]], 1, data))
                if wall[j][i] != 0:
                    layer2.add(Tiles([i, j], [half_size[0], half_size[1]], 2, data))
                if furniture[j][i] != 0:
                    layer3.add(Tiles([i, j], [half_size[0], half_size[1]], 3, data))
                if interact_obj[j][i] != 0:
                    layer3.add(Tiles([i, j], [half_size[0], half_size[1]], 4, data))
                    layer4.add(interact_obj[j][i])
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
    def __init__(self, tile_cor, pl_cor, layer, data):
        pg.sprite.Sprite.__init__(self)
        floor = data['map']['layer1']['floor']
        furniture = data['map']['layer1']['furniture']
        wall = data['map']['layer1']['wall']
        interact_obj = data['map']['layer1']['interact']
        if layer == 1:
            t = floor[tile_cor[1]][tile_cor[0]]
        if layer == 2:
            t = wall[tile_cor[1]][tile_cor[0]]
        if layer == 3:
            t = furniture[tile_cor[1]][tile_cor[0]]
        if layer == 4:
            t = interact_obj[tile_cor[1]][tile_cor[0]]
        self.image = tiles[t-1]
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
tree = ET.parse('Tiles.xml')
root = tree.getroot()
pg.display.init()
tiles = [0] * 94
for i in root.iter('tile'):
    id = int(i.attrib['id'])
    t = list(i.iter('image'))[0].attrib['source'].split('/')[-1]
    t = pg.image.load(f'img/tiles/{t}')
    tiles[id] = pg.transform.scale(t, (t.get_rect()[2] * (scale // 16), t.get_rect()[3] * (scale // 16)))
height = 90
width = 100