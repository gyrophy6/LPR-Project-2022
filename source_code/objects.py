import random
from source_code.constants import *
import numpy as np
import pygame  # Подключение библиотек

bullets = []  # Массив атакующих шаров (пулей)
bones = []  # Массив атакующих прямоугольников (костей)


class Map:
    def __init__(self, location, border):
        ''' Конструктор класса карта

        :param location: номер локации
        :param border: двумерный массив, описывающий границы карты
        '''
        self.pic = ['models/NK.bmp', 'models/corridor.bmp', 'models/classA.bmp', 'models/classB.bmp']
        self.location = location
        self.border = border[location]

    def draw_map(self, surface, width, height, mode):
        '''Функция рисования карты. Если игрок находится в режиме хождения по локациям, рисовать карту,
        если в режиме коммуникации с npc, рисовать интерфейс коммуникации

        :param surface: экран
        :param width: ширина экрана
        :param height: высота экрана
        :param mode: режим хождения по карте/ежим коммуникации
        '''
        if mode == 'map':
            map_surf = pygame.image.load(self.pic[self.location]).convert()
            map_surf.set_colorkey(WHITE)
            map_rect = map_surf.get_rect(center=(width//2, height//2))
            surface.blit(map_surf, map_rect)
        if mode == 'act':
            pygame.draw.rect(surface, WHITE, (120, 400, 950, 240), 8)
            pygame.draw.rect(surface, GREEN, (240, 700, 240, 80), 8)
            pygame.draw.rect(surface, RED, (680, 700, 240, 80), 8)

    def change_location(self, location, border):
        '''Функция, меняющая номер локации и границы, при переходе в другую локацию (из комнаты в комнату)

        :param location: номер локации
        :param border: массив, описывающий границы локации
        '''
        self.location = location
        self.border = border[location]

    def check_border(self, x, y):
        '''Функция, возвращающая 1, если в данную область карты можно наступать, 0, если в данную область карты
        нельзя наступать

        :param x: координата по x
        :param y: координата по y
        '''
        return self.border[x // 120][y // 80]


class MainCharacter:
    def __init__(self, x, y, location):
        '''Конструктор класса главного персонажа

        :param x: координата по x
        :param y: координата по y
        :param location: номер локации, в которой находится персонаж
        '''
        self.pic_up = ['models/sprite_up_1.bmp', 'models/sprite_up_2.bmp', 'models/sprite_up_3.bmp']
        self.pic_down = ['models/sprite_down_1.bmp', 'models/sprite_down_2.bmp', 'models/sprite_down_3.bmp']
        self.pic_left = ['models/sprite_left_1.bmp', 'models/sprite_left_2.bmp', 'models/sprite_left_3.bmp']
        self.pic_right = ['models/sprite_right_1.bmp', 'models/sprite_right_2.bmp', 'models/sprite_right_3.bmp']
        self.x = x
        self.y = y
        self.dx = 6
        self.dy = 6
        self.number = 3
        self.current_number = 0
        self.character_sprite = pygame.image.load(self.pic_down[1]).convert()
        self.location = location
        self.communication_mode = False
        self.fight_mode = False
        self.passed_exams = 0

    def draw_character(self, surface):
        '''Функция отрисовки персонажа

        :param surface: экран
        '''
        character_surf = self.character_sprite
        character_surf.set_colorkey(WHITE)
        character_rect = character_surf.get_rect(center=(self.x, self.y))
        surface.blit(character_surf, character_rect)

    def move_up(self, map):
        '''Функция движения вверх

        :param map: карта
        '''
        if map.check_border(self.x, self.y - self.dy) != 0:
            self.y -= self.dy
            self.current_number += 1
            if self.current_number >= self.number:
                self.current_number = 0
            self.character_sprite = pygame.image.load(self.pic_up[self.current_number]).convert()
        else:
            self.y = self.y + self.dy

    def move_down(self, map):
        '''Функция движения вниз

        :param map: карта
        '''
        if map.check_border(self.x, self.y + self.dy + 35) != 0:                                                        # Здесь так же учтена высота персонажа
            self.y += self.dy                                                                                           # Чтобы он не выходил за край карты нижнюю
            self.current_number += 1                                                                                    # частью ног
            if self.current_number >= self.number:
                self.current_number = 0
            self.character_sprite = pygame.image.load(self.pic_down[self.current_number]).convert()
        else:
            self.y = self.y - self.dy

    def move_left(self, map):
        '''Функция движения влево

        :param map: карта
        '''
        if map.check_border(self.x - self.dx, self.y) != 0:
            self.x -= self.dx
            self.current_number += 1
            if self.current_number >= self.number:
                self.current_number = 0
            self.character_sprite = pygame.image.load(self.pic_left[self.current_number]).convert()
        else:
            self.x = self.x + self.dx

    def move_right(self, map):
        '''Функция движения вправо

        :param map: карта
        '''
        if map.check_border(self.x + self.dx, self.y) != 0:
            self.x += self.dx
            self.current_number += 1
            if self.current_number >= self.number:
                self.current_number = 0
            self.character_sprite = pygame.image.load(self.pic_right[self.current_number]).convert()
        else:
            self.x = self.x - self.dx

    def change_location(self, location):
        '''Функция смены локации

        :param location: номер локации
        '''
        self.location = location

    def set_position(self, x, y):
        ''' Функция присвоения координат

        :param x: координата по x
        :param y: координата по y
        '''
        self.x = x
        self.y = y

    def get_position(self):
        '''Узнать координаты персонажа

        '''
        return self.x, self.y

    def get_location(self):
        '''Узнать номер локации, где находится персонаж

        '''
        return self.location

    def go_to_the_door(self, x_start, y_start):
        ''' Переместить персонажа в начало локации (при смене локации)

        :param x_start: координата по x
        :param y_start: координата по y
        '''
        self.x = x_start
        self.y = y_start

    def small_dist_to_npc(self, npc):
        '''Функция, возвращающая True, если расстояние от персонажа до npc ме //здесь был Гриша// ньше 50 пикселей

        :param npc: npc
        '''
        character_position = self.get_position()
        npc_position = npc.get_position()
        return ((character_position[0] - npc_position[0])**2 +
                (character_position[1] - npc_position[1])**2)**(1/2) < 50

    def set_act_mode(self, mode):
        '''Функция, переводящая персонажа в режим взаимодействия с npc

        :param mode: True - активировать режим коммуникации, False - отключить режим коммуникации
        '''
        self.communication_mode = mode

    def get_act_mode(self):
        '''Функция, возвращающая True, если персонаж в режиме взаимодействия, False, если нет
        '''
        return self.communication_mode

    def set_fight_mode(self, mode):
        '''Функция, переводящая персонажа в режим боя

        :param mode: True - активировать режим боя, False - отключить режим боя
        '''
        self.fight_mode = mode

    def get_fight_mode(self):
        '''Функция, возвращающая True, если персонаж в режиме боя, False, если нет
        '''
        return self.fight_mode

    def pass_exam(self):
        '''Функция, учитывающая сданный экзамен
        '''
        self.passed_exams += 1

    def show_marks(self):
        '''Функция, показывающая, сколько экзаменов сдано

        '''
        return self.passed_exams


class NPC:
    def __init__(self, name, pic, x, y, phrases):
        '''Конструктор класса npc

        :param name: имя npc
        :param pic: модель npc
        :param x: координата по x
        :param y: координата по y
        :param phrases: список фраз, которые может говорить npc
        '''
        self.name = name
        self.pic = pic
        self.x = x
        self.y = y
        self.phrases = phrases
        self.number_of_shots_type1 = 0
        self.number_of_shots_type2 = 0
        self.alive = True

    def draw(self, surface, x, y):
        '''Функция отрисовки npc

        :param surface: экран
        :param x: координата по x
        :param y: координата по y
        '''
        npc_surf = pygame.image.load(self.pic).convert()
        npc_surf.set_colorkey(WHITE)
        npc_rect = npc_surf.get_rect(center=(x, y))
        surface.blit(npc_surf, npc_rect)

    def get_position(self):
        '''Функция, возвращающая координаты npc
        '''
        return self.x, self.y

    def fire_type1(self):
        '''Функция, описывающая выстрелы типа 1 (шары (пули)) разлетаются в разные стороны в диапазоне [-pi; 0]
            Возвращает массив экземпляров класса пули, выпущенные npc
        '''
        global bullets
        for i in range(-5, 6):                                                                                          # Создаётся 10 снарядов, которые разлетаются
            vx = 3*np.cos(np.pi / 10 * i - np.pi/2)                                                                     # в диапазоне [-pi; 0]
            vy = 3*np.sin(np.pi / 10 * i - np.pi/2)
            new_bullet = Bullet(5, 600, 300, vx, vy)
            bullets.append(new_bullet)                                                                                  # Добавление созданных пуль в массив bullets
        self.number_of_shots_type1 += 1                                                                                 # Количество сделанных залпов увеличивается на 1

    def fire_type2(self):
        '''Функция, описывающая выстрелы типа 2 (прямоугольники (кости)), которые перемещаются вдоль оси x.
        Возвращает массив экземпляров класса пули, выпущенные npc
        '''
        global bones
        new_bone = Bone(10, 130, 1)                                                                                     # Создаётся новая кость
        new_bone.set_y_hole(random.randint(440, 580))                                                                   # Рандомно выбирается верхняя y координата дырки
        bones.append(new_bone)                                                                                          # Кость добавляется в массив текущих костей
        self.number_of_shots_type2 += 1                                                                                 # Количество сделанных залпов увеличивается на 1

    def get_number_of_shots_type1(self):
        '''Функция, возвращающая количество залпов типа 1
        '''
        return self.number_of_shots_type1

    def get_number_of_shots_type2(self):
        '''Функция, возвращающая количество залпов типа 2
        '''
        return self.number_of_shots_type2

    def kill(self):
        '''Функция, убивающая npc
        '''
        self.alive = False

    def is_alive(self):
        '''Функция, проверяющая, жив ли npc
        '''
        return self.alive

    def is_peaceful(self):
        '''Функция, проверяющая, настроен npc миролюбиво или нет по отношению к игроку
        '''
        if self.name == 'Koldunov':
            return True
        return False

    def talk(self):
        '''Функция, генерирующая строку вывода на экран. Строка построена по типу "Имя npc: фраза"
        '''
        return self.name + ': ' + self.phrases[random.randint(0, len(self.phrases) - 1)]


class Heart:
    def __init__(self, pic, x, y, dx, dy):
        '''Конструктор класса сердца

        :param pic: модель сердца
        :param x: координата по x
        :param y: координата по y
        :param dx: скорость по x
        :param dy: скорость по y
        '''
        self.pic = pic
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.hp = 5
        self.r = 7

    def draw_heart(self, surface):
        '''Функция отрисовки сердца

        :param surface: экран
        '''
        heart_surf = pygame.image.load(self.pic).convert()
        heart_surf.set_colorkey(WHITE)
        heart_rect = heart_surf.get_rect(center=(self.x, self.y))
        surface.blit(heart_surf, heart_rect)

    def move_up(self):
        '''Функция движения сердца вверх (с ограничением на выход за границу)

        '''
        if self.y - self.dy >= 408:
            self.y -= self.dy
        else:
            self.y += self.dy

    def move_down(self):
        '''Функция движения сердца вниз (с ограничением на выход за границу)

        '''
        if self.y + self.dy <= 632:
            self.y += self.dy
        else:
            self.y -= self.dy

    def move_right(self):
        '''Функция движения сердца вправо (с ограничением на выход за границу)

        '''
        if self.dx + self.dy <= 1062:
            self.x += self.dx
        else:
            self.x -= self.dx

    def move_left(self):
        '''Функция движения сердца влево (с ограничением на выход за границу)

        '''
        if self.x - self.dx >= 128:
            self.x -= self.dx
        else:
            self.x += self.dx

    def set_hp(self, damage):
        '''Функция изменения количества hp

        :param damage: количество урона (лечения), полученное сердцем
        '''
        self.hp += damage

    def get_hp(self):
        '''Функция, показывающее текущее здоровье
        '''
        return self.hp


class Bullet:
    def __init__(self, r, x, y, vx, vy):
        '''Конструктор класса пули

        :param r: радиус пули (шара)
        :param x: координата по x
        :param y: координата по y
        :param vx: скорость по vx
        :param vy: скорость по vy
        '''
        self.r = r
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

    def move(self):
        '''Функция движения пули
        '''
        self.x += self.vx
        self.y -= self.vy

    def draw(self, surface):
        '''Функция отрисовки пули

        :param surface: экран
        '''
        pygame.draw.circle(surface, WHITE, (self.x, self.y), self.r)

    def hittest(self, heart):
        '''Функция, возвращающая True, если пуля столкнулась с сердцем, False, если нет

        :param heart: сердце
        '''
        if (self.x - heart.x) ** 2 + (self.y - heart.y) ** 2 <= (self.r + heart.r) ** 2:
            return True
        return False


class Bone:
    def __init__(self, a, x, vx):
        '''Конструктор класса кости

        :param a: ширина кости
        :param x: координата по x
        :param vx: скорость кости
        '''
        self.a = a
        self.b = 240
        self.x = x
        self.vx = vx
        self.y_hole = 0
        self.color = WHITE

    def move(self):
        '''Функция движения (с проверкой на невыход за границы)
        '''
        if 120 <= self.x <= 1000:
            self.x += self.vx

    def set_y_hole(self, y):
        '''Установить y координату (верхнюю) дырки в кости (прямоугольнике)

        :param y: y координата
        '''
        self.y_hole = y

    def draw(self, surface):
        '''Функция отрисовки прямоугольник (кости)

        :param surface: экран
        '''
        pygame.draw.rect(surface, WHITE, (self.x, 400, self.a, 240))
        pygame.draw.rect(surface, BLACK, (self.x, self.y_hole, self.a, 40))

    def is_bone_dangerous(self):
        '''Проверка, может ли сердце задеть кость. Если кость находится в зоне "боя", функция возвращает True,
        если кость вышла из зоны "боя", False иначе
        '''
        if self.x >= 1000:
            return True
        else:
            return False

    def hittest(self, heart):
        '''Функция проверяет, столкнулось ли сердце с костью (прямоугольником с дыркой)

        :param heart: сердце
        '''
        if -10 <= self.x - heart.x <= 10 and not(-20 + heart.r <= self.y_hole + 20 - heart.y <= 20 - heart.r):
            return True
        return False
