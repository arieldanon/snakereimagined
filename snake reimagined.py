import pygame
import time
import random

pygame.init()

# Set up the game window!
width, height = 600, 400
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Reimagined")

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
purple = (128, 0, 128)
orange = (255, 165, 0)

# Snake and Apple
snake_block = 10
base_snake_speed = 15
snake_speed = base_snake_speed
snake_pos = [100, 50]
snake_body = [[100, 50], [90, 50], [80, 50]]
change_to = [10, 0]

apple_pos = [random.randrange(1, (width // 10)) * 10, random.randrange(1, (height // 10)) * 10]

# Power-ups
power_ups = []
power_up_duration = 10  # in seconds
power_up_start_time = 0

# Speed boost
speed_boost_active = False
speed_boost_duration = 5  # in seconds
speed_boost_start_time = 0
speed_boost_multiplier = 1.5  # Increase speed by 50%

# Reverse item
reverse_active = False
reverse_duration = 5  # in seconds
reverse_start_time = 0

# Obstacles
obstacle_size = 20
obstacle_gap = 10  # Reduced gap between obstacles
obstacles = [
    [200, 100],
    [400, 150],
    [200, 200],
    [400, 250],
    [200, 300],
]

# Score
score = 0
font = pygame.font.SysFont(None, 25)

# Color options for the snake
snake_colors = [red, green, blue, yellow, purple, orange]
current_snake_color = random.choice(snake_colors)

# Game over flag
game_over = False

# Retry flag
retry = False

def reset_game():
    global snake_pos, snake_body, change_to, apple_pos, power_ups, score, game_over, retry
    snake_pos = [100, 50]
    snake_body = [[100, 50], [90, 50], [80, 50]]
    change_to = [10, 0]
    apple_pos = [random.randrange(1, (width // 10)) * 10, random.randrange(1, (height // 10)) * 10]
    power_ups = []
    score = 0
    game_over = False
    retry = False

# Game loop
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and change_to[1] == 0:
                change_to = [0, -snake_block]
            elif event.key == pygame.K_DOWN and change_to[1] == 0:
                change_to = [0, snake_block]
            elif event.key == pygame.K_LEFT and change_to[0] == 0:
                change_to = [-snake_block, 0]
            elif event.key == pygame.K_RIGHT and change_to[0] == 0:
                change_to = [snake_block, 0]

    # Update snake position
    snake_pos[0] += change_to[0]
    snake_pos[1] += change_to[1]

    # Check if snake eats the apple
    if snake_pos[0] == apple_pos[0] and snake_pos[1] == apple_pos[1]:
        apple_pos = [random.randrange(1, (width // 10)) * 10, random.randrange(1, (height // 10)) * 10]
        score += 1

        # Change snake color after eating
        current_snake_color = random.choice(snake_colors)

        # Spawn power-up randomly
        if random.randint(1, 2) == 1:  # 50% chance of spawning a power-up
            power_ups.append([random.randrange(1, (width // 10)) * 10, random.randrange(1, (height // 10)) * 10])

        # Extend snake body
        snake_body.append([])

    # Check if snake collides with power-up
    for power_up in power_ups:
        if snake_pos[0] == power_up[0] and snake_pos[1] == power_up[1]:
            power_ups.remove(power_up)

            # Apply power-up effect
            power_up_type = random.choice(["speed_boost", "reverse"])
            if power_up_type == "speed_boost":
                speed_boost_active = True
                speed_boost_start_time = time.time()
            elif power_up_type == "reverse":
                reverse_active = True
                reverse_start_time = time.time()

    # Update power-up effects
    if speed_boost_active and time.time() - speed_boost_start_time > speed_boost_duration:
        speed_boost_active = False
        snake_speed = base_snake_speed  # Reset speed after speed boost ends

    if reverse_active and time.time() - reverse_start_time > reverse_duration:
        reverse_active = False

    # Update snake speed with speed boost
    if speed_boost_active:
        snake_speed = int(base_snake_speed * speed_boost_multiplier)

    # Update snake body
    for i in range(len(snake_body) - 1, 0, -1):
        snake_body[i] = snake_body[i - 1]

    snake_body[0] = list(snake_pos)

    # Game over if snake hits the boundaries or collides with itself or obstacles
    if (
        snake_pos[0] < 0
        or snake_pos[0] >= width
        or snake_pos[1] < 0
        or snake_pos[1] >= height
        or snake_pos in snake_body[1:]
        or any(
            obstacle[0] <= snake_pos[0] <= obstacle[0] + obstacle_size
            and obstacle[1] <= snake_pos[1] <= obstacle[1] + obstacle_size
            for obstacle in obstacles
        )
    ):
        game_over = True

    # Game over if snake collides with obstacles
    for obstacle in obstacles:
        if snake_pos[0] == obstacle[0] and snake_pos[1] == obstacle[1]:
            game_over = True

    # Draw everything
    window.fill(white)

    # Draw grid lines
    for x in range(0, width, 10):
        pygame.draw.line(window, black, (x, 0), (x, height))
    for y in range(0, height, 10):
        pygame.draw.line(window, black, (0, y), (width, y))

    # Draw obstacles
    for obstacle in obstacles:
        pygame.draw.rect(window, black, [obstacle[0], obstacle[1], obstacle_size, obstacle_size])

    # Draw snake body
    for segment in snake_body:
        pygame.draw.rect(window, current_snake_color, [segment[0], segment[1], snake_block, snake_block])

    # Draw apple
    pygame.draw.rect(window, red, [apple_pos[0], apple_pos[1], snake_block, snake_block])

    # Draw power-ups
    for power_up in power_ups:
        pygame.draw.rect(window, green, [power_up[0], power_up[1], snake_block, snake_block])

    # Draw score
    score_text = font.render("Score: " + str(score), True, black)
    window.blit(score_text, [10, 10])

    # Control snake speed
    pygame.time.Clock().tick(snake_speed)

    # Update display
    pygame.display.update()

# Game over display
font_large = pygame.font.SysFont(None, 50)
game_over_text = font_large.render("Game Over", True, black)
score_text = font.render("Your Score: " + str(score), True, black)
retry_text = font.render("Press 'R' to Retry", True, black)

window.blit(game_over_text, [width // 4, height // 3])
window.blit(score_text, [width // 3, height // 2])
window.blit(retry_text, [width // 3, height // 1.7])
pygame.display.update()

# Wait for key press to retry
retry = False
while not retry:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            reset_game()
            retry = True
            break
        elif event.type == pygame.QUIT:
            retry = True  # Exit the retry loop if the window is closed

    pygame.time.Clock().tick(10)

# Quit the game
pygame.quit()