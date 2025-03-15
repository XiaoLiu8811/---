import pygame
from pygame.math import Vector2
from random import randint

class Snake:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(1, 0)
        self.new_block = False
        
        # Load and scale snake head and body images
        self.head_up = pygame.Surface((20, 20))
        self.head_up.fill((0, 255, 0))
        self.head_down = pygame.transform.rotate(self.head_up, 180)
        self.head_right = pygame.transform.rotate(self.head_up, -90)
        self.head_left = pygame.transform.rotate(self.head_up, 90)
        
        self.body_surface = pygame.Surface((20, 20))
        self.body_surface.fill((0, 200, 0))
    
    def draw(self, window):
        # Draw head
        head_rect = pygame.Rect(self.body[0].x * 20, self.body[0].y * 20, 20, 20)
        
        # Determine head direction
        if self.direction == Vector2(0, -1):  # Up
            window.blit(self.head_up, head_rect)
        elif self.direction == Vector2(0, 1):  # Down
            window.blit(self.head_down, head_rect)
        elif self.direction == Vector2(1, 0):  # Right
            window.blit(self.head_right, head_rect)
        else:  # Left
            window.blit(self.head_left, head_rect)
        
        # Draw body
        for segment in self.body[1:]:
            segment_rect = pygame.Rect(segment.x * 20, segment.y * 20, 20, 20)
            window.blit(self.body_surface, segment_rect)
    
    def move(self):
        if self.new_block:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy
    
    def grow(self):
        self.new_block = True
    
    def reset(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(1, 0)
    
    def check_collision(self, grid_width, grid_height):
        # Check wall collision
        if not 0 <= self.body[0].x < grid_width or not 0 <= self.body[0].y < grid_height:
            return True
        
        # Check self collision
        for segment in self.body[1:]:
            if segment == self.body[0]:
                return True
        
        return False

class Food:
    def __init__(self, grid_width, grid_height):
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.position = self.randomize_position()
        self.surface = pygame.Surface((20, 20))
        self.surface.fill((255, 0, 0))
    
    def draw(self, window):
        food_rect = pygame.Rect(self.position.x * 20, self.position.y * 20, 20, 20)
        window.blit(self.surface, food_rect)
    
    def randomize_position(self):
        return Vector2(randint(0, self.grid_width - 1), randint(0, self.grid_height - 1))