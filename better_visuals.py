import pygame
import math
import sys
import random

pygame.init()
pygame.mixer.init()

# =========================
# SCREEN
# =========================
WIDTH, HEIGHT = 1200, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("HYPERGALACTIC PSYCHIC TABLE TENNIS 3000")

clock = pygame.time.Clock()

# =========================
# COLORS (COSMIC PALETTE)
# =========================
BG = (5, 2, 15)  # Deep space
WHITE = (240, 240, 240)
CYAN = (0, 255, 255)
PINK = (255, 0, 127)
PURPLE = (138, 43, 226)
GREEN = (0, 255, 100)
ORANGE = (255, 140, 0)
MAGENTA = (255, 0, 255)
BLUE = (0, 150, 255)

# =========================
# FONTS
# =========================
TITLE_FONT = pygame.font.SysFont("Arial", 100, bold=True)
MENU_FONT = pygame.font.SysFont("Arial", 50, bold=True)
SCORE_FONT = pygame.font.SysFont("Arial", 80, bold=True)
SMALL_FONT = pygame.font.SysFont("Arial", 30)

# =========================
# SETTINGS
# =========================
PADDLE_W, PADDLE_H = 18, 140
PADDLE_SPEED = 9

BALL_SIZE = 20

INITIAL_SPEED = 7
SPEED_BOOST = 1.06
MAX_SPEED = 20

WIN_SCORE = 7

# =========================
# PARTICLE SYSTEM
# =========================
particles = []

class Particle:
    def _init_(self, x, y, vx, vy, color, life=30, size=4):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.life = life
        self.max_life = life
        self.size = size
    
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.1  # gravity
        self.life -= 1
    
    def draw(self, surf):
        alpha = int(255 * (self.life / self.max_life))
        fade_color = tuple(max(0, min(255, int(c * (self.life / self.max_life)))) for c in self.color)
        pygame.draw.circle(surf, fade_color, (int(self.x), int(self.y)), self.size)

def create_particles(x, y, color, count=8, speed_range=(1, 4)):
    for _ in range(count):
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(*speed_range)
        vx = math.cos(angle) * speed
        vy = math.sin(angle) * speed
        particles.append(Particle(x, y, vx, vy, color, life=40, size=random.randint(2, 5)))

def update_particles():
    global particles
    for p in particles:
        p.update()
    particles = [p for p in particles if p.life > 0]

def draw_particles(surf):
    for p in particles:
        p.draw(surf)

# =========================
# SOUND DESIGN (COSMIC)
# =========================
def play_sound(kind="hit"):
    if kind == "hit":
        freq = random.randint(700, 900)
        duration = 80
    elif kind == "cheer":
        freq = random.randint(1000, 1200)
        duration = 200
    else:
        freq = 600
        duration = 60
    
    sample_rate = 44100
    n_samples = int(sample_rate * duration / 1000)
    buf = bytearray()
    
    for x in range(n_samples):
        wave_sin = math.sin(2 * math.pi * freq * x / sample_rate)
        wave_cos = math.cos(2 * math.pi * (freq * 0.5) * x / sample_rate)
        combined = int(2000 * (wave_sin * 0.7 + wave_cos * 0.3))
        buf += combined.to_bytes(2, byteorder="little", signed=True)
    
    sound = pygame.mixer.Sound(buffer=buf)
    sound.set_volume(0.25)
    sound.play()

# =========================
# BACKGROUND STARS & NEBULA
# =========================
stars = []
for _ in range(100):
    stars.append({
        'x': random.randint(0, WIDTH),
        'y': random.randint(0, HEIGHT),
        'size': random.randint(1, 3),
        'brightness': random.randint(100, 255),
        'pulse': random.uniform(0, 2 * math.pi)
    })

