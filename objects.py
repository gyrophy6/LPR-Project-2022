import pygame
import numpy as np
import random

bullets = []
bones = []


class Map:
    def __init__(self, pic, location, border):
        self.pic = pic
        self.location = location
        self.border = border

    def draw_map(self, surface, width, height, mode):
        if mode == 'map':
            map_surf = pygame.image.load(self.pic[self.location]).convert()
            map_surf.set_colorkey((255, 255, 255))
            map_rect = map_surf.get_rect(center=(width//2, height//2))
            surface.blit(map_surf, map_rect)
        if mode == 'act':
            pygame.draw.rect(surface, (255, 255, 255), (120, 400, 950, 240), 8)
            pygame.draw.rect(surface, (0, 255, 0), (240, 700, 240, 80), 8)
            pygame.draw.rect(surface, (255, 0, 0), (680, 700, 240, 80), 8)

    def change_location(self, location, border):
        self.location = location
        self.border = border

    def check_border(self, x, y):
        return self.border[x // 120][y // 80]


class MainCharacter:
    def __init__(self, pic_up, pic_down, pic_left, pic_right, x, y, location):
        self.pic_up = pic_up
        self.pic_down = pic_down
        self.pic_left = pic_left
        self.pic_right = pic_right
        self.x = x
        self.y = y
        self.dx = 8
        self.dy = 8
        self.number = 3
        self.current_number = 0
        self.character_sprite = pygame.image.load(self.pic_down[1]).convert()
        self.location = location
        self.communication_mode = False
        self.fight_mode = False
        self.passed_exams = 0

    def draw_character(self, surface):
        character_surf = self.character_sprite
        character_surf.set_colorkey((255, 255, 255))
        character_rect = character_surf.get_rect(center=(self.x, self.y))
        surface.blit(character_surf, character_rect)

    def move_up(self, map):
        if map.check_border(self.x, self.y - self.dy) != 0:
            self.y -= self.dy
            self.current_number += 1
            if self.current_number >= self.number:
                self.current_number = 0
            self.character_sprite = pygame.image.load(self.pic_up[self.current_number]).convert()
        else:
            self.y = self.y + self.dy

    def move_down(self, map):
        if map.check_border(self.x, self.y + self.dy) != 0:
            self.y += self.dy
            self.current_number += 1
            if self.current_number >= self.number:
                self.current_number = 0
            self.character_sprite = pygame.image.load(self.pic_down[self.current_number]).convert()
        else:
            self.y = self.y - self.dy

    def move_left(self, map):
        if map.check_border(self.x - self.dx, self.y) != 0:
            self.x -= self.dx
            self.current_number += 1
            if self.current_number >= self.number:
                self.current_number = 0
            self.character_sprite = pygame.image.load(self.pic_left[self.current_number]).convert()
        else:
            self.x = self.x + self.dx

    def move_right(self, map):
        if map.check_border(self.x + self.dx, self.y) != 0:
            self.x += self.dx
            self.current_number += 1
            if self.current_number >= self.number:
                self.current_number = 0
            self.character_sprite = pygame.image.load(self.pic_right[self.current_number]).convert()
        else:
            self.x = self.x - self.dx

    def change_location(self, location):
        self.location = location

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def get_position(self):
        return self.x, self.y

    def get_location(self):
        return self.location

    def go_to_the_door(self, x_start, y_start):
        self.x = x_start
        self.y = y_start

    def small_dist_to_npc(self, npc):
        character_position = self.get_position()
        npc_position = npc.get_position()
        return ((character_position[0] - npc_position[0])**2 +
                (character_position[1] - npc_position[1])**2)**(1/2) < 50

    def set_act_mode(self, mode):
        self.communication_mode = mode

    def get_act_mode(self):
        return self.communication_mode

    def set_fight_mode(self, mode):
        self.fight_mode = mode

    def get_fight_mode(self):
        return self.fight_mode

    def pass_exam(self):
        self.passed_exams += 1

    def show_marks(self):
        return self.passed_exams


class NPC:
    def __init__(self, name, pic, x, y, phrases):
        self.name = name
        self.pic = pic
        self.x = x
        self.y = y
        self.phrases = phrases
        self.number_of_shots_type1 = 0
        self.number_of_shots_type2 = 0
        self.alive = True

    def draw(self, surface, x, y):
        npc_surf = pygame.image.load(self.pic).convert()
        npc_surf.set_colorkey((255, 255, 255))
        npc_rect = npc_surf.get_rect(center=(x, y))
        surface.blit(npc_surf, npc_rect)

    def get_position(self):
        return self.x, self.y

    def fire_type1(self):
        global bullets
        for i in range(-5, 6):
            vx = 3*np.cos(np.pi / 10 * i - np.pi/2)
            vy = 3*np.sin(np.pi / 10 * i - np.pi/2)
            new_bullet = Bullet(5, 600, 300, vx, vy)
            bullets.append(new_bullet)
        self.number_of_shots_type1 += 1

    def fire_type2(self):
        global bones
        new_bone = Bone(10, 130, 1)
        new_bone.set_y_hole(random.randint(440, 580))
        bones.append(new_bone)
        self.number_of_shots_type2 += 1

    def get_number_of_shots_type1(self):
        return self.number_of_shots_type1

    def get_number_of_shots_type2(self):
        return self.number_of_shots_type2

    def kill(self):
        self.alive = False

    def is_alive(self):
        return self.alive

    def is_peaceful(self):
        if self.name == 'Koldunov':
            return True
        return False

    def talk(self):
        return self.name + ': ' + self.phrases[random.randint(0, len(self.phrases) -1)]


class Heart:
    def __init__(self, pic, x, y, dx, dy):
        self.pic = pic
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.hp = 5
        self.r = 7

    def draw_heart(self, surface):
        heart_surf = pygame.image.load(self.pic).convert()
        heart_surf.set_colorkey((255, 255, 255))
        heart_rect = heart_surf.get_rect(center=(self.x, self.y))
        surface.blit(heart_surf, heart_rect)

    def move_up(self):
        if self.y - self.dy >= 408:
            self.y -= self.dy
        else:
            self.y += self.dy

    def move_down(self):
        if self.y + self.dy <= 632:
            self.y += self.dy
        else:
            self.y -= self.dy

    def move_right(self):
        if self.dx + self.dy <= 1062:
            self.x += self.dx
        else:
            self.x -= self.dx

    def move_left(self):
        if self.x - self.dx >= 128:
            self.x -= self.dx
        else:
            self.x += self.dx

    def set_hp(self, damage):
        self.hp += damage

    def get_hp(self):
        return self.hp


class Bullet:
    def __init__(self, r, x, y, vx, vy):
        self.r = r
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

    def move(self):
        self.x += self.vx
        self.y -= self.vy

    def draw(self, surface):
        pygame.draw.circle(surface, (255, 255, 255), (self.x, self.y), self.r)

    def hittest(self, heart):
        if (self.x - heart.x) ** 2 + (self.y - heart.y) ** 2 <= (self.r + heart.r) ** 2:
            return True
        return False


class Bone:
    def __init__(self, a, x, vx):
        self.a = a
        self.b = 240
        self.x = x
        self.vx = vx
        self.y_hole = 0
        self.color = (255, 255, 255)

    def move(self):
        if 120 <= self.x <= 1000:
            self.x += self.vx

    def set_y_hole(self, y):
        self.y_hole = y

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 255, 255), (self.x, 400, self.a, 240))
        pygame.draw.rect(surface, (0, 0, 0), (self.x, self.y_hole, self.a, 40))

    def is_bone_dengerouse(self):
        if self.x >= 1000:
            return True
        else:
            return False

    def hittest(self, heart):
        if -10 <= self.x - heart.x <= 10 and not(-20 - heart.r <= self.y_hole + 20 - heart.y <= 20 + heart.r):
            return True
        return False