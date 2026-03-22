import pygame
import sys
import random
 
pygame.init()
 
WIDTH, HEIGHT = 1000, 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Circle Dodge Game")
 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE  = (50, 120, 255)
RED   = (220, 50,  50)
 
clock = pygame.time.Clock()
 
# ── 한글 폰트 로드 ────────────────────────────────────────────────
def load_korean_font(size):
    candidates = [
        "malgungothic", "malgun gothic",
        "applegothic",  "apple sd gothic neo",
        "nanumgothic",  "nanum gothic",
        "notosanskr",   "noto sans kr",
        "gulim", "dotum", "batang",
    ]
    for name in candidates:
        try:
            f = pygame.font.SysFont(name, size)
            test = f.render("가", True, (0, 0, 0))
            if test.get_width() > 4:
                return f
        except Exception:
            pass
    return pygame.font.SysFont("arial", size)
 
font     = load_korean_font(28)
font_big = load_korean_font(72)
font_mid = load_korean_font(36)
 
# ── 플레이어 (삼각형) ─────────────────────────────────────────────
PLAYER_SIZE  = WIDTH // 100
player_x     = WIDTH  // 2
player_y     = HEIGHT // 2
PLAYER_SPEED = 4
 
def draw_triangle(surface, color, x, y, size):
    points = [
        (x,          y - size * 2),
        (x - size,   y + size),
        (x + size,   y + size),
    ]
    pygame.draw.polygon(surface, color, points)
 
def triangle_collision(cx, cy, cr, tx, ty, size):
    pts = [
        (tx,        ty - size * 2),
        (tx - size, ty + size),
        (tx + size, ty + size),
    ]
    for px, py in pts:
        if (px - cx) ** 2 + (py - cy) ** 2 < cr ** 2:
            return True
    if (tx - cx) ** 2 + (ty - cy) ** 2 < cr ** 2:
        return True
    return False
 
# ── 원 클래스 ─────────────────────────────────────────────────────
class Circle:
    LIFESPAN = 37
 
    def __init__(self, x, y):
        self.base_radius    = random.randint(20, 70)
        self.max_radius     = self.base_radius * 2.5
        self.current_radius = 1.0
        self.growth         = self.max_radius / self.LIFESPAN
        self.x     = x
        self.y     = y
        self.alive = True
 
    def update(self):
        self.current_radius += self.growth
        if self.current_radius >= self.max_radius:
            self.alive = False
 
    def draw(self, surface):
        r = int(self.current_radius)
        pygame.draw.circle(surface, RED, (int(self.x), int(self.y)), r)
 
# ── 예고 점 (경고 도트) ───────────────────────────────────────────
# 각 항목: {'x': int, 'y': int, 'countdown': int}
# countdown이 0이 되면 실제 Circle로 교체되고 목록에서 제거
WARNING_FRAMES = 30   # 0.5초 (60fps 기준)
 
# ── 게임 상태 ─────────────────────────────────────────────────────
SPAWN_INTERVAL  = 7
GRACE_FRAMES    = 120   # 초반 2초 동안 생성 없음
 
def reset_state():
    global circles, pending, spawn_timer, game_timer
    global score, score_timer, game_over, player_x, player_y
    circles     = []
    pending     = []          # 예고 중인 스폰 목록
    spawn_timer = 0
    game_timer  = 0
    score       = 0
    score_timer = 0
    game_over   = False
    player_x    = WIDTH  // 2
    player_y    = HEIGHT // 2
 
reset_state()
 
# ── 메인 루프 ─────────────────────────────────────────────────────
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_r and game_over:
                reset_state()
 
    if not game_over:
        # 플레이어 이동
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]  or keys[pygame.K_a]: player_x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: player_x += PLAYER_SPEED
        if keys[pygame.K_UP]    or keys[pygame.K_w]: player_y -= PLAYER_SPEED
        if keys[pygame.K_DOWN]  or keys[pygame.K_s]: player_y += PLAYER_SPEED
        player_x = max(PLAYER_SIZE, min(WIDTH  - PLAYER_SIZE, player_x))
        player_y = max(PLAYER_SIZE, min(HEIGHT - PLAYER_SIZE, player_y))
 
        game_timer += 1
 
        # ── 스폰 스케줄링 (초반 2초 + 경고 0.5초 고려) ──────────
        # 실제 원이 등장하길 원하는 시점 = GRACE_FRAMES
        # 예고 점은 그보다 WARNING_FRAMES 앞서 생성되므로
        # pending 생성은 game_timer >= (GRACE_FRAMES - WARNING_FRAMES) 부터
        spawn_timer += 1
        if spawn_timer >= SPAWN_INTERVAL and game_timer >= (GRACE_FRAMES - WARNING_FRAMES):
            px = random.randint(50, WIDTH  - 50)
            py = random.randint(50, HEIGHT - 50)
            pending.append({'x': px, 'y': py, 'countdown': WARNING_FRAMES})
            spawn_timer = 0
 
        # ── 예고 점 카운트다운 → 실제 원으로 전환 ───────────────
        next_pending = []
        for p in pending:
            p['countdown'] -= 1
            if p['countdown'] <= 0:
                circles.append(Circle(p['x'], p['y']))
            else:
                next_pending.append(p)
        pending = next_pending
 
        # ── 원 업데이트 & 소멸 ───────────────────────────────────
        for c in circles:
            c.update()
        circles = [c for c in circles if c.alive]
 
        # ── 충돌 검사 (빨간 원만, 예고 점은 제외) ───────────────
        for c in circles:
            if triangle_collision(c.x, c.y, c.current_radius,
                                  player_x, player_y, PLAYER_SIZE):
                game_over = True
                break
 
        # ── 점수 ─────────────────────────────────────────────────
        score_timer += 1
        if score_timer >= 60:
            score += 1
            score_timer = 0
 
    # ── 렌더링 ───────────────────────────────────────────────────
    screen.fill(WHITE)
 
    # 빨간 원
    for c in circles:
        c.draw(screen)
 
    # 예고 점 (검은색, 반지름 5)
    for p in pending:
        pygame.draw.circle(screen, BLACK, (int(p['x']), int(p['y'])), 5)
 
    # 플레이어 삼각형
    draw_triangle(screen, BLUE, player_x, player_y, PLAYER_SIZE)
 
    # UI
    fps_text   = font.render(f"FPS: {int(clock.get_fps())}", True, BLACK)
    score_text = font.render(f"생존 시간: {score}초", True, BLACK)
    screen.blit(fps_text,   (10, 10))
    screen.blit(score_text, (10, 45))
 
    if game_over:
        over_text = font_big.render("GAME OVER", True, (200, 0, 0))
        sub_text  = font_mid.render(f"생존: {score}초  |  R 키로 재시작", True, BLACK)
        screen.blit(over_text, (WIDTH  // 2 - over_text.get_width() // 2, HEIGHT // 2 - 60))
        screen.blit(sub_text,  (WIDTH  // 2 - sub_text.get_width()  // 2, HEIGHT // 2 + 30))
 
    pygame.display.flip()
    clock.tick(60)
 
pygame.quit()
sys.exit()