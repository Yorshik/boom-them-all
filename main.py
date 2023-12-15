import os
import sys
from random import randint

import pygame

SIZE = (500, 500)
screen = pygame.display.set_mode(SIZE)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Bomb(pygame.sprite.Sprite):
    bomb = load_image('bomb.png')
    boom = load_image('boom.png')

    def __init__(self, *group, size=(500, 500)):
        super().__init__(*group)
        self.image = self.bomb
        self.rect = self.image.get_rect()
        self.rect.x = randint(0, size[0] - self.rect.w)
        self.rect.y = randint(0, size[1] - self.rect.h)

    def update_image(self, ev: pygame.event.Event):
        if self.image != self.boom and self.rect.x <= ev.pos[0] <= self.rect.x + self.rect.w and self.rect.y <= ev.pos[
            1] <= self.rect.y + self.rect.h:
            self.image = self.boom


class MyGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

    def update_images(self, e):
        for sprite in self.sprites():
            sprite.update_image(e)


running = True
my_group = MyGroup()
for i in range(20):
    Bomb(my_group, size=SIZE)
clock = pygame.time.Clock()
FPS = 60
while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            my_group.update_images(event)
    my_group.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()
