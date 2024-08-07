from Lib import *
from Rendering import Tiles, player_anim, translater, width, height, all_notification
from copy import deepcopy

class Player(pg.sprite.Sprite):
    def __init__(self, data):
        pg.sprite.Sprite.__init__(self)
        self.image = player_anim['5'][0]
        t = self.image.get_rect()
        self.rect = pg.rect.Rect((t[0], t[1], t[2] - 5, t[3] - 5))
        self.rect.center = half_size
        self.render = 0

        self.pos_sc = data['player']['pos'].copy()
        self.pos_pl = data['player']['pos'].copy()
        self.vector = 5
        self.player_speed = scale // 8
        self.scet = 0
        self.level = 0
        self.tangible_obj = pg.sprite.Group()
        self.data = data

    def check_rout(self):
        self.tangible_obj = pg.sprite.Group()
        for i in range(self.pos_pl[0] // scale - rad_grip, self.pos_pl[0] // scale + rad_grip + 1):
            for j in range(self.pos_pl[1] // scale - rad_grip, self.pos_pl[1] // scale + rad_grip + 1):
                if self.data['map']['layer1']["furniture"][j][i] != 0:
                    t = Tiles([i, j], self.pos_sc, 3, self.data)
                    t.type_text = self.data['map']['layer1']["furniture"][j][i]
                    x = t.image.get_rect()
                    t.rect.y += x[3] - scale
                    self.tangible_obj.add(t)
                if self.data['map']['layer1']["wall"][j][i] != 0:
                    t = Tiles([i, j], self.pos_sc, 2, self.data)
                    t.type_text = self.data['map']['layer1']["wall"][j][i]
                    x = t.image.get_rect()
                    t.rect.y += x[3] - scale
                    self.tangible_obj.add(t)
                if self.data['map']['layer1']["interact"][j][i] != 0:
                    t = Tiles([i, j], self.pos_sc, 4, self.data)
                    t.type_text = self.data['map']['layer1']["interact"][j][i]
                    x = t.image.get_rect()
                    t.rect.y += x[3] - scale
                    t.type = self.data['map']['layer1']["interact"][j][i] - 1
                    self.tangible_obj.add(t)

    def movement(self):
        keystate = pg.key.get_pressed()
        x = 0
        y = 0
        if keystate[pg.K_d]:
            x += self.player_speed
        if keystate[pg.K_a]:
            x -= self.player_speed
        if keystate[pg.K_s]:
            y += self.player_speed
        if keystate[pg.K_w]:
            y -= self.player_speed
        if not(x == y and x == 0):
            self.scet += 1
            k = 24 // self.player_speed
            self.scet %= k * 4
            self.vector = translater[f'{(x // self.player_speed,y // self.player_speed)}']
            self.image = player_anim[str(self.vector)][self.scet // k]
        else:
            self.image = player_anim[str(self.vector)][0]
        etalon = self.rect.center
        if x != 0 or y != 0:
            self.rect.center = (self.rect.center[0], self.rect.center[1] + y)
            if pg.sprite.spritecollideany(self, self.tangible_obj):
                y = 0
            self.rect.center = (etalon[0] + x, etalon[1])
            if pg.sprite.spritecollideany(self, self.tangible_obj):
                x = 0
            self.rect.center = (etalon[0] + x, self.rect.center[1] + y)
            if pg.sprite.spritecollideany(self, self.tangible_obj):
                x = 0
                y = 0
        else:
            self.rect.center = (self.rect.center[0], self.rect.center[1] + y)
            if pg.sprite.spritecollideany(self, self.tangible_obj):
                y = 0
            self.rect.center = (etalon[0] + x, etalon[1])
            if pg.sprite.spritecollideany(self, self.tangible_obj):
                x = 0
        self.rect.center = etalon
        if self.pos_pl[0] + x >= width * scale or self.pos_pl[0] + x <= 0:
            x = 0
        if self.pos_pl[1] + y >= height * scale or self.pos_pl[1] + y <= 0:
            y = 0
        if self.rect.center[0] + x <= size[0] // 3 * 2 and self.rect.center[0] + x >= size[0] // 3:
            self.pos_pl[0] += x
            self.rect.center = (self.rect.center[0] + x, self.rect.center[1])
        else:
            self.pos_sc[0] += x
            self.pos_pl[0] += x
        if self.rect.center[1] + y <= size[1] // 3 * 2 and self.rect.center[1] + y >= size[1] // 3:
            self.pos_pl[1] += y
            self.rect.center = (self.rect.center[0], self.rect.center[1] + y)
        else:
            self.pos_sc[1] += y
            self.pos_pl[1] += y
    def rend_obj(self):
        keystate = pg.key.get_pressed()
        for i in range((self.pos_sc[0] - half_size[0] - rad_grip * scale) // scale, (self.pos_sc[0] + half_size[0] + rad_grip * scale) // scale + 1):
            for j in range((self.pos_sc[1] - half_size[1] - rad_grip * scale) // scale, (self.pos_sc[1] + half_size[1] + rad_grip * scale) // scale + 1):
                if self.data['map']['layer1']["interact"][j][i] != 0:
                    t = Tiles([i, j], self.pos_sc, 4, self.data)   # Тут глобальная кор вместо локальной !!!!
                    t.type = self.data['map']['layer1']["interact"][j][i] - 1
                    etalon = t.rect.center
                    self.render.all_l1.add(deepcopy(t))
                    x = t.image.get_rect()
                    t.rect.size = (x[2] + rad_grip * scale, x[3] + rad_grip * scale)
                    t.rect.center = etalon
                    x = pg.sprite.GroupSingle()
                    x.add(t)
                    elem = t.type
                    in_range = bool(pg.sprite.spritecollideany(self, x))
                    # Можешь вписывать код сюда, фильтруя через if
                    if elem in self.data['map']['items'] and in_range:
                        x = all_notification['up_items']
                        self.render.rend_surface(x[0].render(x[2], True, x[3]), (300, 300))
                        if keystate[pg.K_r]:
                            self.data['map']['layer1']['interact'][j] = \
                            self.data['map']['layer1']['interact'][j][:i] + [0] + \
                            self.data['map']['layer1']['interact'][j][i + 1:]
                            self.render.all_l1.remove(t)
                            self.tangible_obj.remove(t)
    def update(self):
        self.check_rout()
        self.movement()
        self.rend_obj()
        self.render.all_sc.add(self)