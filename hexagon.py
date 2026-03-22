import pygame
import math
import sys
 
# 초기화
pygame.init()
 
# 화면 설정
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("WASD + 방향키 육각형 이동")
 
# 색상
WHITE = (255, 255, 255)
YELLOW = (220, 30, 30)
BLUE = (30, 144, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
 
# 육각형 설정
HEX_RADIUS = 24
SPEED = 5
 
# 노란색 육각형 시작 위치: 화면 중앙에서 왼쪽으로 100픽셀
yellow_x = WIDTH // 2 - 100
yellow_y = HEIGHT // 2
 
# 파란색 육각형 시작 위치: 화면 중앙에서 오른쪽으로 100픽셀
blue_x = WIDTH // 2 + 100
blue_y = HEIGHT // 2
 
# 폰트 설정
font = pygame.font.SysFont("malgungothic", 36)
 
clock = pygame.time.Clock()
 
def draw_hexagon(surface, color, cx, cy, radius):
    """중심 (cx, cy), 반지름 radius인 정육각형을 그립니다."""
    points = []
    for i in range(6):
        angle_deg = 60 * i - 30  # 뾰족한 위쪽 방향
        angle_rad = math.radians(angle_deg)
        px = cx + radius * math.cos(angle_rad)
        py = cy + radius * math.sin(angle_rad)
        points.append((px, py))
    pygame.draw.polygon(surface, color, points)
 
# 메인 루프
while True:
    clock.tick(60)
 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
 
    keys = pygame.key.get_pressed()
 
    # 노란색 육각형: WASD
    if keys[pygame.K_w]:
        yellow_y -= SPEED
    if keys[pygame.K_s]:
        yellow_y += SPEED
    if keys[pygame.K_a]:
        yellow_x -= SPEED
    if keys[pygame.K_d]:
        yellow_x += SPEED
 
    # 파란색 육각형: 방향키
    if keys[pygame.K_UP]:
        blue_y -= SPEED
    if keys[pygame.K_DOWN]:
        blue_y += SPEED
    if keys[pygame.K_LEFT]:
        blue_x -= SPEED
    if keys[pygame.K_RIGHT]:
        blue_x += SPEED
 
    # 화면 경계 처리 - 노란색
    yellow_x = max(HEX_RADIUS, min(WIDTH - HEX_RADIUS, yellow_x))
    yellow_y = max(HEX_RADIUS, min(HEIGHT - HEX_RADIUS, yellow_y))
 
    # 화면 경계 처리 - 파란색
    blue_x = max(HEX_RADIUS, min(WIDTH - HEX_RADIUS, blue_x))
    blue_y = max(HEX_RADIUS, min(HEIGHT - HEX_RADIUS, blue_y))
 
    # 충돌 감지: 두 중심 사이의 거리가 반지름 합보다 작으면 닿은 것
    distance = math.sqrt((yellow_x - blue_x) ** 2 + (yellow_y - blue_y) ** 2)
    is_colliding = distance < HEX_RADIUS * 2
 
    # 그리기
    screen.fill(WHITE)
    draw_hexagon(screen, YELLOW, yellow_x, yellow_y, HEX_RADIUS)
    draw_hexagon(screen, BLUE, blue_x, blue_y, HEX_RADIUS)
 
    # 충돌 시 왼쪽 상단에 "파이썬" 문구 표시
    if is_colliding:
        text = font.render("[허식-무라사키]", True, PURPLE)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, text_rect)
 
    pygame.display.flip()