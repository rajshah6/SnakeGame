'''
Name: Raj Shah
Date Modified: August 16, 2023
Version 1.4.2

Description: This program is a simple snake game that can be played with the arrow keys. Move the snake around
and eat apples to grow bigger and obtain a larger score. Make sure not to bump into the snake's body or any of
the walls surrounding the snake. Have fun!
'''

import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 640, 480
CELL_SIZE = 20
GRID_WIDTH, GRID_HEIGHT = WIDTH // CELL_SIZE, HEIGHT // CELL_SIZE # change width and height proportionate to cell size
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Load background music
background_music = pygame.mixer.Sound("background_music.wav")  

# Load sounds
game_over_sound = pygame.mixer.Sound("game_over.wav")  
eat_apple_sound = pygame.mixer.Sound("eat_apple.wav")  

# COLOURs
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 128, 0)  # dark green
RED = (178, 34, 34)  # dark red
GRID_COLOUR = (51, 51, 51)  # dark gray

# Game loop variables
clock = pygame.time.Clock()
running = True
game_over = False
title_screen = True

# Snake variables
snake_pos = [GRID_WIDTH // 2, GRID_HEIGHT // 2] # middle of board
snake_body = [[GRID_WIDTH // 2, GRID_HEIGHT // 2], [GRID_WIDTH // 2 - 1, GRID_HEIGHT // 2], [GRID_WIDTH // 2 - 2, GRID_HEIGHT // 2]] # initialize with 3 squares
snake_dir = 'RIGHT' # start with facing right

# Fruits
fruits = [{'pos': [random.randrange(1, GRID_WIDTH - 1), random.randrange(1, GRID_HEIGHT - 1)]}] # generate fruit in a random position on the board, then store position in array
fruit_spawn = True

# Score
score = 0
high_score = 0

# Title screen loop
while title_screen:
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

            elif event.key == pygame.K_RETURN:
                title_screen = False # exit title screen

    # Clear the screen
    screen.fill(BLACK)

    # Display title screen text and instructions
    font = pygame.font.Font(None, 72)
    title_text = font.render("Welcome to Snake Game!", True, WHITE)
    title_rect = title_text.get_rect(center=(WIDTH/2, HEIGHT/4)) 
    screen.blit(title_text, title_rect)
    
    instructions = [
        "Use arrow keys to control the snake's direction.",
        "Eat red apples to grow longer and earn points.",
        "Avoid colliding with the walls or the snake's body.",
        "Press ENTER to start the game.",
        "Press ESC at any time to quit."
    ]
    
    font = pygame.font.Font(None, 36)
    for i, instruction in enumerate(instructions): 
        # Print instructions line by line
        instruction_text = font.render(instruction, True, WHITE)
        instruction_rect = instruction_text.get_rect(center=(WIDTH/2, HEIGHT/2 + i * 30))
        screen.blit(instruction_text, instruction_rect)

    pygame.display.flip()
    clock.tick(10) 

music_playing = False 

# Main game loop
while running:
    if music_playing == False:
        background_music.play(-1) # play the background music in a loop
        background_music.set_volume(0.5)
        music_playing = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
          
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

            elif not game_over:
                # Update snake direction based on key input. Ensure direction inputted is perpendicular to current position
                if event.key == pygame.K_UP and snake_dir != 'DOWN':
                    snake_dir = 'UP'
                elif event.key == pygame.K_DOWN and snake_dir != 'UP':
                    snake_dir = 'DOWN'
                elif event.key == pygame.K_LEFT and snake_dir != 'RIGHT':
                    snake_dir = 'LEFT'
                elif event.key == pygame.K_RIGHT and snake_dir != 'LEFT':
                    snake_dir = 'RIGHT'
            else:
                # Reset the game when game over and ENTER is pressed
                if event.key == pygame.K_RETURN:
                    game_over = False
                    snake_pos = [GRID_WIDTH // 2, GRID_HEIGHT // 2]
                    snake_body = [[GRID_WIDTH // 2, GRID_HEIGHT // 2], [GRID_WIDTH // 2 - 1, GRID_HEIGHT // 2], [GRID_WIDTH // 2 - 2, GRID_HEIGHT // 2]]
                    snake_dir = 'RIGHT'
                    fruits = [{'pos': [random.randrange(1, GRID_WIDTH - 1), random.randrange(1, GRID_HEIGHT - 1)]}]
                    fruit_spawn = True
                    score = 0

    if not game_over:
        # Update snake position based on direction
        if snake_dir == 'RIGHT':
            snake_pos[0] += 1
        elif snake_dir == 'LEFT':
            snake_pos[0] -= 1
        elif snake_dir == 'UP':
            snake_pos[1] -= 1
        elif snake_dir == 'DOWN':
            snake_pos[1] += 1

        # Snake body growing mechanism
        snake_body.insert(0, list(snake_pos)) # enlarge snake depending on where its tail is
        if snake_pos == fruits[0]['pos']: # check if snake has eaten apple
            score += 1
            eat_apple_sound.play()
            fruits[0]['pos'] = [random.randrange(1, GRID_WIDTH - 1), random.randrange(1, GRID_HEIGHT - 1)] # create new position for apple
        else:
            snake_body.pop() # undo the enlargement

        # Check for collision with boundaries or snake body
        if (snake_pos[0] < 0 or snake_pos[0] >= GRID_WIDTH or
                snake_pos[1] < 0 or snake_pos[1] >= GRID_HEIGHT or
                snake_pos in snake_body[1:]):
            game_over = True
            game_over_sound.play()

    # Clear the screen
    screen.fill(BLACK)

    # Draw grid
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, GRID_COLOUR, (x, 0), (x, HEIGHT)) # draw the vertical lines with the spacing of the grid length

    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, GRID_COLOUR, (0, y), (WIDTH, y)) # draw horizontal lines

    if not game_over:
        # Draw snake
        for segment in snake_body:
            pygame.draw.rect(screen, GREEN, pygame.Rect(segment[0] * CELL_SIZE, segment[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # Draw fruit
        pygame.draw.rect(screen, RED, pygame.Rect(fruits[0]['pos'][0] * CELL_SIZE, fruits[0]['pos'][1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # Display score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

    # Game over screen
    else: 
        background_music.stop()
        music_playing = False 

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

        # Create high score
        if score > high_score:
            high_score = score
        
        # Display game over text and instructions
        font = pygame.font.Font(None, 72)
        game_over_text = font.render("Game Over!", True, WHITE)
        game_over_rect = game_over_text.get_rect(center=(WIDTH/2, HEIGHT/2 - 50))
        screen.blit(game_over_text, game_over_rect)
        
        font = pygame.font.Font(None, 36)
        play_again_text = font.render(f"Press ENTER to play again", True, WHITE)
        play_again_rect = play_again_text.get_rect(center=(WIDTH/2, HEIGHT/2))
        screen.blit(play_again_text, play_again_rect)

        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}          High Score: {high_score}", True, WHITE)
        score_rect = score_text.get_rect(center=(WIDTH/2, HEIGHT/2 + 35))
        screen.blit(score_text, score_rect)

    # Update display
    pygame.display.flip()

    # Speed of the snake, adjust this value as needed
    clock.tick(10) 

# Quit Pygame
pygame.quit()
sys.exit()
