import pygame
import random
import sys
import math

pygame.init()


def get_korean_font(size):
    candidates = ["malgungothic", "applegothic", "nanumgothic", "notosanscjk"]
    for name in candidates:
        font = pygame.font.SysFont(name, size)
        if font.get_ascent() > 0:
            return font
    return pygame.font.SysFont(None, size)


# ── 기본 설정 ──────────────────────────────────────────
WIDTH, HEIGHT = 1024, 768
FPS           = 60

WHITE  = (255, 255, 255)
BLACK  = (0,   0,   0)
GRAY   = (20,  20,  40)
BLUE   = (50,  150, 255)
RED    = (220, 50,  50)
YELLOW = (240, 220, 0)
GREEN  = (50,  220, 80)

screen   = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")
clock    = pygame.time.Clock()
font     = get_korean_font(32)
font_big = get_korean_font(72)

# ── 상수 ───────────────────────────────────────────────
PLAYER_W, PLAYER_H = 40, 40
ENEMY_W,  ENEMY_H  = 36, 36
BULLET_RADIUS = 12              # 투사체 반지름 (키움)

MAX_ENEMIES      = 8            # 맵 최대 적 수 (5→8)
ENEMY_STOP_Y     = 120          # 적이 멈출 y좌표 (위로 올림)
ATTACK_INTERVAL  = 120          # 공격 주기: 2초 (FPS=60 기준)
NORMAL_LIFE      = 300          # 정상 상태 지속: 5초
BLINK_LIFE       = 120          # 점멸 상태 지속 (300→120, 빠른 점멸)
SPAWN_INTERVAL   = 90           # 적 스폰 간격 (180→90, 1.5초)
ENEMY_MIN_GAP    = 60           # 적 스폰 시 최소 x 간격 (겹침 방지)

BULLET_NORMAL_SPEED  = 7        # 기본 공격 속도 (5→7)
BULLET_RUSH_SPEED    = 13       # 기습 공격 속도 (9→13)
BULLET_REFLECT_SPEED = 10       # 패링 반사 속도 (8→10)
EXPLOSION_SPEED      = 7        # 폭발 투사체 속도 (5→7)

SHIELD_RADIUS    = 38           # 쉴드 반경
PARRY_FRAMES     = 8            # 쉴드를 누른 직후 패링 판정 유효 프레임

# HP 시스템
MAX_HP           = 10
DMG_NORMAL       = 2            # 그냥 피격
DMG_SHIELD       = 1            # 쉴드 피격
DMG_PARRY        = 0            # 패링 성공

# HP바 UI 위치
HP_BAR_X         = WIDTH - 30   # 오른쪽 끝
HP_BAR_BLOCK_W   = 20           # 블록 가로
HP_BAR_BLOCK_H   = 28           # 블록 세로
HP_BAR_GAP       = 4            # 블록 간격
HP_BAR_TOTAL_H   = MAX_HP * (HP_BAR_BLOCK_H + HP_BAR_GAP) - HP_BAR_GAP
HP_BAR_Y         = HEIGHT // 2 - HP_BAR_TOTAL_H // 2  # 화면 세로 중앙

# 타이머 바 (상단 중앙)
TIMER_MAX        = 100 * FPS    # 100초를 프레임으로
TIMER_BAR_W      = 400          # 바 전체 너비
TIMER_BAR_H      = 20           # 바 높이
TIMER_BAR_X      = WIDTH // 2 - TIMER_BAR_W // 2
TIMER_BAR_Y      = 10

# 8방향 폭발 벡터
EIGHT_DIRS = [
    (0, -1), (0, 1), (-1, 0), (1, 0),
    (-0.707, -0.707), (0.707, -0.707),
    (-0.707,  0.707), (0.707,  0.707),
]

# 점멸 색상 순서: 흰→빨→검→빨→흰
BLINK_COLORS = [WHITE, RED, BLACK, RED, WHITE]


# ── 그리기 함수 ────────────────────────────────────────
def draw_player(surf, rect):
    cx = rect.centerx
    pygame.draw.polygon(surf, BLUE, [
        (cx, rect.top),
        (rect.left, rect.bottom),
        (cx, rect.bottom - 8),
        (rect.right, rect.bottom),
    ])
    pygame.draw.rect(surf, YELLOW, (cx - 4, rect.bottom - 10, 8, 10))

