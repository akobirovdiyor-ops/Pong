import pygame
import math
import sys

pygame.init()

# ==========================================
# SETTINGS
# ==========================================

WIDTH, HEIGHT = 1000, 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

TITLE_FONT = pygame.font.SysFont(None, 90)
MENU_FONT = pygame.font.SysFont(None, 50)
SCORE_FONT = pygame.font.SysFont(None, 70)

PADDLE_WIDTH = 15
PADDLE_HEIGHT = 120
PADDLE_SPEED = 8

BALL_SIZE = 20

INITIAL_SPEED = 6
SPEED_INCREASE = 1.08
MAX_SPEED = 20

WIN_SCORE = 10


# ==========================================
# MENU
# ==========================================

def menu():

    while True:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_1:
                    return 1

                if event.key == pygame.K_2:
                    return 2

                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        screen.fill(BLACK)

        title = TITLE_FONT.render("PONG", True, WHITE)

        option1 = MENU_FONT.render(
            "Press 1 - Single Player",
            True,
            WHITE
        )

        option2 = MENU_FONT.render(
            "Press 2 - Two Players",
            True,
            WHITE
        )

        quit_text = MENU_FONT.render(
            "ESC - Quit",
            True,
            WHITE
        )

        screen.blit(
            title,
            (WIDTH // 2 - title.get_width() // 2, 100)
        )

        screen.blit(
            option1,
            (WIDTH // 2 - option1.get_width() // 2, 260)
        )

        screen.blit(
            option2,
            (WIDTH // 2 - option2.get_width() // 2, 330)
        )

        screen.blit(
            quit_text,
            (WIDTH // 2 - quit_text.get_width() // 2, 450)
        )

        pygame.display.flip()
        clock.tick(60)


# ==========================================
# CONTROLS SCREEN
# ==========================================

def show_controls(game_mode):

    while True:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE:
                    return

        screen.fill(BLACK)

        title = TITLE_FONT.render(
            "CONTROLS",
            True,
            WHITE
        )

        p1 = MENU_FONT.render(
            "Player 1: W / S",
            True,
            WHITE
        )

        screen.blit(
            title,
            (WIDTH // 2 - title.get_width() // 2, 120)
        )

        screen.blit(
            p1,
            (WIDTH // 2 - p1.get_width() // 2, 250)
        )

        if game_mode == 1:
            p2 = MENU_FONT.render(
                "Player 2: AI",
                True,
                WHITE
            )
        else:
            p2 = MENU_FONT.render(
                "Player 2: UP / DOWN ARROWS",
                True,
                WHITE
            )

        screen.blit(
            p2,
            (WIDTH // 2 - p2.get_width() // 2, 320)
        )

        start = MENU_FONT.render(
            "Press SPACE to Start",
            True,
            WHITE
        )

        screen.blit(
            start,
            (WIDTH // 2 - start.get_width() // 2, 450)
        )

        pygame.display.flip()
        clock.tick(60)


# ==========================================
# COUNTDOWN
# ==========================================

def countdown():

    for text_value in ["3", "2", "1", "GO!"]:

        start_time = pygame.time.get_ticks()

        while pygame.time.get_ticks() - start_time < 1000:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            screen.fill(BLACK)

            text = TITLE_FONT.render(
                text_value,
                True,
                WHITE
            )

            screen.blit(
                text,
                (
                    WIDTH // 2 - text.get_width() // 2,
                    HEIGHT // 2 - text.get_height() // 2
                )
            )

            pygame.display.flip()
            clock.tick(60)


# ==========================================
# WINNER SCREEN
# ==========================================

def winner_screen(message):

    while True:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_r:
                    return

                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        screen.fill(BLACK)

        winner = TITLE_FONT.render(
            message,
            True,
            WHITE
        )

        restart = MENU_FONT.render(
            "Press R to Play Again",
            True,
            WHITE
        )

        quit_text = MENU_FONT.render(
            "ESC to Quit",
            True,
            WHITE
        )

        screen.blit(
            winner,
            (WIDTH // 2 - winner.get_width() // 2, 180)
        )

        screen.blit(
            restart,
            (WIDTH // 2 - restart.get_width() // 2, 320)
        )

        screen.blit(
            quit_text,
            (WIDTH // 2 - quit_text.get_width() // 2, 390)
        )

        pygame.display.flip()
        clock.tick(60)


# ==========================================
# SPEED INCREASE
# ==========================================

def increase_speed(vx, vy):

    speed = math.sqrt(vx * 2 + vy * 2)

    speed = min(
        speed * SPEED_INCREASE,
        MAX_SPEED
    )

    angle = math.atan2(vy, vx)

    vx = math.cos(angle) * speed
    vy = math.sin(angle) * speed

    return vx, vy


# ==========================================
# MAIN LOOP
# ==========================================

while True:

    game_mode = menu()

    show_controls(game_mode)

    countdown()

    left_score = 0
    right_score = 0

    left_paddle = pygame.Rect(
        30,
        HEIGHT // 2 - PADDLE_HEIGHT // 2,
        PADDLE_WIDTH,
        PADDLE_HEIGHT
    )

    right_paddle = pygame.Rect(
        WIDTH - 45,
        HEIGHT // 2 - PADDLE_HEIGHT // 2,
        PADDLE_WIDTH,
        PADDLE_HEIGHT
    )

    ball = pygame.Rect(
        WIDTH // 2 - BALL_SIZE // 2,
        HEIGHT // 2 - BALL_SIZE // 2,
        BALL_SIZE,
        BALL_SIZE
    )

    ball_x = INITIAL_SPEED
    ball_y = INITIAL_SPEED

    running = True

    while running:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()

        # ====================
        # PLAYER 1
        # ====================

        if keys[pygame.K_w]:
            left_paddle.y -= PADDLE_SPEED

        if keys[pygame.K_s]:
            left_paddle.y += PADDLE_SPEED

        # ====================
        # PLAYER 2 OR AI
        # ====================

        if game_mode == 1:

            ai_speed = 6

            if right_paddle.centery < ball.centery:
                right_paddle.y += ai_speed

            elif right_paddle.centery > ball.centery:
                right_paddle.y -= ai_speed

        else:

            if keys[pygame.K_UP]:
                right_paddle.y -= PADDLE_SPEED

            if keys[pygame.K_DOWN]:
                right_paddle.y += PADDLE_SPEED

        # ====================
        # BOUNDARIES
        # ====================

        left_paddle.y = max(
            0,
            min(
                left_paddle.y,
                HEIGHT - left_paddle.height
            )
        )

        right_paddle.y = max(
            0,
            min(
                right_paddle.y,
                HEIGHT - right_paddle.height
            )
        )

        # ====================
        # MOVE BALL
        # ====================

        ball.x += ball_x
        ball.y += ball_y

        # ====================
        # WALL COLLISION
        # ====================

        if ball.top <= 0:
            ball.top = 0
            ball_y *= -1

        if ball.bottom >= HEIGHT:
            ball.bottom = HEIGHT
            ball_y *= -1

        # ====================
        # LEFT PADDLE HIT
        # ====================

        if ball.colliderect(left_paddle) and ball_x < 0:

            ball.left = left_paddle.right

            offset = (
                ball.centery - left_paddle.centery
            ) / (left_paddle.height / 2)

            speed = math.sqrt(
                ball_x * 2 + ball_y * 2
            )

            ball_x = abs(ball_x)
            ball_y = offset * speed

            ball_x, ball_y = increase_speed(
                ball_x,
                ball_y
            )

        # ====================
        # RIGHT PADDLE HIT
        # ====================

        if ball.colliderect(right_paddle) and ball_x > 0:

            ball.right = right_paddle.left

            offset = (
                ball.centery - right_paddle.centery
            ) / (right_paddle.height / 2)

            speed = math.sqrt(
                ball_x * 2 + ball_y * 2
            )

            ball_x = -abs(ball_x)
            ball_y = offset * speed

            ball_x, ball_y = increase_speed(
                ball_x,
                ball_y
            )

        # ====================
        # SCORE
        # ====================

        if ball.left <= 0:

            right_score += 1

            ball.center = (
                WIDTH // 2,
                HEIGHT // 2
            )

            ball_x = INITIAL_SPEED
            ball_y = INITIAL_SPEED

            countdown()

        if ball.right >= WIDTH:

            left_score += 1

            ball.center = (
                WIDTH // 2,
                HEIGHT // 2
            )

            ball_x = -INITIAL_SPEED
            ball_y = INITIAL_SPEED

            countdown()

        # ====================
        # WIN CONDITION
        # ====================

        if left_score >= WIN_SCORE:

            winner_screen(
                "PLAYER 1 WINS!"
            )

            running = False

        if right_score >= WIN_SCORE:

            if game_mode == 1:
                winner_screen(
                    "AI WINS!"
                )
            else:
                winner_screen(
                    "PLAYER 2 WINS!"
                )

            running = False

        # ====================
        # DRAW
        # ====================

        screen.fill(BLACK)

        for y in range(0, HEIGHT, 30):

            pygame.draw.rect(
                screen,
                WHITE,
                (
                    WIDTH // 2 - 2,
                    y,
                    4,
                    15
                )
            )

        pygame.draw.rect(
            screen,
            WHITE,
            left_paddle
        )

        pygame.draw.rect(
            screen,
            WHITE,
            right_paddle
        )

        pygame.draw.ellipse(
            screen,
            WHITE,
            ball
        )

        left_text = SCORE_FONT.render(
            str(left_score),
            True,
            WHITE
        )

        right_text = SCORE_FONT.render(
            str(right_score),
            True,
            WHITE
        )

        screen.blit(
            left_text,
            (WIDTH // 4, 20)
        )

        screen.blit(
            right_text,
            (WIDTH * 3 // 4, 20)
        )

        pygame.display.flip()

        clock.tick(60)
