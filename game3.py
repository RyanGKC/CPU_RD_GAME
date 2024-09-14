import pygame
import random
import time

pygame.init()

pygame.mixer.music.load('CPU_RD_GAME/soundtrack.mp3')  # Replace with your music file path
pygame.mixer.music.set_volume(0.5)  # Set the volume (0.0 to 1.0)
pygame.mixer.music.play(-1)  # Play the music in a loop (-1 for infinite loop)

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
player_speed_x = 5  # Player's horizontal speed
player_left_speed = player_speed_x  # Speed when moving left
player_right_speed = player_speed_x  # Speed when moving right
player = pygame.Rect(player_x, player_y, player_width, player_height)

# Block properties
block_width = 50
block_height = 50
block_speed = 3
block_speeds = []  # List to store individual block speeds for Stage 3

# Hostile block properties
hostile_block_speeds = []  # List to store individual hostile block speeds

# Wall properties
wall_width = 51
wall_height = SCREEN_HEIGHT * 2  # Twice the length of the screen
wall_speed = 5
wall_speeds = []  # List to store individual wall speeds for Stage 3

# Game variables
score = 0
health = 3
blocks = []
hostile_blocks = []
walls = []
scoreboard = []
stage = 1  # Start at stage 1

# Health bar images
heart_image = pygame.image.load('CPU_RD_GAME/health.png')  # Replace with your heart image file path
heart_image = pygame.transform.scale(heart_image, (30, 30))  # Resize the heart image to fit

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
    hostile_block_speeds.append(speed)
    return pygame.Rect(x, 0, block_width, block_height)

def create_wall():
    x = random.randint(0, SCREEN_WIDTH - wall_width)
    speed = wall_speed
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
    
    for i in range(health):
        screen.blit(heart_image, (SCREEN_WIDTH - 150 + i * 40, 10))  # Display hearts based on health
    
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
        "You won't be able to move past even if you overlap.",
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
        "Blocks will now fall at varying speeds.",
        "Hostile blocks have been increased.",
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
    global score, health, blocks, hostile_blocks, walls, block_speed, wall_speed, stage, block_speeds, wall_speeds, hostile_block_speeds, player_left_speed, player_right_speed
    clock = pygame.time.Clock()

    # Reset game state
    score = 0
    health = 3
    blocks = []
    hostile_blocks = []
    walls = []
    block_speeds = []  # Reset block speeds for Stage 3
    wall_speeds = []  # Reset wall speeds for Stage 3
    hostile_block_speeds = []  # Reset hostile block speeds for Stage 3
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

        # Reset player speed for movement checks
        player_left_speed = player_speed_x
        player_right_speed = player_speed_x

        # Check for collisions with walls
        for wall in walls:
            if player.colliderect(wall):
                if player.right > wall.left and player.left < wall.right and player.bottom > wall.top:
                    if player.right <= wall.right:  # Colliding with the left side of the wall
                        player_right_speed = 0
                    if player.left >= wall.left:  # Colliding with the right side of the wall
                        player_left_speed = 0

        # Movement: Only move if not blocked by walls
        if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and player.left > 0:
            player.x -= player_left_speed
        if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and player.right < SCREEN_WIDTH:
            player.x += player_right_speed
        
        # Transition to Stage 2
        if score >= 50 and stage == 1:
            stage = 2
            block_speed = 5  # Increase block speed
            max_walls = 2
            show_stage_two_intro()
            # Remove all remaining blocks and hostile blocks
            blocks.clear()
            hostile_blocks.clear()
        
        # Transition to Stage 3
        if score >= 100 and stage == 2:
            stage = 3
            wall_speed = 2
            max_walls = 4
            show_stage_three_intro()
            # Remove all remaining blocks, hostile blocks, and clear speeds
            blocks.clear()
            hostile_blocks.clear()
            walls.clear()
            block_speeds.clear()
            wall_speeds.clear()
            hostile_block_speeds.clear()  # Clear hostile block speeds

        # Add blocks randomly
        if stage <= 2:
            if random.randint(1, 20) == 1:
                blocks.append(create_block())
        elif stage == 3:
            if random.randint(1, 25) == 1:
                blocks.append(create_block())

        if stage <= 2:
            if random.randint(1, 50) == 1:
                hostile_blocks.append(create_hostile_block())
        elif stage == 3:
            if random.randint(1, 20) == 1:
                hostile_blocks.append(create_hostile_block())
        
        if stage >= 2 and len(walls) < max_walls and random.randint(1, 100) == 1:
            walls.append(create_wall())
        
        # Move blocks down and check for collisions
        for i, block in enumerate(blocks[:]):
            if i < len(block_speeds):
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
            if i < len(hostile_block_speeds):
                speed = hostile_block_speeds[i] if stage == 3 else block_speed
                hostile_block.y += speed
                if hostile_block.colliderect(player):
                    health -= 1
                    hostile_blocks.remove(hostile_block)
                    hostile_block_speeds.pop(i)  # Remove associated speed
                    if health == 0:
                        game_over = True
                elif hostile_block.y > SCREEN_HEIGHT:
                    hostile_blocks.remove(hostile_block)
                    hostile_block_speeds.pop(i)  # Remove associated speed
        
        for i, wall in enumerate(walls[:]):
            if i < len(wall_speeds):
                speed = wall_speeds[i] if stage == 3 else wall_speed
                wall.y += speed

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

