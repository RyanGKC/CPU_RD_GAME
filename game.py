import pygame
import random
import time

pygame.init()

# Screen Dimensions
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Fall Blocks")

# Colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

player_width = 50
player_height = 50
player_x = SCREEN_WIDTH // 2 - player_width // 2
player_y = SCREEN_HEIGHT - player_height - 10
player_speed = 5

# Block properties
block_width = 50
block_height = 50
block_speed = 1

# Game variables
score = 0
health = 3
blocks = []
hostile_blocks = []
scoreboard = []

# Fonts
font = pygame.font.Font(None, 36)

def create_block():
    x = random.randint(0, SCREEN_WIDTH - block_width)
    return pygame.Rect(x, 0, block_width, block_height)

def draw_game():
    screen.fill(BLACK)
    pygame.draw.rect(screen, GREEN, block)

run = True
while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

pygame.quit()
