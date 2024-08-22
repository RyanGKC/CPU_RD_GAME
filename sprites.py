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

# Load images
player_image = pygame.image.load("player.png")
player_image = pygame.transform.scale(player_image, (50, 50))  # Scale to desired size
block_image = pygame.image.load("block.png")
block_image = pygame.transform.scale(block_image, (50, 50))  # Scale to desired size
hostile_block_image = pygame.image.load("hostile_block.png")
hostile_block_image = pygame.transform.scale(hostile_block_image, (50, 50))  # Scale to desired size
wall_image = pygame.image.load("wall.png")
wall_image = pygame.transform.scale(wall_image, (20, SCREEN_HEIGHT * 2))  # Scale to desired size

# Player sprite class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 10
        self.speed = 5
    
    def update(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)

# Block sprite class
class Block(pygame.sprite.Sprite):
    def __init__(self, color, speed):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - 50)
        self.rect.y = 0
        self.speed = speed
    
    def update(self):
        self.rect.y += self.speed
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)

# Wall sprite class
class Wall(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = wall_image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - 20)
        self.rect.y = -self.rect.height
        self.speed = random.randint(3, 8)
    
    def update(self):
        self.rect.y += self.speed
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)

# Game variables
score = 0
health = 3
blocks = pygame.sprite.Group()
hostile_blocks = pygame.sprite.Group()
walls = pygame.sprite.Group()
scoreboard = []
stage = 1

# Fonts
font = pygame.font.Font(None, 36)

def create_block():
    speed = random.randint(3, 8)
    return Block(GREEN, speed)

def create_hostile_block():
    speed = random.randint(3, 8)
    return Block(RED, speed)

def create_wall():
    return Wall()

def draw_game():
    screen.fill(BLACK)
    
    # Draw all sprites
    player.draw(screen)
    blocks.draw(screen)
    hostile_blocks.draw(screen)
    walls.draw(screen)
    
    # Draw the score and health
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
        "Stage 3: Random speed blocks!",
        "Blocks and walls will now fall at random speeds.",
        "Stay alert and keep moving!",
        "Good luck!"
    ]
    
    screen.fill(BLACK)
    y_offset = SCREEN_HEIGHT // 4
    for line in intro_text:
        text = font.render(line, True, WHITE)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, y_offset))
        y_offset += 40
    pygame.display.flip()
    
    time.sleep(5)  # 5 second delay before starting stage 3

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
    global score, health, blocks, hostile_blocks, walls, block_speed, wall_speed, stage
    clock = pygame.time.Clock()

    # Reset game state
    score = 0
    health = 3
    blocks.empty()
    hostile_blocks.empty()
    walls.empty()
    stage = 1
    block_speed = 3
    wall_speed = 4

    player.rect.centerx = SCREEN_WIDTH // 2
    player.rect.bottom = SCREEN_HEIGHT - 10

    game_over = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        keys = pygame.key.get_pressed()

        # Update the player
        player.update(keys)
        
        # Transition to Stage 2
        if score >= 50 and stage == 1:
            stage = 2
            block_speed = 5
            wall_speed = 6
            show_stage_two_intro()
            blocks.empty()
            hostile_blocks.empty()
        
        # Transition to Stage 3
        if score >= 100 and stage == 2:
            stage = 3
            show_stage_three_intro()
            blocks.empty()
            hostile_blocks.empty()
        
        # Add blocks and hostile blocks randomly
        if random.randint(1, 20) == 1:
            blocks.add(create_block())
        
        if random.randint(1, 50) == 1:
            hostile_blocks.add(create_hostile_block())
        
        if stage == 2 and len(walls) < max_walls and random.randint(1, 100) == 1:
            walls.add(create_wall())
        
        if stage == 3 and len(walls) < max_walls and random.randint(1, 100) == 1:
            walls.add(create_wall())
        
        # Update all game elements
        blocks.update()
        hostile_blocks.update()
        walls.update()
        
        # Check for collisions
        for block in blocks:
            if block.rect.colliderect(player.rect):
                score += 1
                block.kill()
        
        for hostile_block in hostile_blocks:
            if hostile_block.rect.colliderect(player.rect):
                health -= 1
                hostile_block.kill()
                if health == 0:
                    game_over = True
        
        for wall in walls:
            if wall.rect.colliderect(player.rect):
                if wall.rect.bottom > player.rect.top:  # Check if player is below the wall
                    health = 0
                    game_over = True
        
        # Remove walls that move off the screen
        for wall in walls:
            if wall.rect.y > SCREEN_HEIGHT:
                wall.kill()
        
        # Draw game elements
        draw_game()
        clock.tick(60)
    
    return game_over

# Initialize player
player = Player()

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
