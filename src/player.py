import pygame

from animation import AnimateSprite


class Entity(AnimateSprite):

    def __init__(self, name, x, y, colorkey, taille):
        super().__init__(name)
        self.colorkey = colorkey
        self.image = self.get_image(0, 0)
        self.image.set_colorkey(self.colorkey)
        self.rect = self.image.get_rect()
        self.position = [x, y]
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 12)
        self.old_position = self.position.copy()
        self.taille = taille 

    def get_image(self, x, y):
        # Your logic to get an image
        image = super().get_image(x, y)
        image.set_colorkey(self.colorkey)
        return image

    def get(self):
        self.image = self.images["down"]
        self.image.set_colorkey(self.colorkey)
        return self.image

    def save_location(self):
        self.old_position = self.position.copy()

    def move_up(self):
        self.change_animation("up")
        self.position[1] -= self.speed

    def move_down(self):
        self.change_animation("down")
        self.position[1] += self.speed

    def move_right(self):
        self.change_animation("right")
        self.position[0] += self.speed

    def move_left(self):
        self.change_animation("left")
        self.position[0] -= self.speed

    def change_animation(self, name):
        super().change_animation(name)
        self.image.set_colorkey(self.colorkey)

    def update(self):
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    def move_back(self):
        self.position = self.old_position
        self.update()


class Player(Entity):

    def __init__(self):
        super().__init__('player', 0, 0, [55, 130, 52], taille = 32)  # Replace with player's specific colorkey
        

class NPC(Entity):

    def __init__(self, name, nb_points, dialog, colorkey, taille):
        super().__init__(name, 0, 0, colorkey, taille)
        self.name = name
        self.dialog = dialog
        self.nb_points = nb_points
        self.points = []
        self.speed = 1
        self.current_point = 0
        self. taille = taille

    def move(self):
        current_point = self.current_point
        target_point = self.current_point + 1

        if target_point >= self.nb_points:
            target_point = 0

        current_rect = self.points[current_point]
        target_rect = self.points[target_point]

        if current_rect.y < target_rect.y and abs(current_rect.x - target_rect.x) < 3:
            self.move_down()
        elif current_rect.y > target_rect.y and abs(current_rect.x - target_rect.x) < 3:
            self.move_up()
        elif current_rect.x > target_rect.x and abs(current_rect.y - target_rect.y) < 3:
            self.move_left()
        elif current_rect.x < target_rect.x and abs(current_rect.y - target_rect.y) < 3:
            self.move_right()

        if self.rect.colliderect(target_rect):
            self.current_point = target_point

    def teleport_spawn(self):
        location = self.points[self.current_point]
        self.position[0] = location.x
        self.position[1] = location.y
        self.save_location()

    def load_points(self, tmx_data):
        for num in range(1, self.nb_points + 1):
            point = tmx_data.get_object_by_name(f"{self.name}_path{num}")
            rect = pygame.Rect(point.x, point.y, point.width, point.height)
            self.points.append(rect)

