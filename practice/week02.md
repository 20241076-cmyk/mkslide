# week02

## 오늘의 목표
AI에게 명령 내려보기 / 깃 배우기

## 활동내용
1. 제공되는 예시 파일을 AI로 업그레이드하기.
2. 만든 PY 파일을 깃허브에 업로드 하기.

## 시행착오
깃허브를 만들 때 PORTABLE에 익숙지 않아 수업시간 동안 만들지 못하고 나중에 집에서 따로 만들며 복습을 했다.

## 배운 점
기존에는 챗GPT 나 GEMINAI만을 사용하였는데 이번에 교수님의 추천을 받아 클로드를 사용해봤다.
솔직히 처음에는 큰 차이가 있을 것이라 기대하지 않았는데 같은 명령을 내렸을 때 성능적인 차이가 매우 크다는 걸 깨달았다. 이를 통해 AI를 사용할 때는 여러가지 AI를 사용해야 가장 이상적인 답변을 얻을 수 있다는 걸 알 수 있었다.

## 인상적인 질문과 대답

**Q8. 기존 파티클 게임 코드를 더 예쁘게 바꿔줘**

4가지 파티클 모드를 추가했다. Tab 키로 전환 가능하며 각 모드는 다음과 같다.
- 🔥 Firework - 글로우 빛나는 불꽃
- ✨ Sparkle - 반짝이는 빛 입자
- 💨 Smoke - 퍼지는 연기
- ⭐ Star - 회전하는 별 모양

추가로 트레일 효과, 글로우 효과, 무지개 색상, UI 패널(모드/파티클 수/FPS 표시), 반짝이는 배경도 추가됐다. 조작법은 마우스 클릭으로 파티클 생성, Tab으로 모드 변경, C로 전부 지우기, ESC로 종료다.

---

**Q10. 클로드 코드를 사용해보고 싶은데 그건 어떻게 하는거야?**

Claude Code는 터미널에서 코드베이스를 읽고, 명령을 실행하고, 파일을 수정하는 AI 코딩 에이전트다. 단, 무료 플랜에서는 사용할 수 없으며 최소 Pro 구독($20/월) 이상이 필요하다. Windows 설치 방법은 다음과 같다.
1. PowerShell에서 WSL 설치: `wsl --install`
2. WSL 터미널에서 Claude Code 설치: `curl -fsSL https://claude.ai/install.sh | bash`
3. 실행: `claude`
4. 브라우저에서 Pro/Max 계정으로 로그인

---

**Q11. Git 설정 및 GitHub 업로드 방법**

Git Bash를 열고 아래 순서대로 입력하면 된다.
```bash
cd c:/pygame
git init
git config --global user.email "본인이메일@gmail.com"
git config --global user.name "본인이름"
echo # Particle Playground > README.md
git add .
git commit -m "first commit"
git remote add origin https://github.com/20241076-cmyk/mkslide.git
git push -u origin master
```
학교 PC는 관리자 권한이 없어서 일반 설치가 안 되기 때문에 Portable Git을 사용한다.
