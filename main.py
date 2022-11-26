import pygame
from objects import *

width = 1400
height = 1200
screen = pygame.display.set_mode((width, height))
screen.fill((255, 255, 255))


sprite_up = ['models/sprite_up_1.bmp', 'models/sprite_up_2.bmp', 'models/sprite_up_3.bmp']
sprite_down = ['models/sprite_down_1.bmp', 'models/sprite_down_2.bmp', 'models/sprite_down_3.bmp']
sprite_right = ['models/sprite_right_1.bmp', 'models/sprite_right_2.bmp', 'models/sprite_right_3.bmp']
sprite_left = ['models/sprite_left_1.bmp', 'models/sprite_left_2.bmp', 'models/sprite_left_3.bmp']

map = Map('models/map.bmp')
name = MainCharacter(sprite_up, sprite_down, sprite_left, sprite_right, 700, 600, 4, 4, 3, 0)

pygame.display.update()

while True:
    for i in pygame.event.get():
        map.draw_map(screen, width, height)

        if pygame.key.get_pressed()[pygame.K_w]:
            name.move_up()
        elif pygame.key.get_pressed()[pygame.K_s]:
            name.move_down()
        elif pygame.key.get_pressed()[pygame.K_a]:
            name.move_left()
        elif pygame.key.get_pressed()[pygame.K_d]:
            name.move_right()

        name.draw_character(screen)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
