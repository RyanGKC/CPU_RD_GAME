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
ORANGE = (255, 165, 0)

player_width = 50
player_height = 50
player_x = SCREEN_WIDTH // 2 - player_width // 2
player_y = SCREEN_HEIGHT - player_height - 10
player_speed = 5
player = pygame.Rect(player_x, player_y, player_width, player_height)

# Block properties
block_width = 50
block_height = 50
block_speed = 3
block_speeds = []  # List to store individual block speeds for Stage 3

# Wall properties
wall_width = 20
wall_height = SCREEN_HEIGHT * 2  # Twice the length of the screen
wall_speed = 4
wall_speeds = []  # List to store individual wall speeds for Stage 3
max_walls = 2  # Only at most 2 walls can appear at a time

# Game variables
score = 0
health = 3
blocks = []
hostile_blocks = []
walls = []
scoreboard = []
stage = 1  # Start at stage 1

# Fonts
font = pygame.font.Font(None, 36)

def create_block():
    x = random.randint(0, SCREEN_WIDTH - block_width)
    speed = random.randint(3, 8) if stage == 3 else block_speed  # Assign random speed in Stage 3
    block_speeds.append(speed)
    return pygame.Rect(x, 0, block_width, block_height)

def create_hostile_block():
    x = random.randint(0, SCREEN_WIDTH - block_width)
    speed = random.randint(3, 8) if stage == 3 else block_speed  # Assign random speed in Stage 3
    block_speeds.append(speed)
    return pygame.Rect(x, 0, block_width, block_height)

def create_wall():
    x = random.randint(0, SCREEN_WIDTH - wall_width)
    speed = random.randint(3, 8) if stage == 3 else wall_speed  # Assign random speed in Stage 3
    wall_speeds.append(speed)
    return pygame.Rect(x, -wall_height, wall_width, wall_height)

def draw_game():
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, player)

    for block in blocks:
        pygame.draw.rect(screen, GREEN, block)

    for hostile_block in hostile_blocks:
        pygame.draw.rect(screen, RED, hostile_block)
    
    for wall in walls:
        pygame.draw.rect(screen, ORANGE, wall)
    
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

def show_stage_two_intro():
    intro_text = [
        "Stage 2: Increased speed!",
        "Watch out for falling orange walls.",
        "These walls act as temporary borders.",
        "If you're caught below a wall, it's game over!",
        "Good luck!"
    ]
    
    screen.fill(BLACK)
    y_offset = SCREEN_HEIGHT // 4
    for line in intro_text:
        text = font.render(line, True, WHITE)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, y_offset))
        y_offset += 40
    pygame.display.flip()
    
    time.sleep(5)  # 5 second delay before starting stage 2

def show_stage_three_intro():
    intro_text = [
        "Stage 3: Random block and wall speeds!",
        "Blocks and walls will now fall at varying speeds.",
        "Stay sharp and keep collecting those green blocks!",
        "Good luck!"
    ]
    
    screen.fill(BLACK)
    y_offset = SCREEN_HEIGHT // 4
    for line in intro_text:
        text = font.render(line, True, WHITE)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, y_offset))
        y_offset += 40
    pygame.display.flip()
    
    time.sleep(5)  # 5 second delay before starting Stage 3

def show_ending():
    global scoreboard, score
    scoreboard.append(score)
    scoreboard = sorted(scoreboard, reverse=True)[:5]
    
    screen.fill(BLACK)
    game_over_text = font.render("Game Over", True, WHITE)
    final_score_text = font.render(f"Final Score: {score}", True, WHITE)
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 4))
    screen.blit(final_score_text, (SCREEN_WIDTH // 2 - final_score_text.get_width() // 2, SCREEN_HEIGHT // 4 + 40))
    
    # Show the scoreboard
    scoreboard_text = font.render("Top Scores", True, WHITE)
    screen.blit(scoreboard_text, (SCREEN_WIDTH // 2 - scoreboard_text.get_width() // 2, SCREEN_HEIGHT // 2))
    y_offset = SCREEN_HEIGHT // 2 + 40
    for i, score in enumerate(scoreboard):
        score_text = font.render(f"{i + 1}. {score}", True, WHITE)
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, y_offset))
        y_offset += 30
    
    # Restart or Quit options
    restart_text = font.render("Press R to Restart or Q to Quit", True, WHITE)
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

def main_game():
    global score, health, blocks, hostile_blocks, walls, block_speed, wall_speed, stage, block_speeds, wall_speeds
    clock = pygame.time.Clock()

    # Reset game state
    score = 0
    health = 3
    blocks = []
    hostile_blocks = []
    walls = []
    block_speeds = []  # Reset block speeds for Stage 3
    wall_speeds = []  # Reset wall speeds for Stage 3
    stage = 1  # Reset to stage 1
    block_speed = 3
    wall_speed = 4

    game_over = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.left > 0:
            player.x -= player_speed
        if keys[pygame.K_RIGHT] and player.right < SCREEN_WIDTH:
            player.x += player_speed
        
        # Transition to Stage 2
        if score >= 50 and stage == 1:
            stage = 2
            block_speed = 5  # Increase block speed
            wall_speed = 6  # Increase wall speed
            show_stage_two_intro()
            # Remove all remaining blocks and hostile blocks
            blocks.clear()
            hostile_blocks.clear()
        
        # Transition to Stage 3
        if score >= 150 and stage == 2:
            stage = 3
            show_stage_three_intro()
            # Remove all remaining blocks, hostile blocks, and clear speeds
            blocks.clear()
            hostile_blocks.clear()
            walls.clear()
            block_speeds.clear()  
            wall_speeds.clear()  

        # Add blocks randomly
        if random.randint(1, 20) == 1:
            blocks.append(create_block())
        
        if random.randint(1, 50) == 1:
            hostile_blocks.append(create_hostile_block())
        
        if stage >= 2 and len(walls) < max_walls and random.randint(1, 100) == 1:
            walls.append(create_wall())
        
        # Move blocks down and check for collisions
        for i, block in enumerate(blocks[:]):
            speed = block_speeds[i] if stage == 3 else block_speed
            block.y += speed
            if block.colliderect(player):
                score += 1
                blocks.remove(block)
                block_speeds.pop(i)  # Remove associated speed
            elif block.y > SCREEN_HEIGHT:
                blocks.remove(block)
                block_speeds.pop(i)  # Remove associated speed
        
        for i, hostile_block in enumerate(hostile_blocks[:]):
            speed = block_speeds[i] if stage == 3 else block_speed
            hostile_block.y += speed
            if hostile_block.colliderect(player):
                health -= 1
                hostile_blocks.remove(hostile_block)
                block_speeds.pop(i)  # Remove associated speed
                if health == 0:
                    game_over = True
            elif hostile_block.y > SCREEN_HEIGHT:
                hostile_blocks.remove(hostile_block)
                block_speeds.pop(i)  # Remove associated speed
        
        for i, wall in enumerate(walls[:]):
            speed = wall_speeds[i] if stage == 3 else wall_speed
            wall.y += speed

            # Check if player is caught beneath the wall
            if wall.colliderect(player) and player.bottom <= wall.top:
                health = 0  # Instant game over if caught below the wall
                game_over = True

            # Remove walls that move off the screen
            if wall.y > SCREEN_HEIGHT:
                walls.remove(wall)
                wall_speeds.pop(i)  # Remove associated speed
        
        # Draw game elements
        draw_game()
        clock.tick(60)
    
    return game_over

# Main loop
run = True
while run:
    show_intro()
    game_over = main_game()
    if game_over:
        end = show_ending()
        if not end:
            run = False

pygame.quit()


