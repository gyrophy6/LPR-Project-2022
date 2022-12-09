from source_code.objects import *  # Подключение модулей
from source_code.constants import *

finished = False  # Создание основных переменных для работы игры
clock = pygame.time.Clock()
screen = pygame.display.set_mode((width, height))
screen.fill(WHITE)
timer = 0

pygame.init()  # Запуск игры

font_style = pygame.font.SysFont('cambria', 50)  # Установка стилей текста
font_style_small = pygame.font.SysFont('cambria', 25)

exit = font_style.render("Exit", True, RED)
fight = font_style.render("Fight", True, RED)  # Создание сообщений, которые будут выводиться на экран
talk = font_style.render("Talk", True, GREEN)
start_game_text_1 = font_style_small.render("Oh, my head so hurts. Why i am hear? What time is it?...",
                                            True, WHITE)
start_game_text_2 = font_style_small.render("Oh no, my exam starts in 10 minutes, i have to hurry",
                                            True, WHITE)
end_game_text = font_style_small.render("You passed all exams. Congratulations!", True, WHITE)
peaceful = font_style.render("It's not worth fighting with LM...", True, WHITE)

map = Map(0, border)  # Создание карты
name = MainCharacter(700, 600, 0)  # Создание главного героя
heart = Heart('models/heart.bmp', 595, 520, 5, 5)  # Создание сердца
npc1 = NPC('Koldunov', 'models/Koldunov.bmp', 900, 400, phrases_1)  # Создание npc1 (КЛМ)
npc2 = NPC('Nikolaenko', 'models/Nikolaenko.bmp', 880, 370, phrases_2)  # Создание npc2 (Николаенко)
npc3 = NPC('Zhdanovskii', 'models/Zhdanovskii.bmp', 880, 370, phrases_2)  # Создание npc3 (Ждановский)

write_message_about_peaceful = False  # Создание флаговых переменных
start_fire_1 = False
start_fire_2 = False
start_game = False
finish_game = False
time_fire = 0

name.set_act_mode(True)  # Установить режим коммуникации

