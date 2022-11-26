import pygame
from objects import *

width = 1400
height = 1200
clock = pygame.time.Clock()
screen = pygame.display.set_mode((width, height))
screen.fill((255, 255, 255))
finished = False

pygame.init()

font_style = pygame.font.SysFont('cambria', 50)

sprite_up = ['models/sprite_up_1.bmp', 'models/sprite_up_2.bmp', 'models/sprite_up_3.bmp']
sprite_down = ['models/sprite_down_1.bmp', 'models/sprite_down_2.bmp', 'models/sprite_down_3.bmp']
sprite_right = ['models/sprite_right_1.bmp', 'models/sprite_right_2.bmp', 'models/sprite_right_3.bmp']
sprite_left = ['models/sprite_left_1.bmp', 'models/sprite_left_2.bmp', 'models/sprite_left_3.bmp']
locations = ['models/map.bmp', 'models/map2.bmp']

map = Map(locations, 0)
name = MainCharacter(sprite_up, sprite_down, sprite_left, sprite_right, 700, 600, 4, 4, 3, 0, 0)
exit = font_style.render("Exit", True, (0, 0, 0))

while not finished:
    for i in pygame.event.get():
        map.draw_map(screen, width, height)

        if i.type == pygame.MOUSEBUTTONDOWN:
            print(i.pos[0], i.pos[1])
            if 5 <= i.pos[0] <= 205 and 170 <= i.pos[1] <= 220:
                finished = True

        if pygame.key.get_pressed()[pygame.K_w]:
            name.move_up()
        elif pygame.key.get_pressed()[pygame.K_s]:
            name.move_down()
        elif pygame.key.get_pressed()[pygame.K_a]:
            name.move_left()
        elif pygame.key.get_pressed()[pygame.K_d]:
            name.move_right()

        character_position = name.get_position()
        if character_position[0] - 330 >= 1390 and 700 <= character_position[1] - 230 <= 1000 and name.get_location() == 0:
            name.change_location(1)
            map.change_location(1)
            name.go_to_the_door(330, 900)

        print(character_position[0], character_position[1])

        name.draw_character(screen)
        screen.blit(exit, [5, 170])

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True