def draw_enemy(surf, en):
    """적 딕셔너리를 받아서 상태에 맞는 색으로 그림"""
    rect  = en["rect"]
    cx    = rect.centerx
    color = _get_enemy_color(en)
    pygame.draw.polygon(surf, color, [
        (cx, rect.bottom),
        (rect.left, rect.top),
        (cx, rect.top + 8),
        (rect.right, rect.top),
    ])

def _get_enemy_color(en):
    """적의 현재 상태(점멸 단계)에 따른 색 반환"""
    if not en["blinking"]:
        return RED
    # 점멸: BLINK_LIFE 동안 BLINK_COLORS를 순환
    ratio     = 1.0 - en["blink_timer"] / BLINK_LIFE
    idx       = int(ratio * len(BLINK_COLORS)) % len(BLINK_COLORS)
    return BLINK_COLORS[idx]

def draw_shield(surf, rect, parry_active):
    """쉴드 원 그리기 — 패링 중이면 밝게"""
    cx, cy = rect.centerx, rect.centery
    color  = WHITE if parry_active else (100, 180, 255)
    pygame.draw.circle(surf, color, (cx, cy), SHIELD_RADIUS, 3)

def draw_bullet(surf, b):
    """투사체 딕셔너리를 받아서 원으로 그림"""
    color = b["color"]
    cx    = int(b["x"])
    cy    = int(b["y"])
    pygame.draw.circle(surf, color, (cx, cy), BULLET_RADIUS)

def draw_stars(surf, stars):
    for s in stars:
        pygame.draw.circle(surf, WHITE, (s[0], s[1]), s[2])

def draw_hp_bar(surf, hp):
    """세로 블록 HP바 — 화면 오른쪽 끝, 세로 중앙"""
    for i in range(MAX_HP):
        # 블록은 위에서부터 그리되, HP가 높을수록 위쪽이 채워짐
        block_y = HP_BAR_Y + (MAX_HP - 1 - i) * (HP_BAR_BLOCK_H + HP_BAR_GAP)
        filled  = i < hp
        color   = GREEN if filled else (60, 60, 60)
        pygame.draw.rect(surf, color,
                         (HP_BAR_X, block_y, HP_BAR_BLOCK_W, HP_BAR_BLOCK_H),
                         border_radius=3)
        # 테두리
        pygame.draw.rect(surf, WHITE,
                         (HP_BAR_X, block_y, HP_BAR_BLOCK_W, HP_BAR_BLOCK_H),
                         1, border_radius=3)

def draw_timer_bar(surf, timer):
    """상단 중앙 노란색 타이머 바 — 100초 동안 천천히 닳음"""
    ratio    = timer / TIMER_MAX
    fill_w   = int(TIMER_BAR_W * ratio)
    # 배경 (빈 바)
    pygame.draw.rect(surf, (60, 60, 20),
                     (TIMER_BAR_X, TIMER_BAR_Y, TIMER_BAR_W, TIMER_BAR_H),
                     border_radius=4)
    # 채워진 부분
    if fill_w > 0:
        pygame.draw.rect(surf, YELLOW,
                         (TIMER_BAR_X, TIMER_BAR_Y, fill_w, TIMER_BAR_H),
                         border_radius=4)
    # 테두리
    pygame.draw.rect(surf, WHITE,
                     (TIMER_BAR_X, TIMER_BAR_Y, TIMER_BAR_W, TIMER_BAR_H),
                     1, border_radius=4)

def draw_hud(score, hp, timer):
    screen.blit(font.render(f"Score: {score}", True, WHITE), (10, 10))
    draw_timer_bar(screen, timer)
    draw_hp_bar(screen, hp)


# ── 적 생성 ────────────────────────────────────────────
def make_enemy(existing_enemies):
    """적 딕셔너리 생성 — 기존 적과 x좌표 겹침 방지"""
    for _ in range(50):  # 최대 50번 시도
        x = random.randint(0, WIDTH - ENEMY_W)
        overlap = any(
            abs(x - en["rect"].x) < ENEMY_W + ENEMY_MIN_GAP
            for en in existing_enemies
        )
        if not overlap:
            break
    return {
        "rect":        pygame.Rect(x, -ENEMY_H, ENEMY_W, ENEMY_H),
        "moving":      True,
        "life_timer":  NORMAL_LIFE,
        "blinking":    False,
        "blink_timer": BLINK_LIFE,
        "attack_cd":   ATTACK_INTERVAL,
    }


