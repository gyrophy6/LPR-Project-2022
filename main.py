import pygame
from objects import *
import numpy as np

width = 1200
height = 800
FPS = 120
clock = pygame.time.Clock()
screen = pygame.display.set_mode((width, height))
screen.fill((255, 255, 255))
finished = False
timer = 0

pygame.init()

font_style = pygame.font.SysFont('cambria', 50)
font_style_small = pygame.font.SysFont('cambria', 25)

sprite_up = ['models/sprite_up_1.bmp', 'models/sprite_up_2.bmp', 'models/sprite_up_3.bmp']
sprite_down = ['models/sprite_down_1.bmp', 'models/sprite_down_2.bmp', 'models/sprite_down_3.bmp']
sprite_right = ['models/sprite_right_1.bmp', 'models/sprite_right_2.bmp', 'models/sprite_right_3.bmp']
sprite_left = ['models/sprite_left_1.bmp', 'models/sprite_left_2.bmp', 'models/sprite_left_3.bmp']

locations = ['models/NK.bmp', 'models/corridor.bmp', 'models/classA.bmp', 'models/classB.bmp']

border1 = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 1, 1, 0, 1, 1, 0, 1, 1, 0],
                    [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                    [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                    [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                    [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                    [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                    [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])

border1 = border1.transpose()

border2 = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 1, 0, 0, 1, 0, 0, 0, 0],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])

border2 = border2.transpose()

border3 = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 1, 0, 1, 0, 1, 0, 0],
                    [0, 0, 0, 1, 0, 1, 0, 1, 0, 0],
                    [0, 0, 1, 1, 1, 1, 1, 1, 0, 0],
                    [0, 0, 0, 1, 0, 1, 0, 1, 0, 0],
                    [0, 0, 0, 1, 0, 1, 0, 1, 0, 0],
                    [0, 0, 1, 1, 1, 1, 1, 1, 0, 0],
                    [0, 0, 0, 1, 0, 1, 0, 1, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0]])

border3 = border3.transpose()

map = Map(locations, 0, border1)
name = MainCharacter(sprite_up, sprite_down, sprite_left, sprite_right, 700, 600, 0)
heart = Heart('models/heart.bmp', 595, 520, 5, 5)
phrases_1 = ['I ain\'t joking. Ever.', 'You agree? Have recognized?', 'Not a season, but Season*',
             'That was just like that']
phrases_2 = ['Take exam ticket']
npc1 = NPC('Koldunov', 'models/Koldunov.bmp', 900, 400, phrases_1)
npc2 = NPC('Nikolaenko', 'models/Nikolaenko.bmp', 880, 370, phrases_2)
npc3 = NPC('Zhdanovskii', 'models/Zhdanovskii.bmp', 880, 370, phrases_2)
exit = font_style.render("Exit", True, (255, 0, 0))
fight = font_style.render("Fight", True, (255, 0, 0))
talk = font_style.render("Talk", True, (0, 255, 0))
start_game_text_1 = font_style_small.render("Oh, my head so hurts. Why i am hear? What time is it?...",
                                            True, (255, 255, 255))
start_game_text_2 = font_style_small.render("Oh no, my exam starts in 10 minutes, i have to hurry",
                                            True, (255, 255, 255))
end_game_text = font_style_small.render("You passed all exams. Congratulations!",
                                            True, (255, 255, 255))
peaceful = font_style.render("It's not worth fighting with LM...", True, (255, 255, 255))
write_message_about_peaceful = False
start_fire_1 = False
start_fire_2 = False
start_game = False
finish_game = False
time_fire = 0
name.set_act_mode(True)

