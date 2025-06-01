import pygame
from game import Game
from music import GestionMusique

if __name__ == '__main__':
    pygame.init()
    game = Game()
    game.run()