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
player = pygame.Rect(player_x, player_y, player_width, player_height)

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
    pygame.draw.rect(screen, WHITE, player)

    for block in blocks:
        pygame.draw.rect(screen, GREEN, block)

    for hostile_block in hostile_blocks:
        pygame.draw.rect(screen, RED, hostile_block)
    
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    
    health_text = font.render(f"Health: {'♥' * health}", True, RED)
    screen.blit(health_text, (SCREEN_WIDTH - 150, 10))
    
    pygame.display.flip()

def show_intro():
    intro_text = [
        "Welcome to Fall Blocks!",
        "Move left and right to avoid the red blocks.",
        "Collect green blocks to increase your score.",
        "You have 3 hearts. Lose all, and the game is over.",
        "Press any key to start..."
    ]
    
    screen.fill(BLACK)
    y_offset = SCREEN_HEIGHT // 4
    for line in intro_text:
        text = font.render(line, True, WHITE)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, y_offset))
        y_offset += 40
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                waiting = False
                time.sleep(0.2)
                
    pygame.event.clear()

# Function to show the ending screen
def show_ending():
    global scoreboard
    scoreboard.append(score)
    scoreboard = sorted(scoreboard, reverse=True)[:5]
    
    screen.fill(WHITE)
    game_over_text = font.render("Game Over", True, BLACK)
    final_score_text = font.render(f"Final Score: {score}", True, BLACK)
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 4))
    screen.blit(final_score_text, (SCREEN_WIDTH // 2 - final_score_text.get_width() // 2, SCREEN_HEIGHT // 4 + 40))
    
    # Show the scoreboard
    scoreboard_text = font.render("Top Scores", True, BLACK)
    screen.blit(scoreboard_text, (SCREEN_WIDTH // 2 - scoreboard_text.get_width() // 2, SCREEN_HEIGHT // 2))
    y_offset = SCREEN_HEIGHT // 2 + 40
    for i, score in enumerate(scoreboard):
        score_text = font.render(f"{i + 1}. {score}", True, BLACK)
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, y_offset))
        y_offset += 30
    
    # Restart or Quit options
    restart_text = font.render("Press R to Restart or Q to Quit", True, BLACK)
    screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT - 100))
    
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False
                    return True
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
    return False



run = True
while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

pygame.quit()
