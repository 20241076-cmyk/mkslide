import pygame
import random
import sys
import math
import base64
import io

pygame.init()
pygame.mixer.init()


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

# ── 효과음 로드 ────────────────────────────────────────
def load_sounds():
    sounds = {}
    try:
        sounds["parry"] = pygame.mixer.Sound(
            "assets/sounds/parry.mp3"
        )
    except Exception:
        sounds["parry"] = None
    return sounds

sounds = load_sounds()

# ── 스프라이트 시트 로드 ───────────────────────────────
SHEET_B64 = "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"

_sheet_bytes   = base64.b64decode(SHEET_B64)
_sheet_surface = pygame.image.load(io.BytesIO(_sheet_bytes))
# convert_alpha는 display 초기화 후에 호출해야 하므로 나중에 처리
FRAME_W, FRAME_H   = 32, 39
SPRITE_SCALE       = 2
FRAME_DELAY        = 150
COLS               = 5

def load_player_frames():
    sheet = pygame.image.load(io.BytesIO(base64.b64decode(SHEET_B64))).convert_alpha()
    frames = []
    for i in range(5):
        row, col = divmod(i, COLS)
        rect = pygame.Rect(col * FRAME_W, row * FRAME_H, FRAME_W, FRAME_H)
        frames.append(sheet.subsurface(rect))
    return frames

# ── 상수 ───────────────────────────────────────────────
PLAYER_W, PLAYER_H = 40, 40
ENEMY_W,  ENEMY_H  = 36, 36
BULLET_RADIUS      = 12

MAX_ENEMIES      = 10
ENEMY_STOP_Y     = 120
ATTACK_INTERVAL  = 120
NORMAL_LIFE      = 300
BLINK_LIFE       = 120
SPAWN_INTERVAL   = 90
ENEMY_MIN_GAP    = 60

BULLET_NORMAL_SPEED  = 7
BULLET_RUSH_SPEED    = 13
BULLET_REFLECT_SPEED = 10
EXPLOSION_SPEED      = 7
CAPSULE_SPEED        = BULLET_NORMAL_SPEED // 2   # 회복 캡슐 낙하 속도
CAPSULE_SIZE         = 14                          # 캡슐 정사각형 한 변
CAPSULE_DROP_CHANCE  = 0.05                        # 5% 확률

SHIELD_RADIUS    = 38
PARRY_FRAMES     = 8

# HP 시스템
MAX_HP       = 10
DMG_NORMAL   = 2
DMG_SHIELD   = 1
DMG_CONTACT  = 5           # 적과 직접 충돌 데미지

# HP바 UI (오른쪽)
HP_BAR_X       = WIDTH - 30
HP_BAR_BLOCK_W = 20
HP_BAR_BLOCK_H = 28
HP_BAR_GAP     = 4
HP_BAR_TOTAL_H = MAX_HP * (HP_BAR_BLOCK_H + HP_BAR_GAP) - HP_BAR_GAP
HP_BAR_Y       = HEIGHT // 2 - HP_BAR_TOTAL_H // 2

# 필살기 게이지 (왼쪽) — 블록 하나가 HP 블록 두 개 크기
GAUGE_MAX       = 5
GAUGE_BLOCK_W   = 20
GAUGE_BLOCK_H   = HP_BAR_BLOCK_H * 2 + HP_BAR_GAP   # HP 블록 2개 합친 크기
GAUGE_GAP       = 4
GAUGE_TOTAL_H   = GAUGE_MAX * (GAUGE_BLOCK_H + GAUGE_GAP) - GAUGE_GAP
GAUGE_X         = 10
GAUGE_Y         = HEIGHT // 2 - GAUGE_TOTAL_H // 2

# 타이머 바 (상단 중앙)
TIMER_MAX    = 100 * FPS
TIMER_BAR_W  = 400
TIMER_BAR_H  = 20
TIMER_BAR_X  = WIDTH // 2 - TIMER_BAR_W // 2
TIMER_BAR_Y  = 10

