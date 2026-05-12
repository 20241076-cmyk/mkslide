# Week 11 실습

## 오늘 한 것
- PyInstaller 설치 및 빌드
- resource_path() 함수 추가
- --add-data 옵션으로 에셋 포함
- .exe 실행 확인

## resource_path() 를 써야 하는 이유
pyinstaller를 사용하여 빌드된 exe를 실행하면 임시 폴더에 파일을 압축 해제하고, 그 경로를 sys._MEIPASS에 저장한다. 반면 개발 중 vscode나 thonny에서 실행할 때는 sys._MEIPASS가 존재하지 않으며, 대신 file을 기준으로 .py 파일의 위치를 경로로 사용한다. resource_path는 조건문으로 이 두 가지 상황을 구분하여 어느 환경에서든 올바른 경로를 반환하기 때문에 필요한 함수다.

## 빌드 명령어
(오늘 사용한 명령어 기록)

```
pyinstaller --onefile --windowed --add-data "assets;assets" --name=paring_shooter paring_shooter.py
```

## AI 활용 내역
1. PyInstaller로 exe 만드는 방법 질문 → cd로 폴더 이동 후 `pyinstaller --onefile game.py` 실행, dist 폴더에 exe 생성된다고 설명
2. 학교 자료 vs 실제 결과 다름 → `--onefile` 옵션 때문에 dll 없이 exe 하나만 나온 것, 잘못된 게 아니라고 설명
3. 학교 자료 명령어와 내 명령어 차이 → `--windowed`(콘솔창 제거)와 `--name` 옵션 설명
