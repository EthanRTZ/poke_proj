import pygame

class GestionMusique:
    def __init__(self):
        pygame.mixer.init()
        self.musique_actuelle = None

    def jouer_musique(self, nom_fichier):
        if self.musique_actuelle != nom_fichier:
            pygame.mixer.music.load(f"music/{nom_fichier}")
            pygame.mixer.music.play(-1)
            self.musique_actuelle = nom_fichier

    def mise_a_jour_musique(self, map_actuelle):
        if map_actuelle == "map1":
            self.jouer_musique("current.mp3")
        elif map_actuelle == "house1" or "house2":
            self.jouer_musique("house.mp3")
        elif map_actuelle == "pokecenter":
            self.jouer_musique("pokecenter.mp3")
        elif map_actuelle == "pokeshop":
            self.jouer_musique("pokeshop.mp3")  # Musique par défaut

    def arreter_musique(self):
        pygame.mixer.music.stop()
        self.musique_actuelle = None
