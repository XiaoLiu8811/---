import pygame
import sys
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Set up the window
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Snake Game')

# Game states
MENU = 'menu'
PLAYING = 'playing'
GAME_OVER = 'game_over'

class Game:
    def __init__(self):
        self.state = MENU
        self.clock = pygame.time.Clock()
        
    def run(self):
        while True:
            if self.state == MENU:
                self.show_menu()
            elif self.state == PLAYING:
                self.play_game()
            elif self.state == GAME_OVER:
                self.show_game_over()
            
            pygame.display.update()
            self.clock.tick(60)
    
    def show_menu(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            
        window.fill(BLACK)
        # TODO: Add menu implementation
    
    def play_game(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            
        window.fill(BLACK)
        # TODO: Add game implementation
    
    def show_game_over(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            
        window.fill(BLACK)
        # TODO: Add game over screen implementation

if __name__ == '__main__':
    game = Game()
    game.run()