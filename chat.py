import pygame
import random
import time
import os

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Falling Blocks Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Player properties
player_width = 50
player_height = 50
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - player_height - 10
player_speed = 5
player = pygame.Rect(player_x, player_y, player_width, player_height)

# Block properties
block_width = 50
block_height = 50
block_speed = 5

# Game variables
score = 0
health = 3
blocks = []
hostile_blocks = []
scoreboard = []

# Fonts
font = pygame.font.Font(None, 36)

# Function to create a new block
def create_block():
    x = random.randint(0, WIDTH - block_width)
    return pygame.Rect(x, 0, block_width, block_height)

# Function to draw the player, blocks, score, and health
def draw_game():
    screen.fill(WHITE)
    pygame.draw.rect(screen, BLACK, player)
    
    for block in blocks:
        pygame.draw.rect(screen, GREEN, block)
    
    for hostile_block in hostile_blocks:
        pygame.draw.rect(screen, RED, hostile_block)
    
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))
    
    health_text = font.render(f"Health: {'♥' * health}", True, RED)
    screen.blit(health_text, (WIDTH - 150, 10))
    
    pygame.display.flip()

# Function to show the introduction screen
def show_intro():
    intro_text = [
        "Welcome to Fall Blocks!",
        "Move left and right to avoid the red blocks.",
        "Collect green blocks to increase your score.",
        "You have 3 hearts. Lose all, and the game is over.",
        "Press any key to start..."
    ]
    
    screen.fill(BLACK)
    y_offset = HEIGHT // 4
    for line in intro_text:
        text = font.render(line, True, WHITE)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, y_offset))
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

# Function to show the ending screen
def show_ending():
    global scoreboard
    scoreboard.append(score)
    scoreboard = sorted(scoreboard, reverse=True)[:5]
    
    screen.fill(WHITE)
    game_over_text = font.render("Game Over", True, BLACK)
    final_score_text = font.render(f"Final Score: {score}", True, BLACK)
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 4))
    screen.blit(final_score_text, (WIDTH // 2 - final_score_text.get_width() // 2, HEIGHT // 4 + 40))
    
    # Show the scoreboard
    scoreboard_text = font.render("Top Scores", True, BLACK)
    screen.blit(scoreboard_text, (WIDTH // 2 - scoreboard_text.get_width() // 2, HEIGHT // 2))
    y_offset = HEIGHT // 2 + 40
    for i, score in enumerate(scoreboard):
        score_text = font.render(f"{i + 1}. {score}", True, BLACK)
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, y_offset))
        y_offset += 30
    
    # Restart or Quit options
    restart_text = font.render("Press R to Restart or Q to Quit", True, BLACK)
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT - 100))
    
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

# Main game loop
def main_game():
    global score, health, blocks, hostile_blocks
    clock = pygame.time.Clock()
    score = 0
    health = 3
    blocks = []
    hostile_blocks = []
    game_over = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.left > 0:
            player.x -= player_speed
        if keys[pygame.K_RIGHT] and player.right < WIDTH:
            player.x += player_speed
        
        # Add blocks randomly
        if random.randint(1, 20) == 1:
            blocks.append(create_block())
        
        if random.randint(1, 50) == 1:
            hostile_blocks.append(create_block())
        
        # Move blocks down and check for collisions
        for block in blocks[:]:
            block.y += block_speed
            if block.colliderect(player):
                score += 1
                blocks.remove(block)
            elif block.y > HEIGHT:
                score -= 1
                blocks.remove(block)
        
        for hostile_block in hostile_blocks[:]:
            hostile_block.y += block_speed
            if hostile_block.colliderect(player):
                health -= 1
                hostile_blocks.remove(hostile_block)
                if health == 0:
                    game_over = True
            elif hostile_block.y > HEIGHT:
                hostile_blocks.remove(hostile_block)
        
        draw_game()
        clock.tick(60)
    
    return game_over

# Main loop
while True:
    show_intro()
    game_over = main_game()
    if game_over:
        if not show_ending():
            break

pygame.quit()