# 8방향 폭발 벡터
EIGHT_DIRS = [
    (0, -1), (0, 1), (-1, 0), (1, 0),
    (-0.707, -0.707), (0.707, -0.707),
    (-0.707,  0.707), (0.707,  0.707),
]

BLINK_COLORS = [WHITE, RED, BLACK, RED, WHITE]


# ── 그리기 함수 ────────────────────────────────────────
def draw_player(surf, rect, frame_index, frames):
    frame = frames[frame_index]
    scaled = pygame.transform.scale(
        frame,
        (FRAME_W * SPRITE_SCALE, FRAME_H * SPRITE_SCALE)
    )
    draw_x = rect.centerx - scaled.get_width() // 2
    draw_y = rect.centery - scaled.get_height() // 2
    surf.blit(scaled, (draw_x, draw_y))

def draw_enemy(surf, en):
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
    if not en["blinking"]:
        return RED
    ratio = 1.0 - en["blink_timer"] / BLINK_LIFE
    idx   = int(ratio * len(BLINK_COLORS)) % len(BLINK_COLORS)
    return BLINK_COLORS[idx]

def draw_shield(surf, rect, parry_active):
    cx, cy = rect.centerx, rect.centery
    color  = WHITE if parry_active else (100, 180, 255)
    pygame.draw.circle(surf, color, (cx, cy), SHIELD_RADIUS, 3)

def draw_bullet(surf, b):
    pygame.draw.circle(surf, b["color"], (int(b["x"]), int(b["y"])), BULLET_RADIUS)

