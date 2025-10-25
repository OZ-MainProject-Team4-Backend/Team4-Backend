# 베이스 이미지
FROM python:3.12-slim

# 환경 변수
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PATH="/root/.local/bin:${PATH}"

# 기본 패키지 설치 + psycopg2 의존성 추가
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# uv 설치 (패키지 관리 도구)
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV UV_PYTHON=3.12

# 작업 디렉토리 설정
WORKDIR /AWS

# 의존성 파일 복사 및 설치
COPY pyproject.toml ./
RUN uv sync --all-packages

# 앱 코드 복사
COPY . .

# 환경 변수 등록
ARG SECRET_KEY
ENV SECRET_KEY=${SECRET_KEY}
ENV DJANGO_SETTINGS_MODULE=AWS.settings

# 포트 개방
EXPOSE 8000

# Django 실행 (gunicorn)
CMD ["uv", "run", "gunicorn", "AWS.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
