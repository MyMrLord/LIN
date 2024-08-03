from Lavr import Player
import Rendering
from Lib import *
import json
class Build:
    def __init__(self):
        self.data = {}
    def building(self, **kwgs):
        pg.init()

        pg.event.set_allowed([pg.QUIT])

        screen = pg.display.set_mode(size)
        pg.display.set_caption('LIN')
        clock = pg.time.Clock()

        rendering = Rendering.Render(screen, kwgs['player'], self.data)
        kwgs['player'].render = rendering

        run = True
        while run:
            for i in pg.event.get():
                if i.type == pg.QUIT:
                    run = False
            for i in kwgs:
                kwgs[i].update()

            rendering.update()

            pg.display.flip()
            clock.tick(fps)
        pg.quit()
    def connect_data_with_build(self):
        with open('data.json') as f:
            self.data = json.load(f)
        for i in self.data:
            if i == 'player':
                player = Player.Player(self.data[i])
            if i == 'map':
                if self.data['map'][self.data['player']['layer']] == 0:
                    self.create_map(self.data['player']['layer'])

        build.building(player=player)
    def save_game(self):
        with open('data.json') as f:
            json.dump(self.data, f)
    def create_map(self, layer):
        self.data['map'][layer] = {'floor': [], 'wall': [], 'furniture': [], 'interact': []}
        with open('layer1.xml') as f:
            import xml.etree.ElementTree as ET
            tree = ET.parse('layer1.xml')
            root = tree.getroot()
            for elem in root.iter('layer'):
                if elem.attrib['name'] == 'floor':
                    for i in list(elem.iter('data'))[0].text.split('\n'):
                        if i.split() == []:
                            continue
                        if i[-1] == ",":
                            i = i[:-1]
                        self.data['map'][layer]['floor'].append(list(map(int, i.split(','))))
                if elem.attrib['name'] == 'wall':
                    for i in list(elem.iter('data'))[0].text.split('\n'):
                        if i.split() == []:
                            continue
                        if i[-1] == ",":
                            i = i[:-1]
                        self.data['map'][layer]['wall'].append(list(map(int, i.split(','))))
                if elem.attrib['name'] == 'furniture':
                    for i in list(elem.iter('data'))[0].text.split('\n'):
                        if i.split() == []:
                            continue
                        if i[-1] == ",":
                            i = i[:-1]
                        self.data['map'][layer]['furniture'].append(list(map(int, i.split(','))))
                if elem.attrib['name'] == 'interact':
                    for i in list(elem.iter('data'))[0].text.split('\n'):
                        if i.split() == []:
                            continue
                        if i[-1] == ",":
                            i = i[:-1]
                        self.data['map'][layer]['interact'].append(list(map(int, i.split(','))))

build = Build()