import pygame

class AnimateSprite(pygame.sprite.Sprite):
    
    def __init__(self, name, colorkey=(0, 0, 0),taille = 32):
        super().__init__()
        self.sprite_sheet = pygame.image.load(f"/home/slidium/Documents/poke_proj/sprites/{name}.png").convert()
        self.animation_index = 0
        self.clock = 0
        self.colorkey = colorkey
        self.taille = taille
        self.images = {
            "down": self.get_images(taille),
            "left": self.get_images(taille*2),
            "right": self.get_images(taille*3),
            "up": self.get_images(0)
        }
        self.speed = 3
        self.image = self.images["down"][self.animation_index]
        self.image.set_colorkey(self.colorkey)

    def change_animation(self, name):
        self.image = self.images[name][self.animation_index]
        self.image.set_colorkey(self.colorkey)
        self.clock += self.speed * 8

        if self.clock >= 100:
            self.animation_index += 1

            if self.animation_index >= len(self.images[name]):
                self.animation_index = 0

            self.clock = 0

    def get_images(self, y):
        images = []
        for i in range(0, 3):
            x = i * self.taille
            image = self.get_image(x, y)
            images.append(image)
        return images

    def get_image(self, x, y):
        image = pygame.Surface([self.taille, self.taille]).convert()
        image.blit(self.sprite_sheet, (0, 0), (x, y, self.taille, self.taille))
        image.set_colorkey(self.colorkey)
        return image