# ── 투사체 생성 ────────────────────────────────────────
def make_bullet(x, y, dx, dy, speed, color, is_reflected=False):
    length = math.hypot(dx, dy)
    if length == 0:
        length = 1
    return {
        "x":           float(x),
        "y":           float(y),
        "dx":          dx / length,
        "dy":          dy / length,
        "speed":       speed,
        "color":       color,
        "is_reflected": is_reflected,  # 패링 반사 투사체 여부
    }

def make_explosion_bullets(en):
    """적 폭발 시 8방향 투사체 생성"""
    cx = en["rect"].centerx
    cy = en["rect"].centery
    bullets = []
    for dx, dy in EIGHT_DIRS:
        bullets.append(make_bullet(cx, cy, dx, dy, EXPLOSION_SPEED, RED))
    return bullets


# ── 게임 오버 화면 ─────────────────────────────────────
def game_over_screen(score):
    screen.fill((10, 10, 30))
    screen.blit(font_big.render("GAME OVER", True, RED),   (280, 260))
    screen.blit(font.render(f"Score: {score}", True, WHITE), (440, 360))
    screen.blit(font.render("R: Restart   Q: Quit", True, WHITE), (350, 410))
    pygame.display.flip()
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_r: return True
                if e.key == pygame.K_q: pygame.quit(); sys.exit()

def game_clear_screen(score):
    screen.fill((10, 20, 10))
    screen.blit(font_big.render("CLEAR!", True, YELLOW), (330, 260))
    screen.blit(font.render(f"Score: {score}", True, WHITE), (440, 360))
    screen.blit(font.render("R: Restart   Q: Quit", True, WHITE), (350, 410))
    pygame.display.flip()
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_r: return True
                if e.key == pygame.K_q: pygame.quit(); sys.exit()


# ── 메인 ──────────────────────────────────────────────
def main():
    while True:
        _run_game()

