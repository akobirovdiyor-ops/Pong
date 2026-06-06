import pygame
import math
import sys
import random

pygame.init()

# =========================
# SCREEN
# =========================
WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Neon Pong")

clock = pygame.time.Clock()

# =========================
# COLORS
# =========================
BG = (10, 12, 30)
WHITE = (240, 240, 240)
CYAN = (0, 255, 255)
PINK = (255, 60, 200)
BLUE = (80, 160, 255)

# =========================
# FONTS
# =========================
TITLE_FONT = pygame.font.SysFont("Arial", 80)
MENU_FONT = pygame.font.SysFont("Arial", 40)
SCORE_FONT = pygame.font.SysFont("Arial", 60)

# =========================
# SETTINGS
# =========================
PADDLE_W, PADDLE_H = 15, 120
PADDLE_SPEED = 8

BALL_SIZE = 18

INITIAL_SPEED = 6
SPEED_BOOST = 1.05
MAX_SPEED = 18

WIN_SCORE = 10

# =========================
# EFFECTS
# =========================
particles = []
trail = []


# =========================
# MENU
# =========================
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

        screen.fill(BG)

        title = TITLE_FONT.render("NEON PONG", True, CYAN)
        opt1 = MENU_FONT.render("1 - Single Player", True, WHITE)
        opt2 = MENU_FONT.render("2 - Two Players", True, WHITE)
        info = MENU_FONT.render("P1: W/S | P2: UP/DOWN", True, PINK)

        screen.blit(title, (WIDTH//2 - title.get_width()//2, 120))
        screen.blit(opt1, (WIDTH//2 - opt1.get_width()//2, 260))
        screen.blit(opt2, (WIDTH//2 - opt2.get_width()//2, 320))
        screen.blit(info, (WIDTH//2 - info.get_width()//2, 400))

        pygame.display.flip()
        clock.tick(60)


# =========================
# WIN SCREEN
# =========================
def win_screen(text):
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

        screen.fill(BG)

        t = TITLE_FONT.render(text, True, CYAN)
        info = MENU_FONT.render("Press R to Restart", True, WHITE)

        screen.blit(t, (WIDTH//2 - t.get_width()//2, 250))
        screen.blit(info, (WIDTH//2 - info.get_width()//2, 380))

        pygame.display.flip()
        clock.tick(60)


# =========================
# COUNTDOWN
# =========================
def countdown():
    for txt in ["3", "2", "1", "GO"]:
        start = pygame.time.get_ticks()

        while pygame.time.get_ticks() - start < 700:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            screen.fill(BG)

            t = TITLE_FONT.render(txt, True, CYAN)
            screen.blit(t, (WIDTH//2 - t.get_width()//2, HEIGHT//2 - t.get_height()//2))

            pygame.display.flip()
            clock.tick(60)


# =========================
# SPEED CONTROL (ARC BOUNCE)
# =========================
def increase_speed(vx, vy):
    speed = math.sqrt(vx*2 + vy*2)
    speed = min(speed * SPEED_BOOST, MAX_SPEED)

    angle = math.atan2(vy, vx)
    return math.cos(angle) * speed, math.sin(angle) * speed


# =========================
# PARTICLES
# =========================
def spawn_particles(x, y, color):
    for _ in range(6):
        particles.append([
            x, y,
            random.randint(-2, 2),
            random.randint(-2, 2),
            color,
            4
        ])


def update_particles():
    for p in particles[:]:
        p[0] += p[2]
        p[1] += p[3]
        p[5] -= 0.2
        if p[5] <= 0:
            particles.remove(p)


# =========================
# GAME LOOP
# =========================
while True:

    mode = menu()

    left = pygame.Rect(30, HEIGHT//2 - PADDLE_H//2, PADDLE_W, PADDLE_H)
    right = pygame.Rect(WIDTH-45, HEIGHT//2 - PADDLE_H//2, PADDLE_W, PADDLE_H)

    ball = pygame.Rect(WIDTH//2, HEIGHT//2, BALL_SIZE, BALL_SIZE)

    vx, vy = INITIAL_SPEED, INITIAL_SPEED

    left_score = 0
    right_score = 0

    trail = []
    particles = []

    countdown()

    running = True

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()

        # =========================
        # PLAYER 1
        # =========================
        if keys[pygame.K_w]:
            left.y -= PADDLE_SPEED
        if keys[pygame.K_s]:
            left.y += PADDLE_SPEED

        # =========================
        # PLAYER 2 / AI
        # =========================
        if mode == 1:
            ai_speed = 6
            deadzone = 12

            if abs(right.centery - ball.centery) > deadzone:
                if right.centery < ball.centery:
                    right.y += ai_speed
                else:
                    right.y -= ai_speed
        else:
            if keys[pygame.K_UP]:
                right.y -= PADDLE_SPEED
            if keys[pygame.K_DOWN]:
                right.y += PADDLE_SPEED

        # clamp paddles
        left.y = max(0, min(HEIGHT-left.height, left.y))
        right.y = max(0, min(HEIGHT-right.height, right.y))

        # =========================
        # MOVE BALL
        # =========================
        ball.x += vx
        ball.y += vy

        # =========================
        # TRAIL (SHORT)
        # =========================
        trail.append((ball.x, ball.y))
        if len(trail) > 8:
            trail.pop(0)

        # =========================
        # WALLS
        # =========================
        if ball.top <= 0 or ball.bottom >= HEIGHT:
            vy *= -1

        # =========================
        # COLLISION LEFT
        # =========================
        if ball.colliderect(left) and vx < 0:

            hit_pos = (ball.centery - left.centery) / (left.height / 2)
            vx = abs(vx)
            vy = hit_pos * 5

            vx, vy = increase_speed(vx, vy)

            spawn_particles(ball.x, ball.y, PINK)

        # =========================
        # COLLISION RIGHT
        # =========================
        if ball.colliderect(right) and vx > 0:

            hit_pos = (ball.centery - right.centery) / (right.height / 2)
            vx = -abs(vx)
            vy = hit_pos * 5

            vx, vy = increase_speed(vx, vy)

            spawn_particles(ball.x, ball.y, BLUE)

        # =========================
        # SCORE
        # =========================
        if ball.left <= 0:
            right_score += 1
            ball.center = (WIDTH//2, HEIGHT//2)
            vx, vy = INITIAL_SPEED, INITIAL_SPEED
            countdown()

        if ball.right >= WIDTH:
            left_score += 1
            ball.center = (WIDTH//2, HEIGHT//2)
            vx, vy = -INITIAL_SPEED, INITIAL_SPEED
            countdown()

        # =========================
        # WIN
        # =========================
        if left_score >= WIN_SCORE:
            win_screen("PLAYER 1 WINS!")
            break

        if right_score >= WIN_SCORE:
            win_screen("AI WINS!" if mode == 1 else "PLAYER 2 WINS!")
            break

        # =========================
        # UPDATE EFFECTS
        # =========================
        update_particles()

        # =========================
        # DRAW
        # =========================
        screen.fill(BG)

        # trail
        for i, p in enumerate(trail):
            color = (i * 30 % 255, 120, 255 - i * 20)
            pygame.draw.circle(screen, color, p, 4)

        # particles
        for p in particles:
            pygame.draw.circle(screen, p[4], (int(p[0]), int(p[1])), int(p[5]))

        # center net
        for y in range(0, HEIGHT, 20):
            pygame.draw.rect(screen, CYAN, (WIDTH//2, y, 3, 10))

        pygame.draw.rect(screen, PINK, left)
        pygame.draw.rect(screen, BLUE, right)
        pygame.draw.ellipse(screen, CYAN, ball)

        l = SCORE_FONT.render(str(left_score), True, WHITE)
        r = SCORE_FONT.render(str(right_score), True, WHITE)

        screen.blit(l, (WIDTH//4, 20))
        screen.blit(r, (WIDTH*3//4, 20))

        pygame.display.flip()
        clock.tick(60)

pygame.quit()
