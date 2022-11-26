import pygame


class Map:
    def __init__(self, pic, location):
        self.pic = pic
        self.location = location

    def draw_map(self, surface, width, height):
        map_surf = pygame.image.load(self.pic[self.location]).convert()
        if self.location == 1:                                                                      # КОСТЫЛЬ
            map_surf = pygame.transform.scale(map_surf, (1400, 1200))
        map_surf.set_colorkey((255, 255, 255))
        map_rect = map_surf.get_rect(center=(width//2, height//2))
        surface.blit(map_surf, map_rect)

    def change_location(self, location):
        self.location = location


class MainCharacter:
    def __init__(self, pic_up, pic_down, pic_left, pic_right, x, y, dx, dy, number, current_number, location):
        self.pic_up = pic_up
        self.pic_down = pic_down
        self.pic_left = pic_left
        self.pic_right = pic_right
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.number = number
        self.current_number = current_number
        self.character_sprite = pygame.image.load(self.pic_down[1]).convert()
        self.location = location

    def draw_character(self, surface):
        character_surf = pygame.transform.scale(self.character_sprite, (800, 400))                       #КОСТЫЛЬ
        character_surf.set_colorkey((255, 255, 255))
        character_rect = character_surf.get_rect(center=(self.x, self.y))
        surface.blit(character_surf, character_rect)

    def move_up(self):
        self.y -= self.dy
        self.current_number += 1
        if self.current_number >= self.number:
            self.current_number = 0
        self.character_sprite = pygame.image.load(self.pic_up[self.current_number]).convert()

    def move_down(self):
        self.y += self.dy
        self.current_number += 1
        if self.current_number >= self.number:
            self.current_number = 0
        self.character_sprite = pygame.image.load(self.pic_down[self.current_number]).convert()

    def move_left(self):
        self.x -= self.dx
        self.current_number += 1
        if self.current_number >= self.number:
            self.current_number = 0
        self.character_sprite = pygame.image.load(self.pic_left[self.current_number]).convert()

    def move_right(self):
        self.x += self.dx
        self.current_number += 1
        if self.current_number >= self.number:
            self.current_number = 0
        self.character_sprite = pygame.image.load(self.pic_right[self.current_number]).convert()

    def change_location(self, location):
        self.location = location

    def get_position(self):
        return self.x, self.y

    def get_location(self):
        return self.location

    def go_to_the_door(self, x_start, y_start):
        self.x = x_start
        self.y = y_start


