# Test Booking System

시험 일정 예약 시스템 API 서버

&nbsp;

## 실행 방법

1. 프로젝트 코드를 GitHub에서 가져옵니다.

   ```
   git clone https://github.com/jvnlee/test_booking_system.git
   ```

2. Docker Desktop을 [설치](https://www.docker.com/)합니다.

   > 이미 설치되어 있다면 스킵하셔도 됩니다.


3. Docker Desktop을 실행합니다.


4. 프로젝트 루트 디렉토리 `/test_booking_system` 에서 아래 커맨드로 앱을 실행합니다.

    ```
    docker compose up -d
    ```

   **정상 실행 중인 모습:**

   ![앱 실행 완료](https://github.com/user-attachments/assets/4560c5d5-69af-46f5-a0eb-4a03e5fe2fa2)

   **실행 관련 참고 사항:**

   - 실행의 용이성을 위해 환경 변수가 담긴 `.env` 파일을 소스 코드에 공개 처리 해두었습니다.
   
   - API 테스트 편의성을 위해 관리자 계정 1개와 시험 일정 데이터를 앱 실행 시점에 주입하도록 했습니다.
   
      > 관리자 계정: username: admin, password: adminpassword
      > 
      > 시험 일정 더미 데이터: 2025-03-01 00시부터 2025-03-31 23시까지 1시간 단위 일정

&nbsp;

## API 문서

### Swagger

위에 안내된 실행 방법대로 앱을 실행한 상태에서 브라우저로 아래 URL에 접속하면 확인 가능합니다.

```
http://localhost:8000/docs
```

![swagger](https://github.com/user-attachments/assets/73b2c3d9-a239-4fba-a581-a5c5a54ed7d1)

&nbsp;

### Postman

API를 직접 실행시켜 테스트할 때 편리하도록 Postman 문서에 모든 성공/실패 케이스에 대한 예시 요청과 응답을 세팅해놓았습니다.

🔗 [관리자 API 문서](https://documenter.getpostman.com/view/20015084/2sAYdkFoAP#bfb54a5a-560f-4372-9746-73b78ddee599)

🔗 [기업 고객 API 문서](https://documenter.getpostman.com/view/20015084/2sAYdkFoAQ)

우측 상단의 `Run in Postman` 버튼을 통해 실행이 가능합니다.

![postman](https://github.com/user-attachments/assets/690e3ee4-728d-4064-bec7-c509f6d38a93)

&nbsp;

## 사용된 기술

- Python 3.13.2

- FastAPI 0.115.8

- PostgresQL 14.17

- Poetry

- SQLAlchemy

- Alembic

- Docker

&nbsp;

## ERD

![erd](https://github.com/user-attachments/assets/842d3c33-2f38-4d72-9458-35212b5d7281)

&nbsp;

## 프로젝트 디렉토리 구조

```
├── alembic             
│   └── versions        # DB 마이그레이션 버전
└── app
    ├── api
    │   └── endpoints   # API 라우터
    ├── core            # 공통 모듈
    ├── db              # DB 관련 설정
    ├── exception       # 예외
    ├── model           # SQLAlchemy 모델
    ├── schema          # Pydantic 스키마
    └── service         # 비즈니스 로직
```
