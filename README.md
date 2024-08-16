# Mallard

## 프로젝트 개요
이 리포지토리는 프론트엔드와 백엔드 코드를 모두 포함하는 모노리포(Monorepo) 스타일로 관리됩니다.

## 디렉토리 구조
```
mallard/
│
├── frontend/                  # 프론트엔드 애플리케이션
│   ├── public/                # 정적 파일 (HTML, 이미지 등)
│   ├── src/                   # 소스 코드 (JavaScript, CSS, React/Vue/Angular 등)
│   ├── package.json           # 프론트엔드 패키지 설정
│   ├── Dockerfile             # 프론트엔드용 Dockerfile
│   └── .env                   # 프론트엔드 환경 변수 설정 파일
│
├── backend/                   # 백엔드 애플리케이션
│   ├── myproject/             # Django 또는 Flask 소스 코드
│   ├── manage.py              # Django 관리 스크립트
│   ├── requirements.txt       # 백엔드 패키지 설정
│   ├── Dockerfile             # 백엔드용 Dockerfile
│   └── .env                   # 백엔드 환경 변수 설정 파일
│
├── docs/                      # 프로젝트 문서화 디렉토리
│   ├── README.md              # 리포지토리의 일반 문서화
│   └── API.md                 # API 명세서
│
├── .github/                   # GitHub 설정 파일 및 워크플로우
│   └── workflows/             # GitHub Actions 워크플로우 파일들
│       ├── backend-docker-publish.yml
│       └── frontend-docker-publish.yml
│
├── docker-compose.yml         # Docker Compose 설정 파일
└── README.md                  # 리포지토리 설명 파일
```