def draw_background():
    screen.fill(BG)
    
    # Draw stars with pulsing effect
    for i, star in enumerate(stars):
        star['pulse'] += 0.02
        brightness = max(0, min(255, int(150 + 100 * math.sin(star['pulse']))))
        color = (brightness, brightness // 2, brightness)
        pygame.draw.circle(screen, color, (star['x'], star['y']), star['size'])
    
    # Nebula glow effect
    for y in range(0, HEIGHT, 80):
        for x in range(0, WIDTH, 120):
            radius = 60
            color_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(color_surface, (138, 43, 226, 20), (radius, radius), radius)
            screen.blit(color_surface, (x - radius, y - radius))

# =========================
# DRAW PADDLE AURA (PSYCHIC)
# =========================
def draw_paddle_with_aura(paddle, color, aura_color):
    # Outer psychic aura
    for i in range(3, 0, -1):
        alpha = max(0, min(255, int(50 / i)))
        aura_surface = pygame.Surface((paddle.width + i * 4, paddle.height + i * 4), pygame.SRCALPHA)
        pygame.draw.rect(aura_surface, (*aura_color, alpha), (0, 0, paddle.width + i * 4, paddle.height + i * 4))
        screen.blit(aura_surface, (paddle.x - i * 2, paddle.y - i * 2))
    
    # Main paddle
    pygame.draw.rect(screen, color, paddle)
    pygame.draw.rect(screen, WHITE, paddle, 2)  # Border glow

# =========================
# MENU
# =========================
def menu():
    pulse = 0
    while True:
        pulse += 0.05
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 1
                if event.key == pygame.K_2:
                    return 2
        
        draw_background()
        
        # Pulsing title
        title_color = (
            max(0, min(255, int(100 + 155 * math.sin(pulse)))),
            max(0, min(255, int(200 + 55 * math.cos(pulse * 0.7)))),
            255
        )
        title = TITLE_FONT.render("HYPERGALACTIC", True, title_color)
        subtitle = MENU_FONT.render("PSYCHIC TABLE TENNIS 3000", True, MAGENTA)
        
        opt1 = MENU_FONT.render("1 - SOLO MATCH", True, CYAN)
        opt2 = MENU_FONT.render("2 - DUAL COMBAT", True, GREEN)
        info = SMALL_FONT.render("P1: W/S  |  P2: UP/DOWN  |  ESC: QUIT", True, PINK)
        
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 80))
        screen.blit(subtitle, (WIDTH//2 - subtitle.get_width()//2, 180))
        screen.blit(opt1, (WIDTH//2 - opt1.get_width()//2, 320))
        screen.blit(opt2, (WIDTH//2 - opt2.get_width()//2, 400))
        screen.blit(info, (WIDTH//2 - info.get_width()//2, 550))
        
        pygame.display.flip()
        clock.tick(60)

# =========================
# WIN SCREEN
# =========================
def win_screen(text):
    pulse = 0
    while True:
        pulse += 0.08
        
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
        
        draw_background()
        
        # Psychic explosion effect
        create_particles(WIDTH//2, HEIGHT//2, MAGENTA, count=2)
        update_particles()
        draw_particles(screen)
        
        # Pulsing win text
        intensity = max(0, min(255, int(100 + 155 * math.sin(pulse))))
        t = TITLE_FONT.render(text, True, (intensity, 50, 255))
        info = MENU_FONT.render("Press R to Restart", True, WHITE)
        esc = SMALL_FONT.render("ESC to Menu", True, PINK)
        
        screen.blit(t, (WIDTH//2 - t.get_width()//2, 200))
        screen.blit(info, (WIDTH//2 - info.get_width()//2, 380))
        screen.blit(esc, (WIDTH//2 - esc.get_width()//2, 460))
        
        pygame.display.flip()
        clock.tick(60)

# =========================
# COUNTDOWN
# =========================
def countdown(left_score, right_score):
    for txt in ["3", "2", "1", "ENGAGE!"]:
        start = pygame.time.get_ticks()
        while pygame.time.get_ticks() - start < 700:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            draw_background()
            
            # Pulsing countdown
            intensity = max(0, min(255, int(100 + 155 * math.sin((pygame.time.get_ticks() - start) / 100))))
            t = TITLE_FONT.render(txt, True, (intensity, 150, 255))
            screen.blit(t, (WIDTH//2 - t.get_width()//2, HEIGHT//2 - 180))
            
            # Score display
            score = SCORE_FONT.render(f"{left_score}   :   {right_score}", True, WHITE)
            screen.blit(score, (WIDTH//2 - score.get_width()//2, HEIGHT//2))
            
            # Rule
            rule = MENU_FONT.render("First to 7 Psychic Victories!", True, GREEN)
            screen.blit(rule, (WIDTH//2 - rule.get_width()//2, HEIGHT//2 + 120))
            
            pygame.display.flip()
            clock.tick(60)

# =========================
# SPEED CONTROL
# =========================
def increase_speed(vx, vy):
    speed = math.sqrt(vx*2 + vy*2)
    speed = min(speed * SPEED_BOOST, MAX_SPEED)
    angle = math.atan2(vy, vx)
    return math.cos(angle) * speed, math.sin(angle) * speed

# =========================
# MAIN GAME LOOP
# =========================
while True:
    mode = menu()
    
    left = pygame.Rect(30, HEIGHT//2 - PADDLE_H//2, PADDLE_W, PADDLE_H)
    right = pygame.Rect(WIDTH-50, HEIGHT//2 - PADDLE_H//2, PADDLE_W, PADDLE_H)
    
    ball = pygame.Rect(WIDTH//2, HEIGHT//2, BALL_SIZE, BALL_SIZE)
    
    vx, vy = INITIAL_SPEED, INITIAL_SPEED
    
    left_score = 0
    right_score = 0
    
    countdown(left_score, right_score)
    
    running = True
    ball_trail = []
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        keys = pygame.key.get_pressed()
        
        # PLAYER 1
        if keys[pygame.K_w]:
            left.y -= PADDLE_SPEED
        if keys[pygame.K_s]:
            left.y += PADDLE_SPEED
        
        # PLAYER 2 / AI
        if mode == 1:
            ai_speed = 7
            deadzone = 15
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
        
        left.y = max(0, min(HEIGHT - left.height, left.y))
        right.y = max(0, min(HEIGHT - right.height, right.y))
        
        # BALL MOVE
        ball.x += vx
        ball.y += vy
        
        # Ball trail for visual effect
        ball_trail.append((ball.centerx, ball.centery))
        if len(ball_trail) > 20:
            ball_trail.pop(0)
        
        # WALL BOUNCE
        if ball.top <= 0 or ball.bottom >= HEIGHT:
            vy *= -1
            create_particles(ball.centerx, ball.centery, CYAN, count=6)
            play_sound("hit")
        
        # LEFT PADDLE HIT
        if ball.colliderect(left) and vx < 0:
            hit = (ball.centery - left.centery) / (left.height / 2)
            vx = abs(vx)
            vy = hit * 6
            vx, vy = increase_speed(vx, vy)
            create_particles(ball.centerx, ball.centery, PINK, count=12, speed_range=(2, 5))
            play_sound("hit")
        
        # RIGHT PADDLE HIT
        if ball.colliderect(right) and vx > 0:
            hit = (ball.centery - right.centery) / (right.height / 2)
            vx = -abs(vx)
            vy = hit * 6
            vx, vy = increase_speed(vx, vy)
            create_particles(ball.centerx, ball.centery, BLUE, count=12, speed_range=(2, 5))
            play_sound("hit")
        
        # SCORE - RIGHT MISS (LEFT PLAYER SCORES)
        if ball.left <= 0:
            left_score += 1
            create_particles(WIDTH//4, HEIGHT//2, GREEN, count=20, speed_range=(3, 8))
            play_sound("cheer")
            ball.center = (WIDTH//2, HEIGHT//2)
            vx, vy = INITIAL_SPEED, INITIAL_SPEED
            ball_trail = []
            countdown(left_score, right_score)
        
        # SCORE - LEFT MISS (RIGHT PLAYER SCORES)
        if ball.right >= WIDTH:
            right_score += 1
            create_particles(WIDTH*3//4, HEIGHT//2, ORANGE, count=20, speed_range=(3, 8))
            play_sound("cheer")
            ball.center = (WIDTH//2, HEIGHT//2)
            vx, vy = -INITIAL_SPEED, INITIAL_SPEED
            ball_trail = []
            countdown(left_score, right_score)
        
        # WIN CHECK
        if left_score >= WIN_SCORE:
            win_screen("⚡ LEFT PLAYER TRIUMPHS ⚡")
            break
        
        if right_score >= WIN_SCORE:
            if mode == 1:
                win_screen("🤖 AI ACHIEVES PSYCHIC DOMINANCE 🤖")
            else:
                win_screen("⚡ RIGHT PLAYER TRIUMPHS ⚡")
            break
        
        # DRAW EVERYTHING
        draw_background()
        
        # Center line with glow
        for y in range(0, HEIGHT, 25):
            pygame.draw.line(screen, MAGENTA, (WIDTH//2, y), (WIDTH//2, y + 15), 2)
        
        # Ball trail
        for i, (tx, ty) in enumerate(ball_trail):
            alpha_val = int(100 * (i / len(ball_trail)))
            trail_color = (int(255 * (i / len(ball_trail))), 200, 255)
            pygame.draw.circle(screen, trail_color, (int(tx), int(ty)), max(1, int(BALL_SIZE/2 * (1 - i/len(ball_trail)))))
        
        # Draw paddles with aura
        draw_paddle_with_aura(left, PINK, MAGENTA)
        draw_paddle_with_aura(right, BLUE, CYAN)
        
        # Draw ball with glow
        pygame.draw.ellipse(screen, CYAN, ball)
        pygame.draw.ellipse(screen, WHITE, ball, 2)
        
        # Update and draw particles
        update_particles()
        draw_particles(screen)
        
        # Score display with glow
        l = SCORE_FONT.render(str(left_score), True, PINK)
        r = SCORE_FONT.render(str(right_score), True, BLUE)
        
        screen.blit(l, (WIDTH//4 - l.get_width()//2, 30))
        screen.blit(r, (WIDTH*3//4 - r.get_width()//2, 30))
        
        pygame.display.flip()
        clock.tick(60)

pygame.quit()