while not finished:
    if name.get_act_mode():
        if not start_game:
            screen.fill((0, 0, 0))
            start_game = True
            screen.blit(start_game_text_1, [320, 400])
            screen.blit(start_game_text_2, [320, 450])
            pygame.display.update()
            pygame.time.wait(5000)
            name.set_act_mode(False)
        if finish_game:
            screen.fill((0, 0, 0))
            screen.blit(end_game_text, [280, 400])
            pygame.display.update()
            pygame.time.wait(3000)
            finished = True
            name.set_act_mode(False)
        screen.fill((0, 0, 0))
        map.draw_map(screen, width, height, 'act')
        hp = font_style_small.render("HP: " + str(heart.get_hp()) + " / 5", True, (255, 0, 0))
        screen.blit(hp, [540, 660])
        screen.blit(fight, [740, 710])
        screen.blit(talk, [300, 710])
        if name.get_location() == 1:
            npc1.draw(screen, 600, 300)
        elif name.get_location() == 2:
            npc2.draw(screen, 600, 300)
        elif name.get_location() == 3:
            npc3.draw(screen, 600, 300)
    else:
        screen.fill((255, 255, 255))
        map.draw_map(screen, width, height, 'map')
        name.draw_character(screen)

    if name.get_fight_mode():
        if name.get_location() == 2:
            heart.draw_heart(screen)
            if npc2.get_number_of_shots_type1() <= 10:
                if not start_fire_1 or (start_fire_1 and timer - time_fire >= 1):
                    npc2.fire_type1()
                    start_fire_1 = True
                    time_fire = timer
            elif npc2.get_number_of_shots_type1() > 10 and timer - time_fire >= 2:
                name.set_fight_mode(False)
                if heart.get_hp() > 0:
                    mark = font_style.render("Nikolaenko: Your mark is " + str(heart.get_hp()*2) + '/10', True, (255, 255, 255))
                    name.pass_exam()
                    if name.show_marks() == 2:
                        finish_game = True
                        name.set_act_mode(True)
                else:
                    mark = font_style.render('Nikolaenko: You lost. Retake in January', True, (255, 255, 255))
                    finished = True
                name.set_fight_mode(False)
                name.set_position(850, 400)
                screen.blit(mark, [140, 400])
                screen.blit(exit, [5, 10])
                pygame.display.update()
                pygame.time.wait(1000)
                npc2.kill()
                heart.set_hp(5 - heart.get_hp())
                name.set_act_mode(False)

        if name.get_location() == 3:
            heart.draw_heart(screen)
            if npc3.get_number_of_shots_type2() <= 5:
                if not start_fire_2 or (start_fire_2 and timer - time_fire >= 4):
                    npc3.fire_type2()
                    start_fire_2 = True
                    time_fire = timer
            elif npc3.get_number_of_shots_type2() > 5 and timer - time_fire >= 8:
                name.set_fight_mode(False)
                if heart.get_hp() > 0:
                    mark = font_style.render("Zhdanovskii: Your mark is " + str(heart.get_hp()*2) + '/10',
                                             True, (255, 255, 255))
                    name.pass_exam()
                    if name.show_marks() == 2:
                        finish_game = True
                        name.set_act_mode(True)
                else:
                    mark = font_style.render('Zhdanovskii: You lost. Retake in January', True, (255, 255, 255))
                    finished = True
                name.set_fight_mode(False)
                name.set_position(850, 400)
                screen.blit(mark, [140, 400])
                screen.blit(exit, [5, 10])
                pygame.display.update()
                pygame.time.wait(1000)
                npc3.kill()
                heart.set_hp(5 - heart.get_hp())
                name.set_act_mode(False)

    clock.tick(FPS)
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
             finished = True

        if i.type == pygame.MOUSEBUTTONDOWN:
            if 5 <= i.pos[0] <= 205 and 0 <= i.pos[1] <= 70:
                finished = True

        if pygame.key.get_pressed()[pygame.K_w] and not name.get_act_mode():
            name.move_up(map)
        elif pygame.key.get_pressed()[pygame.K_s] and not name.get_act_mode():
            name.move_down(map)
        elif pygame.key.get_pressed()[pygame.K_a] and not name.get_act_mode():
            name.move_left(map)
        elif pygame.key.get_pressed()[pygame.K_d] and not name.get_act_mode():
            name.move_right(map)
        elif name.get_location() == 1 and name.small_dist_to_npc(npc1) and npc1.is_alive():
            name.set_act_mode(True)
            if i.type == pygame.MOUSEBUTTONDOWN:
                if 680 <= i.pos[0] <= 920 and 680 <= i.pos[1] <= 760 and not npc1.is_peaceful():
                    name.set_fight_mode(True)
                elif 680 <= i.pos[0] <= 920 and 680 <= i.pos[1] <= 760 and npc1.is_peaceful():
                    screen.blit(peaceful, [140, 400])
                    screen.blit(exit, [5, 10])
                    pygame.display.update()
                    pygame.time.wait(2000)
                    name.set_act_mode(False)
                    name.set_position(850, 400)
                elif 240 <= i.pos[0] <= 480 and 680 <= i.pos[1] <= 760:
                    phrase = font_style.render(npc1.talk(), True, (255, 255, 255))
                    screen.blit(phrase, [140, 400])
                    screen.blit(exit, [5, 10])
                    pygame.display.update()
                    pygame.time.wait(2000)
                    name.set_act_mode(False)
                    name.set_position(850, 400)

        if name.get_location() == 2 and name.small_dist_to_npc(npc2) and npc2.is_alive():
            name.set_act_mode(True)
            if i.type == pygame.MOUSEBUTTONDOWN:
                if 680 <= i.pos[0] <= 920 and 680 <= i.pos[1] <= 760 and not npc2.is_peaceful():
                    name.set_fight_mode(True)
                elif 240 <= i.pos[0] <= 480 and 680 <= i.pos[1] <= 760 and not name.get_fight_mode():
                    phrase = font_style.render(npc2.talk(), True, (255, 255, 255))
                    screen.blit(phrase, [140, 400])
                    screen.blit(exit, [5, 10])
                    pygame.display.update()
                    pygame.time.wait(2000)
                    name.set_act_mode(False)
                    name.set_position(850, 440)

        if name.get_location() == 3 and name.small_dist_to_npc(npc3) and npc3.is_alive():
            name.set_act_mode(True)
            if i.type == pygame.MOUSEBUTTONDOWN:
                if 680 <= i.pos[0] <= 920 and 680 <= i.pos[1] <= 760 and not npc3.is_peaceful():
                    name.set_fight_mode(True)
                elif 240 <= i.pos[0] <= 480 and 680 <= i.pos[1] <= 760 and not name.get_fight_mode():
                    phrase = font_style.render(npc3.talk(), True, (255, 255, 255))
                    screen.blit(phrase, [140, 400])
                    screen.blit(exit, [5, 10])
                    pygame.display.update()
                    pygame.time.wait(2000)
                    name.set_act_mode(False)
                    name.set_position(850, 440)

        if name.get_fight_mode():
            if pygame.key.get_pressed()[pygame.K_w]:
                heart.move_up()
            elif pygame.key.get_pressed()[pygame.K_s]:
                heart.move_down()
            elif pygame.key.get_pressed()[pygame.K_a]:
                heart.move_left()
            elif pygame.key.get_pressed()[pygame.K_d]:
                heart.move_right()

    for bullet in bullets:
        bullet.draw(screen)
        bullet.move()
        if bullet.hittest(heart):
            heart.set_hp(-1)
            bullets.remove(bullet)

    for bone in bones:
        bone.draw(screen)
        bone.move()
        if bone.hittest(heart):
            heart.set_hp(-1)
            bones.remove(bone)
        if bone.is_bone_dengerouse():
            bones.remove(bone)

    character_position = name.get_position()
    if 480 <= character_position[0] <= 720 and 160 <= character_position[1] <= 240 and name.get_location() == 0:
        name.change_location(1)
        map.change_location(1, border2)
        name.go_to_the_door(30, 400)
    elif character_position[0] <= 20 and 320 <= character_position[1] <= 560 and name.get_location() == 1:
        name.change_location(0)
        map.change_location(0, border1)
        name.go_to_the_door(600, 280)
    elif 240 <= character_position[0] <= 360 and character_position[1] <= 320 and name.get_location() == 1:
        name.change_location(2)
        map.change_location(2, border3)
        name.go_to_the_door(900, 700)
    elif 600 <= character_position[0] <= 730 and character_position[1] <= 320 and name.get_location() == 1:
        name.change_location(3)
        map.change_location(3, border3)
        name.go_to_the_door(900, 700)
    elif 840 <= character_position[0] <= 960 and 720 <= character_position[1] and name.get_location() == 2:
        name.change_location(1)
        map.change_location(1, border2)
        name.go_to_the_door(300, 380)
    elif 840 <= character_position[0] <= 960 and 720 <= character_position[1] and name.get_location() == 3:
        name.change_location(1)
        map.change_location(1, border2)
        name.go_to_the_door(665, 380)
    if name.get_location() == 1 and not name.get_act_mode() and npc1.is_alive():
        npc_position = npc1.get_position()
        npc1.draw(screen, npc_position[0], npc_position[1])
    if name.get_location() == 2 and not name.get_act_mode() and npc2.is_alive():
        npc_position = npc2.get_position()
        npc2.draw(screen, npc_position[0], npc_position[1])
    if name.get_location() == 3 and not name.get_act_mode() and npc3.is_alive():
        npc_position = npc3.get_position()
        npc3.draw(screen, npc_position[0], npc_position[1])

    timer += 1/120
    screen.blit(exit, [5, 10])
    pygame.display.update()