def _run_game():
    player      = pygame.Rect(WIDTH // 2 - PLAYER_W // 2, HEIGHT - 100, PLAYER_W, PLAYER_H)
    enemies     = []
    bullets     = []
    score       = 0
    hp          = MAX_HP
    invincible  = 0
    spawn_timer = 0
    timer       = TIMER_MAX     # 100초 카운트다운

    # 쉴드 관련
    shield_active = False
    parry_timer   = 0

    stars = [[random.randint(0, WIDTH), random.randint(0, HEIGHT), random.randint(1, 2)]
             for _ in range(80)]

    while True:
        clock.tick(FPS)

        # ── 이벤트 ──────────────────────────────────────
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()

        # ── 입력 ────────────────────────────────────────
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]  and player.left   > 0:      player.x -= 6
        if keys[pygame.K_RIGHT] and player.right  < WIDTH:  player.x += 6
        if keys[pygame.K_UP]    and player.top    > 0:      player.y -= 6
        if keys[pygame.K_DOWN]  and player.bottom < HEIGHT: player.y += 6

        # 쉴드 입력
        prev_shield   = shield_active
        shield_active = keys[pygame.K_SPACE]

        # 쉴드를 방금 눌렀을 때 → 패링 판정 윈도우 시작
        if shield_active and not prev_shield:
            parry_timer = PARRY_FRAMES
        if parry_timer > 0:
            parry_timer -= 1

        # ── 적 스폰 ──────────────────────────────────────
        spawn_timer += 1
        if spawn_timer >= SPAWN_INTERVAL and len(enemies) < MAX_ENEMIES:
            spawn_timer = 0
            enemies.append(make_enemy(enemies))

        # ── 적 업데이트 ───────────────────────────────────
        new_explosion_bullets = []
        alive_enemies = []

        for en in enemies:
            rect = en["rect"]

            # 이동 단계: ENEMY_STOP_Y까지 내려오기
            if en["moving"]:
                rect.y += 3
                if rect.top >= ENEMY_STOP_Y:
                    rect.top      = ENEMY_STOP_Y
                    en["moving"]  = False

            # 정지 후 생존 타이머
            if not en["moving"]:
                if not en["blinking"]:
                    en["life_timer"] -= 1
                    if en["life_timer"] <= 0:
                        en["blinking"]    = True
                        en["blink_timer"] = BLINK_LIFE
                else:
                    en["blink_timer"] -= 1
                    if en["blink_timer"] <= 0:
                        # 폭발 후 제거
                        new_explosion_bullets += make_explosion_bullets(en)
                        continue  # alive_enemies에 추가하지 않음

                # 공격 (이동 중이 아닐 때만)
                en["attack_cd"] -= 1
                if en["attack_cd"] <= 0:
                    en["attack_cd"] = ATTACK_INTERVAL
                    cx = rect.centerx
                    cy = rect.bottom

                    # 기본 공격 vs 기습 공격 랜덤 선택
                    if random.random() < 0.5:
                        # 기본 공격: 느린 직선 (빨간색)
                        bullets.append(make_bullet(cx, cy, 0, 1, BULLET_NORMAL_SPEED, RED))
                    else:
                        # 기습 공격: 빠른 유도 (노란색) — 발사 시점 방향으로 고정
                        dx = player.centerx - cx
                        dy = player.centery - cy
                        bullets.append(make_bullet(cx, cy, dx, dy, BULLET_RUSH_SPEED, YELLOW))

            alive_enemies.append(en)

        enemies  = alive_enemies

        # ── 투사체 이동 ───────────────────────────────────
        alive_bullets = []
        for b in bullets:
            b["x"] += b["dx"] * b["speed"]
            b["y"] += b["dy"] * b["speed"]
            # 화면 밖으로 나가면 제거
            if 0 <= b["x"] <= WIDTH and 0 <= b["y"] <= HEIGHT:
                alive_bullets.append(b)
        bullets = alive_bullets

        # 폭발 투사체는 이동 처리 후 추가 (튀는 버그 방지)
        bullets += new_explosion_bullets

        # ── 반사 투사체 vs 적 충돌 ───────────────────────
        hit_enemies   = set()
        alive_bullets = []
        for b in bullets:
            if not b["is_reflected"]:
                alive_bullets.append(b)
                continue
            bx, by = int(b["x"]), int(b["y"])
            hit = False
            for ei, en in enumerate(enemies):
                if en["rect"].collidepoint(bx, by):
                    hit_enemies.add(ei)
                    score += 20
                    hit = True
                    break
            if not hit:
                alive_bullets.append(b)

        enemies = [en for i, en in enumerate(enemies) if i not in hit_enemies]
        bullets = alive_bullets

        # ── 투사체 vs 플레이어 충돌 ──────────────────────
        alive_bullets = []
        for b in bullets:
            if b["is_reflected"]:
                alive_bullets.append(b)
                continue
            bx, by = int(b["x"]), int(b["y"])
            # 쉴드와 충돌 판정
            if shield_active:
                px, py = player.centerx, player.centery
                dist   = math.hypot(bx - px, by - py)
                if dist <= SHIELD_RADIUS:
                    if parry_timer > 0:
                        # 패링 성공: 흰색으로 바꿔서 방향 반전, HP 변화 없음
                        alive_bullets.append(make_bullet(
                            bx, by,
                            -b["dx"], -b["dy"],
                            BULLET_REFLECT_SPEED,
                            WHITE,
                            is_reflected=True
                        ))
                    else:
                        # 쉴드 피격: HP -1
                        if invincible <= 0:
                            hp        -= DMG_SHIELD
                            invincible = 60
                            if hp <= 0:
                                if game_over_screen(score): return
                                pygame.quit(); sys.exit()
                    continue
            # 쉴드 없이 플레이어 직접 충돌: HP -2
            if player.collidepoint(bx, by):
                if invincible <= 0:
                    hp        -= DMG_NORMAL
                    invincible = 90
                    if hp <= 0:
                        if game_over_screen(score): return
                        pygame.quit(); sys.exit()
                continue
            alive_bullets.append(b)
        bullets = alive_bullets

        # ── 무적 타이머 ───────────────────────────────────
        if invincible > 0:
            invincible -= 1

        # ── 타이머 감소 및 클리어 판정 ──────────────────────
        timer -= 1
        if timer <= 0:
            if game_clear_screen(score): return
            pygame.quit(); sys.exit()

        # ── 별 이동 ───────────────────────────────────────
        for s in stars:
            s[1] += 1
            if s[1] > HEIGHT:
                s[1] = 0
                s[0] = random.randint(0, WIDTH)

        # ── 렌더링 ────────────────────────────────────────
        screen.fill(GRAY)
        draw_stars(screen, stars)

        for b in bullets:
            draw_bullet(screen, b)

        for en in enemies:
            draw_enemy(screen, en)

        # 플레이어 (무적 중 깜빡임)
        blink = (invincible // 10) % 2 == 0
        if blink:
            draw_player(screen, player)
            if shield_active:
                draw_shield(screen, player, parry_timer > 0)

        draw_hud(score, hp, timer)
        pygame.display.flip()

main()