while not finished:  # Пока игра не закончилась
    if name.get_act_mode():  # Если активирован режим взаимодействия
        if not start_game:  # Если игра только начинается
            screen.fill(BLACK)  # Нарисовать вступление
            start_game = True
            screen.blit(start_game_text_1, [320, 350])
            screen.blit(start_game_text_2, [320, 400])
            pygame.display.update()
            pygame.time.wait(5000)
            name.set_act_mode(False)
        if finish_game:  # Если игра заканчивается
            screen.fill(BLACK)  # Нарисовать завершение игры
            screen.blit(end_game_text, [280, 350])
            pygame.display.update()
            pygame.time.wait(3000)
            finished = True
            name.set_act_mode(False)
        screen.fill(BLACK)  # Рисовать интерфейс взаимодействия
        map.draw_map(screen, width, height, 'act')
        hp = font_style_small.render("HP: " + str(heart.get_hp()) + " / 5", True, RED)
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
        screen.fill(WHITE)
        map.draw_map(screen, width, height, 'map')
        name.draw_character(screen)

    if name.get_fight_mode():  # Если персонаж в режиме боя
        if name.get_location() == 2:  # Если персонаж дерётся в локации 2
            heart.draw_heart(screen)  # Отрисовать сердце
            if npc2.get_number_of_shots_type1() <= 10:  # Если npc2 ещё не сделал 10 залпов
                if not start_fire_1 or (
                        start_fire_1 and timer - time_fire >= 1):  # Если огонь ещё не открыт или между залпами прошла секунда
                    npc2.fire_type1()  # Дать залп типа 1
                    start_fire_1 = True  # Записать в переменную, что открыт огонь
                    time_fire = timer  # Записать время залпа
            elif npc2.get_number_of_shots_type1() > 10 and timer - time_fire >= 2:  # Если сделано больше 10 залпов и с момента последнего прошло больше 2 секунд
                name.set_fight_mode(False)  # Выйти из режима боя
                if heart.get_hp() > 0:  # Если hp > 0
                    mark = font_style.render("Nikolaenko: Your mark is " + str(heart.get_hp() * 2) + '/10', True,
                                             # Сгенерировать сообщение об оценке
                                             WHITE)
                    name.pass_exam()  # Зачитать сданный экзамен
                    if name.show_marks() == 2:  # Если сдано 2 экзамена
                        finish_game = True  # Закончить игру
                        name.set_act_mode(True)  # Перейти к завершающему "слайду"
                else:  # Иначе (если hp < 0)
                    mark = font_style.render('Nikolaenko: You lost. Retake in January', True,
                                             WHITE)  # Сгенерировать сообщение о пересдаче
                    finished = True  # Закончить игру
                pygame.draw.rect(screen, BLACK,
                                 (124, 404, 940, 230))  # Залить разговорное окно чёрным (убрать сердце)
                screen.blit(mark, [140, 400])  # Вывести сообщение о результате
                screen.blit(exit, [5, 10])  # Отрисовать кнопку выхода из игры
                pygame.display.update()  # Обновить экран
                pygame.time.wait(1000)  # Подождать (пока играющий прочтёт сообщение)
                npc2.kill()  # Убить npc
                heart.set_hp(5 - heart.get_hp())  # Восстановить hp до фулла
                name.set_position(850, 400)  # Переместить персонажа вне зону взаимодействия с npc
                name.set_act_mode(False)  # Выйти из режима взаимодействия

        if name.get_location() == 3:  # Если бой в локации номер 3
            heart.draw_heart(screen)  # Код ниже аналогично коду, описывающему бой в локации 2
            if npc3.get_number_of_shots_type2() <= 5:  # изменены тайминги взаимодействия
                if not start_fire_2 or (start_fire_2 and timer - time_fire >= 4):
                    npc3.fire_type2()
                    start_fire_2 = True
                    time_fire = timer
            elif npc3.get_number_of_shots_type2() > 5 and timer - time_fire >= 8:
                name.set_fight_mode(False)
                if heart.get_hp() > 0:
                    mark = font_style.render("Zhdanovskii: Your mark is " + str(heart.get_hp() * 2) + '/10',
                                             True, WHITE)
                    name.pass_exam()
                    if name.show_marks() == 2:
                        finish_game = True
                        name.set_act_mode(True)
                else:
                    mark = font_style.render('Zhdanovskii: You lost. Retake in January', True, WHITE)
                    finished = True
                pygame.draw.rect(screen, BLACK, (124, 404, 940, 230))
                screen.blit(mark, [140, 400])
                screen.blit(exit, [5, 10])
                pygame.display.update()
                pygame.time.wait(1000)
                npc3.kill()
                heart.set_hp(5 - heart.get_hp())
                name.set_position(850, 400)
                name.set_act_mode(False)

    clock.tick(FPS)
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            finished = True

        if i.type == pygame.MOUSEBUTTONDOWN:
            if 5 <= i.pos[0] <= 205 and 0 <= i.pos[1] <= 70:  # Если нажата кнопка выход
                finished = True  # Закончить игру

        if pygame.key.get_pressed()[
            pygame.K_w] and not name.get_act_mode():  # Движение персонажа, если он не в режиме взаимодействия
            name.move_up(map)
        elif pygame.key.get_pressed()[pygame.K_s] and not name.get_act_mode():
            name.move_down(map)
        elif pygame.key.get_pressed()[pygame.K_a] and not name.get_act_mode():
            name.move_left(map)
        elif pygame.key.get_pressed()[pygame.K_d] and not name.get_act_mode():
            name.move_right(map)

        elif name.get_location() == 1 and name.small_dist_to_npc(
                npc1) and npc1.is_alive():  # Если герой в локации 1, близко к npc и npc жив
            name.set_act_mode(True)  # Активировать режим взаимодействия
            if i.type == pygame.MOUSEBUTTONDOWN:
                if 680 <= i.pos[0] <= 920 and 680 <= i.pos[
                    1] <= 760 and not npc1.is_peaceful():  # Если нажата кнопка "бой" и npc не настроен миролюбиво
                    name.set_fight_mode(True)  # Активировать режим боя
                elif 680 <= i.pos[0] <= 920 and 680 <= i.pos[
                    1] <= 760 and npc1.is_peaceful():  # Если нажата кнопка "бой" и npc настроен миролюбиво
                    screen.blit(peaceful, [140, 400])  # Вывести сообщение о миролюбивости
                elif 240 <= i.pos[0] <= 480 and 680 <= i.pos[1] <= 760:  # Если нажата кнопка "поговорить"
                    phrase = font_style.render(npc1.talk(), True, WHITE)  # Вывести случайную реплику npc
                    screen.blit(phrase, [140, 400])
                screen.blit(exit, [5, 10])  # Вывести кнопку выхода из игры
                pygame.display.update()  # Обновить экран
                pygame.time.wait(2000)  # Подождать (пока игрок прочитает сообщение)
                name.set_act_mode(False)  # Выключить режим взаимодействия
                name.set_position(850, 400)  # Переместить персонажа на расстояние не взаимодействия от npc

        if name.get_location() == 2 and name.small_dist_to_npc(npc2) and npc2.is_alive():  # Аналогично для локации 2
            name.set_act_mode(True)
            if i.type == pygame.MOUSEBUTTONDOWN:
                if 680 <= i.pos[0] <= 920 and 680 <= i.pos[1] <= 760 and not npc2.is_peaceful():
                    name.set_fight_mode(True)
                elif 240 <= i.pos[0] <= 480 and 680 <= i.pos[
                    1] <= 760 and not name.get_fight_mode():  # Поговорить можно только когда не активирован режим боя
                    phrase = font_style.render(npc2.talk(), True, WHITE)
                    screen.blit(phrase, [140, 400])
                    screen.blit(exit, [5, 10])
                    pygame.display.update()
                    pygame.time.wait(2000)
                    name.set_act_mode(False)
                    name.set_position(850, 440)

        if name.get_location() == 3 and name.small_dist_to_npc(npc3) and npc3.is_alive():  # Аналогично для локации 3
            name.set_act_mode(True)
            if i.type == pygame.MOUSEBUTTONDOWN:
                if 680 <= i.pos[0] <= 920 and 680 <= i.pos[1] <= 760 and not npc3.is_peaceful():
                    name.set_fight_mode(True)
                elif 240 <= i.pos[0] <= 480 and 680 <= i.pos[1] <= 760 and not name.get_fight_mode():
                    phrase = font_style.render(npc3.talk(), True, WHITE)
                    screen.blit(phrase, [140, 400])
                    screen.blit(exit, [5, 10])
                    pygame.display.update()
                    pygame.time.wait(2000)
                    name.set_act_mode(False)
                    name.set_position(850, 440)

        if name.get_fight_mode():  # Если режим боя активирован
            if pygame.key.get_pressed()[pygame.K_w]:  # Движение сердца
                heart.move_up()
            elif pygame.key.get_pressed()[pygame.K_s]:
                heart.move_down()
            elif pygame.key.get_pressed()[pygame.K_a]:
                heart.move_left()
            elif pygame.key.get_pressed()[pygame.K_d]:
                heart.move_right()

    for bullet in bullets:  # Отрисовать все пули (шарики)
        bullet.draw(screen)
        bullet.move()
        if bullet.hittest(heart):  # При столкновении удалить пулю из списка
            heart.set_hp(-1)
            bullets.remove(bullet)

    for bone in bones:  # Отрисовать все кости аналогично
        bone.draw(screen)
        heart.draw_heart(screen)
        bone.move()
        if bone.hittest(heart):
            heart.set_hp(-1)
            bones.remove(bone)
        if bone.is_bone_dangerous():
            bones.remove(bone)

    character_position = name.get_position()  # Перемещение между локациями
    if 480 <= character_position[0] <= 720 and 160 <= character_position[1] <= 240 and name.get_location() == 0:
        name.change_location(1)
        map.change_location(1, border)
        name.go_to_the_door(30, 400)
    elif character_position[0] <= 20 and 320 <= character_position[1] <= 560 and name.get_location() == 1:
        name.change_location(0)
        map.change_location(0, border)
        name.go_to_the_door(600, 280)
    elif 240 <= character_position[0] <= 360 and character_position[1] <= 320 and name.get_location() == 1:
        name.change_location(2)
        map.change_location(2, border)
        name.go_to_the_door(900, 700)
    elif 600 <= character_position[0] <= 730 and character_position[1] <= 320 and name.get_location() == 1:
        name.change_location(3)
        map.change_location(3, border)
        name.go_to_the_door(900, 700)
    elif 840 <= character_position[0] <= 960 and 720 <= character_position[1] and name.get_location() == 2:
        name.change_location(1)
        map.change_location(1, border)
        name.go_to_the_door(300, 380)
    elif 840 <= character_position[0] <= 960 and 720 <= character_position[1] and name.get_location() == 3:
        name.change_location(1)
        map.change_location(1, border)
        name.go_to_the_door(665, 380)

    if name.get_location() == 1 and not name.get_act_mode() and npc1.is_alive():  # Если режим взаимодействия не активирован и npc жив
        npc_position = npc1.get_position()  # Отрисовать npc
        npc1.draw(screen, npc_position[0], npc_position[1])
    if name.get_location() == 2 and not name.get_act_mode() and npc2.is_alive():
        npc_position = npc2.get_position()
        npc2.draw(screen, npc_position[0], npc_position[1])
    if name.get_location() == 3 and not name.get_act_mode() and npc3.is_alive():
        npc_position = npc3.get_position()
        npc3.draw(screen, npc_position[0], npc_position[1])

    timer += 1 / 120  # Обновить таймер
    screen.blit(exit, [5, 10])  # Нарисовать кнопку выход из игры
    pygame.display.update()  # Обновить экран


