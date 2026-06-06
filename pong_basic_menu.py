mport pygame
import math
import sys

pygame.init()

# ----------------------------
# SETTINGS
# ----------------------------
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


# ----------------------------
# MENU
# ----------------------------
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

        controls = MENU_FONT.render(
            "P1: W/S    P2: UP/DOWN",
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
            (WIDTH // 2 - option1.get_width() // 2, 250)
        )

        screen.blit(
            option2,
            (WIDTH // 2 - option2.get_width() // 2, 320)
        )

        screen.blit(
            controls,
            (WIDTH // 2 - controls.get_width() // 2, 390)
        )

        screen.blit(
            quit_text,
            (WIDTH // 2 - quit_text.get_width() // 2, 460)
        )

        pygame.display.flip()
        clock.tick(60)


# ----------------------------
# WIN SCREEN
# ----------------------------
def winner_screen(text):

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

        winner = TITLE_FONT.render(text, True, WHITE)

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


# ----------------------------
# SPEED FUNCTION
# ----------------------------
def increase_speed(vx, vy):

    speed = math.sqrt(vx*2 + vy*2)

    speed = min(speed * SPEED_INCREASE, MAX_SPEED)

    angle = math.atan2(vy, vx)

    vx = math.cos(angle) * speed
    vy = math.sin(angle) * speed

    return vx, vy


# ----------------------------
# GAME LOOP
# ----------------------------
while True:

    game_mode = menu()

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

    def reset_ball(direction):
        nonlocal_ball = [direction]

        ball.center = (WIDTH // 2, HEIGHT // 2)

        return (
            INITIAL_SPEED * direction,
            INITIAL_SPEED if pygame.time.get_ticks() % 2 else -INITIAL_SPEED
        )

    running = True

    while running:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()

        # Left paddle
        if keys[pygame.K_w]:
            left_paddle.y -= PADDLE_SPEED

        if keys[pygame.K_s]:
            left_paddle.y += PADDLE_SPEED

        # Right paddle
        if game_mode == 1:

            AI_SPEED = 6

            if right_paddle.centery < ball.centery:
                right_paddle.y += AI_SPEED

            elif right_paddle.centery > ball.centery:
                right_paddle.y -= AI_SPEED

        else:

            if keys[pygame.K_UP]:
                right_paddle.y -= PADDLE_SPEED

            if keys[pygame.K_DOWN]:
                right_paddle.y += PADDLE_SPEED

        # Keep paddles on screen
        left_paddle.y = max(
            0,
            min(left_paddle.y, HEIGHT - left_paddle.height)
        )

        right_paddle.y = max(
            0,
            min(right_paddle.y, HEIGHT - right_paddle.height)
        )

        # Ball movement
        ball.x += ball_x
        ball.y += ball_y

        # Wall collisions
        if ball.top <= 0:
            ball.top = 0
            ball_y *= -1

        if ball.bottom >= HEIGHT:
            ball.bottom = HEIGHT
            ball_y *= -1

        # Left paddle collision
        if ball.colliderect(left_paddle) and ball_x < 0:

            ball.left = left_paddle.right

            offset = (
                ball.centery - left_paddle.centery
            ) / (left_paddle.height / 2)

            speed = math.sqrt(ball_x*2 + ball_y*2)

            ball_x = abs(ball_x)
            ball_y = offset * speed

            ball_x, ball_y = increase_speed(
                ball_x,
                ball_y
            )

        # Right paddle collision
        if ball.colliderect(right_paddle) and ball_x > 0:

            ball.right = right_paddle.left

            offset = (
                ball.centery - right_paddle.centery
            ) / (right_paddle.height / 2)

            speed = math.sqrt(ball_x*2 + ball_y*2)

            ball_x = -abs(ball_x)
            ball_y = offset * speed

            ball_x, ball_y = increase_speed(
                ball_x,
                ball_y
            )

        # Score
        if ball.left <= 0:

            right_score += 1

            ball_x, ball_y = reset_ball(1)

        if ball.right >= WIDTH:

            left_score += 1

            ball_x, ball_y = reset_ball(-1)

        # Win condition
        if left_score >= WIN_SCORE:

            winner_screen("PLAYER 1 WINS!")
            running = False

        if right_score >= WIN_SCORE:

            if game_mode == 1:
                winner_screen("AI WINS!")
            else:
                winner_screen("PLAYER 2 WINS!")

            running = False

        # Draw
        screen.fill(BLACK)

        for y in range(0, HEIGHT, 30):

            pygame.draw.rect(
                screen,
                WHITE,
                (WIDTH // 2 - 2, y, 4, 15)
            )

        pygame.draw.rect(screen, WHITE, left_paddle)
        pygame.draw.rect(screen, WHITE, right_paddle)

        pygame.draw.ellipse(screen, WHITE, ball)

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

        screen.blit(left_text, (WIDTH // 4, 20))
        screen.blit(right_text, (WIDTH * 3 // 4, 20))

        pygame.display.flip()
        clock.tick(60)
