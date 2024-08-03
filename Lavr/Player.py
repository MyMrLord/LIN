from Lib import *
from Rendering import Tiles, furniture, wall

class Player(pg.sprite.Sprite):
    def __init__(self, data):
        pg.sprite.Sprite.__init__(self)
        self.image = player_anim['5'][0]
        t = self.image.get_rect()
        self.rect = pg.rect.Rect((t[0], t[1], t[2] - 5, t[3] - 5))
        self.rect.center = half_size
        self.render = 0

        self.pos_sc = data['pos'].copy()
        self.pos_pl = data['pos'].copy()
        self.vector = 5
        self.player_speed = scale // 8
        self.scet = 0
        self.level = 0
        self.tangible_obj = pg.sprite.Group()

    def check_rout(self):
        self.tangible_obj = pg.sprite.Group()
        for i in range(self.pos_pl[0] // scale - rad_grip, self.pos_pl[0] // scale + rad_grip + 1):
            for j in range(self.pos_pl[1] // scale - rad_grip, self.pos_pl[1] // scale + rad_grip + 1):
                if furniture[j][i] != 0:
                    t = Tiles([i, j], self.pos_sc, 3)
                    t.type_text = furniture[j][i]
                    x = t.image.get_rect()
                    t.rect.y += x[3] - scale
                    self.tangible_obj.add(t)
                if wall[j][i] != 0:
                    t = Tiles([i, j], self.pos_sc, 2)
                    t.type_text = wall[j][i]
                    x = t.image.get_rect()
                    t.rect.y += x[3] - scale
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
    def update(self):
        self.check_rout()
        self.movement()
        self.render.all_sc.add(self)