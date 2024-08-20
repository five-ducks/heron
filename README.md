# Heron

## 프로젝트 개요
이 리포지토리는 프론트엔드와 백엔드 코드를 모두 포함하는 모노리포(Monorepo) 스타일로 관리됩니다.

## 디렉토리 구조
```
Heron/
│
├── frontend/                  # 프론트엔드 애플리케이션
│
├── backend/                   # 백엔드 애플리케이션
│   ├── config/                # Django 프로젝트 설정 파일들
│   ├── friends/               # 친구 관련 기능을 담당하는 Django 앱
│   ├── games/                 # 게임 관련 기능을 담당하는 Django 앱
│   ├── users/                 # 유저 관리 기능을 담당하는 Django 앱
│   ├── Dockerfile             # 백엔드용 Dockerfile
|   ├── docker-entrypoint.sh   # Docker 컨테이너 시작 시 실행되는 스크립트
│   ├── manage.py              # Django 관리 스크립트
│   └── requirements.txt       # 백엔드 패키지 설정
│
├── .env                       # 환경 변수 설정 파일
├── .gitignore                 # Git 에서 무시할 파일 및 디렉토리 목록
├── README.md                  # 리포지토리 설명 파일
└── docker-compose.yml         # Docker Compose 설정 파일
```
