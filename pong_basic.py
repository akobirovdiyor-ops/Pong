import pygame
import math

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Font
font = pygame.font.SysFont(None, 60)

# Paddles
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100

player = pygame.Rect(
    30,
    HEIGHT // 2 - PADDLE_HEIGHT // 2,
    PADDLE_WIDTH,
    PADDLE_HEIGHT
)

enemy = pygame.Rect(
    WIDTH - 40,
    HEIGHT // 2 - PADDLE_HEIGHT // 2,
    PADDLE_WIDTH,
    PADDLE_HEIGHT
)

# Ball
BALL_SIZE = 20
ball = pygame.Rect(
    WIDTH // 2 - BALL_SIZE // 2,
    HEIGHT // 2 - BALL_SIZE // 2,
    BALL_SIZE,
    BALL_SIZE
)

# Game settings
INITIAL_SPEED = 5
SPEED_INCREASE = 1.08
MAX_SPEED = 18

ball_x = INITIAL_SPEED
ball_y = INITIAL_SPEED

player_score = 0
enemy_score = 0


def reset_ball(direction):
    global ball_x, ball_y

    ball.center = (WIDTH // 2, HEIGHT // 2)

    ball_x = INITIAL_SPEED * direction

    # Randomize slight vertical direction
    ball_y = INITIAL_SPEED if pygame.time.get_ticks() % 2 else -INITIAL_SPEED


def increase_speed(vx, vy):
    speed = math.sqrt(vx * vx + vy * vy)

    speed = min(speed * SPEED_INCREASE, MAX_SPEED)

    angle = math.atan2(vy, vx)

    vx = math.cos(angle) * speed
    vy = math.sin(angle) * speed

    return vx, vy


running = True

while running:

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player movement
    keys = pygame.key.get_pressed()

    if keys[pygame.K_UP]:
        player.y -= 7

    if keys[pygame.K_DOWN]:
        player.y += 7

    # Keep player on screen
    player.y = max(0, min(player.y, HEIGHT - player.height))

    # AI movement
    ai_speed = 6

    if enemy.centery < ball.centery:
        enemy.y += ai_speed
    elif enemy.centery > ball.centery:
        enemy.y -= ai_speed

    enemy.y = max(0, min(enemy.y, HEIGHT - enemy.height))

    # Ball movement
    ball.x += ball_x
    ball.y += ball_y

    # Wall collision
    if ball.top <= 0:
        ball.top = 0
        ball_y *= -1

    if ball.bottom >= HEIGHT:
        ball.bottom = HEIGHT
        ball_y *= -1

    # Paddle collision (player)
    if ball.colliderect(player) and ball_x < 0:

        ball.left = player.right

        # Change angle based on hit location
        offset = (
            ball.centery - player.centery
        ) / (player.height / 2)

        speed = math.sqrt(ball_x*2 + ball_y*2)

        ball_x = abs(ball_x)
        ball_y = offset * speed

        ball_x, ball_y = increase_speed(ball_x, ball_y)

    # Paddle collision (enemy)
    if ball.colliderect(enemy) and ball_x > 0:

        ball.right = enemy.left

        offset = (
            ball.centery - enemy.centery
        ) / (enemy.height / 2)

        speed = math.sqrt(ball_x*2 + ball_y*2)

        ball_x = -abs(ball_x)
        ball_y = offset * speed

        ball_x, ball_y = increase_speed(ball_x, ball_y)

    # Scoring
    if ball.left <= 0:
        enemy_score += 1
        reset_ball(1)

    if ball.right >= WIDTH:
        player_score += 1
        reset_ball(-1)

    # Drawing
    screen.fill(BLACK)

    # Center line
    pygame.draw.line(
        screen,
        WHITE,
        (WIDTH // 2, 0),
        (WIDTH // 2, HEIGHT),
        2
    )

    # Paddles
    pygame.draw.rect(screen, WHITE, player)
    pygame.draw.rect(screen, WHITE, enemy)

    # Ball
    pygame.draw.ellipse(screen, WHITE, ball)

    # Scores
    player_text = font.render(str(player_score), True, WHITE)
    enemy_text = font.render(str(enemy_score), True, WHITE)

    screen.blit(player_text, (WIDTH // 4, 20))
    screen.blit(enemy_text, (WIDTH * 3 // 4, 20))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
