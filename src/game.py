import pygame
import pytmx
import pyscroll
from player import Player
from dialog import DialogBox
from map import MapManager
from music import GestionMusique  # Assurez-vous que le nom du fichier est correct

class Game:

    def __init__(self):
        # Démarrage
        self.running = True
        self.map = "map1"

        # Affichage de la fenêtre
        self.screen = pygame.display.set_mode((1920, 1080))
        pygame.display.set_caption("zeldo")

        # Initialisation du joystick
        pygame.joystick.init()
        self.joystick = None
        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()

        # Générer le joueur
        self.player = Player()
        self.map_manager = MapManager(self.screen, self.player)
        self.dialog_box = DialogBox()
        self.gestion_musique = GestionMusique()
        
        # Jouer la musique initiale
        self.gestion_musique.mise_a_jour_musique(self.map)

    def handle_input(self):
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_ESCAPE]:
            self.running = False
        elif pressed[pygame.K_UP]:
            self.player.move_up()
        elif pressed[pygame.K_DOWN]:
            self.player.move_down()
        elif pressed[pygame.K_RIGHT]:
            self.player.move_right()
        elif pressed[pygame.K_LEFT]:
            self.player.move_left()

        if self.joystick:
            axis_x = self.joystick.get_axis(0)
            axis_y = self.joystick.get_axis(1)

            # Empêcher le mouvement diagonal
            if abs(axis_x) > abs(axis_y):
                if axis_x < -0.5:
                    self.player.move_left()
                elif axis_x > 0.5:
                    self.player.move_right()
            else:
                if axis_y < -0.5:
                    self.player.move_up()
                elif axis_y > 0.5:
                    self.player.move_down()

    def update(self):
        self.map_manager.update()
        
        # Vérifier si la carte a changé et mettre à jour la musique
        nouvelle_map = self.map_manager.get_map()  # Assurez-vous d'avoir cette méthode ou équivalent
        if nouvelle_map != self.map:
            self.map = nouvelle_map
            self.gestion_musique.mise_a_jour_musique(self.map)

    def run(self):
        clock = pygame.time.Clock()

        while self.running:

            self.player.save_location()
            self.handle_input()
            self.update()
            self.map_manager.draw()
            self.dialog_box.render(self.screen)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.map_manager.check_npc_collisions(self.dialog_box)

            clock.tick(60)

        pygame.quit()


if __name__ == "__main__":
    pygame.init()
    game = Game()
    game.run()
