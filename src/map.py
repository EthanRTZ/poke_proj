from dataclasses import dataclass
import pygame
import pytmx
import pyscroll
from player import NPC


@dataclass
class Portals:
    from_world: str
    origin_point: str
    target_world: str
    teleport_point: str

@dataclass
class Map:
    name: str
    walls: list[pygame.Rect]
    group: pyscroll.PyscrollGroup
    tmx_data: pytmx.TiledMap
    portals: list[Portals]
    npcs: list[NPC]

class MapManager:

    def __init__(self, screen, player):
        self.maps = dict()
        self.screen = screen
        self.player = player
        self.current_map = "map1"

        self.register_map("map1", portals=[
            Portals(from_world="map1", origin_point="enter_house1", target_world="house1", teleport_point="spawn_house1"),
            Portals(from_world="map1", origin_point="enter_house2", target_world="house2", teleport_point="spawn_house2"),
            Portals(from_world="map1", origin_point="enter_pokecenter", target_world="pokecenter", teleport_point="spawn_pokecenter"),
            Portals(from_world="map1", origin_point="enter_pokeshop", target_world="pokeshop", teleport_point="spawn_pokeshop")
        ],
         npcs=[
            NPC("tkt", nb_points=4, dialog=["Yo , ca va ?", "Quelle beau temps tu ne trouve pas ?"],colorkey = [55,143,87], taille = 32) 
        ])
        self.register_map("house1", portals=[
            Portals(from_world="house1", origin_point="exit_house1", target_world="map1", teleport_point="enter_house1_exit")
        ])

        self.register_map("house2", portals=[
            Portals(from_world="house2", origin_point="exit_house2", target_world="map1", teleport_point="enter_house2_exit")
        ])

        self.register_map("pokeshop", portals=[
            Portals(from_world="pokeshop", origin_point="exit_pokeshop", target_world="map1", teleport_point="enter_pokeshop_exit")
        ])

        self.register_map("pokecenter", portals=[
            Portals(from_world="pokecenter", origin_point="exit_pokecenter", target_world="map1", teleport_point="enter_pokecenter_exit")
        ])

        self.teleport_player("player")
        self.teleport_ncps()

    def check_npc_collisions(self, dialog_box):
        for sprite in self.get_group().sprites():
            if sprite.feet.colliderect(self.player.rect) and type(sprite) is NPC:
                dialog_box.execute(sprite.dialog)

    def check_collision(self):
        # Portails
        for portal in self.get_map().portals:
            if portal.from_world == self.current_map:
                point = self.get_object(portal.origin_point)
                rect = pygame.Rect(point.x, point.y, point.width, point.height)

                if self.player.feet.colliderect(rect):
                    copy_portal = portal
                    self.current_map = portal.target_world
                    self.teleport_player(copy_portal.teleport_point)
        # Collision
        for sprite in self.get_group().sprites():

            if type(sprite) is NPC:
                if sprite.feet.colliderect(self.player.rect):
                    sprite.speed = 0
                else:
                    sprite.speed = 1

            if sprite.feet.collidelist(self.get_walls()) > -1:
                sprite.move_back()

    def teleport_player(self, name):
        point = self.get_object(name)
        self.player.position[0] = point.x
        self.player.position[1] = point.y
        self.player.save_location()

    def register_map(self, name, portals=[], npcs=[]):
        # Charger la carte classique
        tmx_data = pytmx.util_pygame.load_pygame(f"/home/slidium/Documents/poke_proj/map/{name}.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 4

        # Les collisions
        walls = []

        for obj in tmx_data.objects:
            if obj.type == "collision":
                walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # Dessiner les différents calques
        group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=3)
        group.add(self.player)

        #recuperer tous les NPC pour les ajouter au groupe
        for npc in npcs:
            group.add(npc)

        # Créer un objet Map
        self.maps[name] = Map(name, walls, group, tmx_data, portals, npcs)

    def get_map(self):
        return self.maps[self.current_map]

    def get_group(self):
        return self.get_map().group

    def get_walls(self):
        return self.get_map().walls

    def get_object(self, name):
        return self.get_map().tmx_data.get_object_by_name(name)

    def teleport_ncps(self):
        for map_name in self.maps:
            map_data = self.maps[map_name]
            ncps = map_data.npcs

            for npc in ncps:
                npc.load_points(map_data.tmx_data)
                npc.teleport_spawn()

    def draw(self):
        self.get_group().draw(self.screen)
        self.get_group().center(self.player.rect.center)

    def update(self):
        self.get_group().update()
        self.check_collision()

        for npc in self.get_map().npcs:
            npc.move()
