# Heron

## 프로젝트 개요
이 리포지토리는 프론트엔드와 백엔드 코드를 모두 포함하는 모노리포(Monorepo) 스타일로 관리됩니다.

## 디렉토리 구조
```
Heron/
│
├── frontend/                  # 프론트엔드 애플리케이션
│   ├── public/                # 정적 파일 (HTML, 이미지 등)
│   ├── src/                   # 소스 코드 (JavaScript, CSS, React/Vue/Angular 등
|   |    ├── core/             # 공통 컴포넌트
|   |    ├── routes/           # 페이지
|   |    ├── components/       # 컴포넌트
│   ├── package.json           # 프론트엔드 패키지 설정
│   ├── Dockerfile             # 프론트엔드용 Dockerfile
|   ├── index.html             # 시작 html 파일  
│   └── .env                   # 프론트엔드 환경 변수 설정 파일
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
