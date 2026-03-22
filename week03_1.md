# Pygame 학습 대화기록
날짜: 2026년 3월 17일

---

## 1. 들여쓰기 오류 해결

**질문:** IndentationError 오류 발생

**오류 내용:**
```
IndentationError: expected an indented block after 'while' statement on line 11
```

**원인 및 해결:**
- `while running:` 아래 코드들의 들여쓰기 누락
- 10번 줄에 불필요한 `3` 삭제

**수정된 코드:**
```python
import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("My First Pygame")
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():       # ← 4칸 들여쓰기
        if event.type == pygame.QUIT:      # ← 8칸 들여쓰기
            running = False                # ← 12칸 들여쓰기
    screen.fill(WHITE)                     # ← 4칸 들여쓰기
    pygame.draw.circle(screen, BLUE, (400, 300), 50)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
```

---

## 2. pygame 설치 오류 해결

**오류 내용:**
```
ModuleNotFoundError: No module named 'pygame'
```

**해결 방법:**
```bash
pip install pygame
```

**Thonny 사용자의 경우:**
1. 상단 메뉴 Tools → Manage packages 클릭
2. 검색창에 `pygame` 입력
3. Install 버튼 클릭

---

## 3. 색상 변경 기능 추가 (빨→노→초→파, 1초마다)

**요청:** 가운데 원이 빨간색→노란색→초록색→파란색 순으로 1초마다 변하게

**코드:**
```python
import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("My First Pygame")
WHITE = (255, 255, 255)
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 30)
running = True

COLORS = [(255,0,0), (255,127,0), (255,255,0), (0,255,0), (0,0,255), (75,0,130), (148,0,211)]
color_index = 0
timer = 0

while running:
    dt = clock.tick(60)
    timer += dt

    if timer >= 1000:
        color_index = (color_index + 1) % len(COLORS)
        timer = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill(WHITE)
    pygame.draw.circle(screen, COLORS[color_index], (400, 300), 50)
    fps_text = font.render(f"FPS: {int(clock.get_fps())}", True, (0,0,0))
    screen.blit(fps_text, (500, 500))
    pygame.display.flip()

pygame.quit()
sys.exit()
```

---

## 4. FPS 표시 추가

**요청:** FPS가 화면에 표시되도록

**추가된 3줄:**
```python
font = pygame.font.SysFont("Arial", 30)                                    # 폰트 준비
fps_text = font.render(f"FPS: {int(clock.get_fps())}", True, (0,0,0))     # FPS 텍스트 생성
screen.blit(fps_text, (10, 10))                                            # 화면에 출력
```

---

## 5. 코드 설명 (초보자용)

| 코드 | 설명 |
|------|------|
| `import pygame` | 게임 만들기 도구 상자를 가져와요 |
| `import sys` | 프로그램 종료 도구를 가져와요 |
| `pygame.init()` | pygame을 켜요. 제일 먼저 실행해야 해요 |
| `pygame.display.set_mode((800, 600))` | 가로 800, 세로 600 창을 만들어요 |
| `pygame.display.set_caption(...)` | 창 제목을 설정해요 |
| `WHITE = (255, 255, 255)` | 흰색을 RGB로 저장해요 |
| `clock = pygame.time.Clock()` | 게임 속도를 조절할 타이머예요 |
| `font = pygame.font.SysFont("Arial", 30)` | FPS 표시할 Arial 폰트를 준비해요 |
| `running = True` | 게임이 켜져 있는지 기억하는 변수예요 |
| `while running:` | running이 True인 동안 무한 반복해요 |
| `pygame.event.get()` | 키보드, 마우스 같은 사용자 행동을 감지해요 |
| `pygame.QUIT` | X버튼을 누르면 running=False로 게임 종료 |
| `screen.fill(WHITE)` | 화면을 흰색으로 채워요 (이전 그림을 지워요) |
| `pygame.draw.circle(...)` | 원을 그려요 |
| `pygame.display.flip()` | 그린 내용을 실제 화면에 표시해요 |
| `clock.tick(60)` | 1초에 최대 60번 반복 (60 FPS) |
| `pygame.quit()` | pygame을 정상 종료해요 |
| `sys.exit()` | 프로그램을 완전히 닫아요 |

---

## 6. screen.fill() 동작 설명

**질문:** 그림이 겹쳐지지 않고 그냥 검게 변하는데?

**설명:**
- pygame은 처음에 화면을 **기본값인 검은색**으로 시작해요
- `screen.fill(WHITE)`를 빼면 흰 배경이 없어서 검은 화면이 보이는 것
- 원이 움직이는 경우에 `fill()`이 없으면 이전 위치의 원이 꼬리처럼 겹쳐 보여요

---

## 7. 색상 자연스럽게 변하기 (선형 보간)

**요청:** 딱딱 끊기지 않고 자연스럽게 색이 변하도록

**핵심 원리 (선형 보간 / lerp):**
```python
t = timer / 1000  # 0.0 ~ 1.0 사이 비율
c1 = COLORS[color_index]
c2 = COLORS[(color_index + 1) % len(COLORS)]
blend = (
    int(c1[0] + (c2[0] - c1[0]) * t),
    int(c1[1] + (c2[1] - c1[1]) * t),
    int(c1[2] + (c2[2] - c1[2]) * t)
)
```

예시 (빨강→주황 전환 중 t=0.5):
- R: 255 + (255-255) × 0.5 = 255
- G: 0 + (127-0) × 0.5 = 63
- B: 0 + (0-0) × 0.5 = 0
- → **(255, 63, 0)** 중간 색!

---

## 8. 원 크기 설정

```python
pygame.draw.circle(screen, blend, (400, 300), 50)
#                                              ^^
#                                           반지름 50
```

- `50` → 기본 크기
- `100` → 2배 크기
- `25` → 절반 크기

---

## 최종 코드

```python
import pygame
import sys
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("My First Pygame")
WHITE = (255, 255, 255)
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 30)
running = True

COLORS = [(255,0,0), (255,127,0), (255,255,0), (0,255,0), (0,0,255), (75,0,130), (148,0,211)]
color_index = 0
timer = 0

while running:
    dt = clock.tick(60)
    timer += dt

    if timer >= 1000:
        color_index = (color_index + 1) % len(COLORS)
        timer = 0

    t = timer / 1000
    c1 = COLORS[color_index]
    c2 = COLORS[(color_index + 1) % len(COLORS)]
    blend = (
        int(c1[0] + (c2[0] - c1[0]) * t),
        int(c1[1] + (c2[1] - c1[1]) * t),
        int(c1[2] + (c2[2] - c1[2]) * t)
    )

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill(WHITE)
    pygame.draw.circle(screen, blend, (400, 300), 50)
    fps_text = font.render(f"FPS: {int(clock.get_fps())}", True, (0,0,0))
    screen.blit(fps_text, (500, 500))
    pygame.display.flip()

pygame.quit()
sys.exit()
```