def draw_capsule(surf, cap):
    pygame.draw.rect(surf, GREEN,
                     (int(cap["x"] - CAPSULE_SIZE // 2),
                      int(cap["y"] - CAPSULE_SIZE // 2),
                      CAPSULE_SIZE, CAPSULE_SIZE))
    pygame.draw.rect(surf, WHITE,
                     (int(cap["x"] - CAPSULE_SIZE // 2),
                      int(cap["y"] - CAPSULE_SIZE // 2),
                      CAPSULE_SIZE, CAPSULE_SIZE), 1)

def draw_stars(surf, stars):
    for s in stars:
        pygame.draw.circle(surf, WHITE, (s[0], s[1]), s[2])

def draw_hp_bar(surf, hp):
    """세로 블록 HP바 — 오른쪽 끝, 세로 중앙"""
    for i in range(MAX_HP):
        block_y = HP_BAR_Y + (MAX_HP - 1 - i) * (HP_BAR_BLOCK_H + HP_BAR_GAP)
        color   = GREEN if i < hp else (60, 60, 60)
        pygame.draw.rect(surf, color,
                         (HP_BAR_X, block_y, HP_BAR_BLOCK_W, HP_BAR_BLOCK_H),
                         border_radius=3)
        pygame.draw.rect(surf, WHITE,
                         (HP_BAR_X, block_y, HP_BAR_BLOCK_W, HP_BAR_BLOCK_H),
                         1, border_radius=3)

def draw_gauge_bar(surf, gauge):
    """필살기 게이지 — 왼쪽 끝, 세로 중앙, 아래서부터 파란색으로 채워짐"""
    for i in range(GAUGE_MAX):
        block_y = GAUGE_Y + (GAUGE_MAX - 1 - i) * (GAUGE_BLOCK_H + GAUGE_GAP)
        color   = BLUE if i < gauge else BLACK
        pygame.draw.rect(surf, color,
                         (GAUGE_X, block_y, GAUGE_BLOCK_W, GAUGE_BLOCK_H),
                         border_radius=3)
        pygame.draw.rect(surf, WHITE,
                         (GAUGE_X, block_y, GAUGE_BLOCK_W, GAUGE_BLOCK_H),
                         1, border_radius=3)

def draw_timer_bar(surf, timer):
    ratio  = timer / TIMER_MAX
    fill_w = int(TIMER_BAR_W * ratio)
    pygame.draw.rect(surf, (60, 60, 20),
                     (TIMER_BAR_X, TIMER_BAR_Y, TIMER_BAR_W, TIMER_BAR_H),
                     border_radius=4)
    if fill_w > 0:
        pygame.draw.rect(surf, YELLOW,
                         (TIMER_BAR_X, TIMER_BAR_Y, fill_w, TIMER_BAR_H),
                         border_radius=4)
    pygame.draw.rect(surf, WHITE,
                     (TIMER_BAR_X, TIMER_BAR_Y, TIMER_BAR_W, TIMER_BAR_H),
                     1, border_radius=4)

def draw_hud(score, hp, gauge, timer):
    screen.blit(font.render(f"Score: {score}", True, WHITE), (10, 10))
    draw_timer_bar(screen, timer)
    draw_hp_bar(screen, hp)
    draw_gauge_bar(screen, gauge)


# ── 적 생성 ────────────────────────────────────────────
def make_enemy(existing_enemies):
    for _ in range(50):
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


# ── 투사체 / 캡슐 생성 ─────────────────────────────────
def make_bullet(x, y, dx, dy, speed, color, is_reflected=False):
    length = math.hypot(dx, dy) or 1
    return {
        "x": float(x), "y": float(y),
        "dx": dx / length, "dy": dy / length,
        "speed": speed, "color": color,
        "is_reflected": is_reflected,
    }

def make_explosion_bullets(en):
    cx, cy = en["rect"].centerx, en["rect"].centery
    return [make_bullet(cx, cy, dx, dy, EXPLOSION_SPEED, RED)
            for dx, dy in EIGHT_DIRS]

def make_capsule(x, y):
    return {"x": float(x), "y": float(y)}


# ── 결과 화면 ──────────────────────────────────────────
def game_over_screen(score):
    screen.fill((10, 10, 30))
    screen.blit(font_big.render("GAME OVER", True, RED),    (280, 260))
    screen.blit(font.render(f"Score: {score}", True, WHITE), (440, 360))
    screen.blit(font.render("R: Restart   Q: Quit", True, WHITE), (350, 410))
    pygame.display.flip()
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_r: return True
                if e.key == pygame.K_q: pygame.quit(); sys.exit()

def game_clear_screen(score):
    screen.fill((10, 20, 10))
    screen.blit(font_big.render("CLEAR!", True, YELLOW),    (330, 260))
    screen.blit(font.render(f"Score: {score}", True, WHITE), (440, 360))
    screen.blit(font.render("R: Restart   Q: Quit", True, WHITE), (350, 410))
    pygame.display.flip()
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_r: return True
                if e.key == pygame.K_q: pygame.quit(); sys.exit()

def title_screen():
    font_sub   = get_korean_font(28)
    font_title = get_korean_font(60)
    blink_timer = 0
    blink_show  = True
    stars = [[random.randint(0, WIDTH), random.randint(0, HEIGHT), random.randint(1, 2)]
             for _ in range(80)]

    # 브금 재생
    try:
        pygame.mixer.music.load("assets/sounds/bgm.mp3")
        pygame.mixer.music.play(-1)
    except Exception:
        pass

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    pygame.mixer.music.stop()
                    return
        for s in stars:
            s[1] += 1
            if s[1] > HEIGHT:
                s[1] = 0
                s[0] = random.randint(0, WIDTH)
        blink_timer += clock.tick(60)
        if blink_timer >= 600:
            blink_show  = not blink_show
            blink_timer = 0
        screen.fill(GRAY)
        for s in stars:
            pygame.draw.circle(screen, WHITE, (s[0], s[1]), s[2])
        title_surf = font_title.render("방패의-전선", True, YELLOW)
        screen.blit(title_surf, (WIDTH // 2 - title_surf.get_width() // 2, 260))
        if blink_show:
            space_surf = font_sub.render("SPACE  —  게임 시작", True, WHITE)
            screen.blit(space_surf, (WIDTH // 2 - space_surf.get_width() // 2, 430))
        pygame.display.flip()


# ── 메인 ──────────────────────────────────────────────
def main():
    while True:
        title_screen()
        _run_game()

def _run_game():
    player_frames = load_player_frames()

    # 게임 중 브금 재생
    try:
        pygame.mixer.music.load("assets/sounds/game_bgm.mp3")
        pygame.mixer.music.play(-1)
    except Exception:
        pass

    player      = pygame.Rect(WIDTH // 2 - PLAYER_W // 2, HEIGHT - 100, PLAYER_W, PLAYER_H)
    enemies     = []
    bullets     = []
    capsules    = []           # 회복 캡슐 리스트
    score       = 0
    hp          = MAX_HP
    gauge       = 0            # 필살기 게이지 (0~5)
    invincible  = 0
    spawn_timer = 0
    timer       = TIMER_MAX

    shield_active = False
    parry_timer   = 0
    frame_index   = 2       # 기본 프레임 = 2번 (정면)
    frame_timer   = 0       # 프레임 전환 타이머 (ms)

    stars = [[random.randint(0, WIDTH), random.randint(0, HEIGHT), random.randint(1, 2)]
             for _ in range(80)]

    while True:
        dt = clock.tick(FPS)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()

        # ── 입력 ────────────────────────────────────────
        keys = pygame.key.get_pressed()
        moving_left  = keys[pygame.K_LEFT]  and player.left   > 0
        moving_right = keys[pygame.K_RIGHT] and player.right  < WIDTH
        if moving_left:  player.x -= 6
        if moving_right: player.x += 6
        if keys[pygame.K_UP]   and player.top    > 0:      player.y -= 6
        if keys[pygame.K_DOWN] and player.bottom < HEIGHT: player.y += 6

        # 방향에 따른 프레임 전환
        # 왼쪽: 2→1→0, 멈추면 0→1→2
        # 오른쪽: 2→3→4, 멈추면 4→3→2
        frame_timer += dt
        if frame_timer >= 80:   # 80ms마다 프레임 전환
            frame_timer = 0
            if moving_left and not moving_right:
                if frame_index > 0:
                    frame_index -= 1
            elif moving_right and not moving_left:
                if frame_index < 4:
                    frame_index += 1
            else:
                # 멈춤: 2번으로 복귀
                if frame_index < 2:
                    frame_index += 1
                elif frame_index > 2:
                    frame_index -= 1

        prev_shield   = shield_active
        shield_active = keys[pygame.K_SPACE]
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

            if en["moving"]:
                rect.y += 3
                if rect.top >= ENEMY_STOP_Y:
                    rect.top     = ENEMY_STOP_Y
                    en["moving"] = False

            if not en["moving"]:
                if not en["blinking"]:
                    en["life_timer"] -= 1
                    if en["life_timer"] <= 0:
                        en["blinking"]    = True
                        en["blink_timer"] = BLINK_LIFE
                else:
                    en["blink_timer"] -= 1
                    if en["blink_timer"] <= 0:
                        new_explosion_bullets += make_explosion_bullets(en)
                        continue

                en["attack_cd"] -= 1
                if en["attack_cd"] <= 0:
                    en["attack_cd"] = ATTACK_INTERVAL
                    cx, cy = rect.centerx, rect.bottom
                    if random.random() < 0.5:
                        bullets.append(make_bullet(cx, cy, 0, 1, BULLET_NORMAL_SPEED, RED))
                    else:
                        dx = player.centerx - cx
                        dy = player.centery - cy
                        bullets.append(make_bullet(cx, cy, dx, dy, BULLET_RUSH_SPEED, YELLOW))

            alive_enemies.append(en)

        enemies = alive_enemies

        # ── 주인공 ↔ 적 직접 충돌 ────────────────────────
        contact_hit = set()
        for ei, en in enumerate(enemies):
            if player.colliderect(en["rect"]) and invincible <= 0:
                contact_hit.add(ei)
                hp        -= DMG_CONTACT
                invincible = 90
                score     += 10
                if hp <= 0:
                    if game_over_screen(score): return
                    pygame.quit(); sys.exit()
                break  # 한 프레임에 한 번만

        # 충돌한 적 제거 + 5% 캡슐 드롭
        for ei in contact_hit:
            en = enemies[ei]
            if random.random() < CAPSULE_DROP_CHANCE:
                capsules.append(make_capsule(en["rect"].centerx, en["rect"].centery))
        enemies = [en for i, en in enumerate(enemies) if i not in contact_hit]

        # ── 투사체 이동 ───────────────────────────────────
        alive_bullets = []
        for b in bullets:
            b["x"] += b["dx"] * b["speed"]
            b["y"] += b["dy"] * b["speed"]
            if 0 <= b["x"] <= WIDTH and 0 <= b["y"] <= HEIGHT:
                alive_bullets.append(b)
        bullets = alive_bullets

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
                    hit    = True
                    break
            if not hit:
                alive_bullets.append(b)

        # 패링으로 처치된 적 → 게이지 +1 (최대 5), 5% 캡슐 드롭
        for ei in hit_enemies:
            en = enemies[ei]
            gauge = min(gauge + 1, GAUGE_MAX)
            if random.random() < CAPSULE_DROP_CHANCE:
                capsules.append(make_capsule(en["rect"].centerx, en["rect"].centery))
        enemies = [en for i, en in enumerate(enemies) if i not in hit_enemies]
        bullets = alive_bullets

        # ── 투사체 vs 플레이어 충돌 ──────────────────────
        alive_bullets = []
        for b in bullets:
            if b["is_reflected"]:
                alive_bullets.append(b)
                continue
            bx, by = int(b["x"]), int(b["y"])
            if shield_active:
                px, py = player.centerx, player.centery
                if math.hypot(bx - px, by - py) <= SHIELD_RADIUS:
                    if parry_timer > 0:
                        alive_bullets.append(make_bullet(
                            bx, by, -b["dx"], -b["dy"],
                            BULLET_REFLECT_SPEED, WHITE, is_reflected=True
                        ))
                        if sounds["parry"]:
                            sounds["parry"].stop()
                            sounds["parry"].play()
                    else:
                        if invincible <= 0:
                            hp        -= DMG_SHIELD
                            invincible = 60
                            if hp <= 0:
                                if game_over_screen(score): return
                                pygame.quit(); sys.exit()
                    continue
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

        # ── 캡슐 이동 및 플레이어 획득 ───────────────────
        alive_capsules = []
        for cap in capsules:
            cap["y"] += CAPSULE_SPEED
            if cap["y"] > HEIGHT:
                continue
            cap_rect = pygame.Rect(
                cap["x"] - CAPSULE_SIZE // 2,
                cap["y"] - CAPSULE_SIZE // 2,
                CAPSULE_SIZE, CAPSULE_SIZE
            )
            if player.colliderect(cap_rect):
                hp = min(hp + 1, MAX_HP)   # HP +1, 최대 초과 불가
            else:
                alive_capsules.append(cap)
        capsules = alive_capsules

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

        for cap in capsules:
            draw_capsule(screen, cap)

        for en in enemies:
            draw_enemy(screen, en)

        blink = (invincible // 10) % 2 == 0
        if blink:
            draw_player(screen, player, frame_index, player_frames)
            if shield_active:
                draw_shield(screen, player, parry_timer > 0)

        draw_hud(score, hp, gauge, timer)
        pygame.display.flip()

main()