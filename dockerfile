# syntax=docker/dockerfile:1.2
FROM python:3.12

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    TZ=Asia/Tokyo \
    PYTHONPATH=/app

WORKDIR /src

# タイムゾーンと依存関係のインストール
RUN apt update -yqq && \
    apt install -y --no-install-recommends \
    build-essential curl ca-certificates \
    file git locales sudo && \
    apt clean && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --no-cache-dir poetry && \
    poetry config virtualenvs.in-project true

# プロジェクトファイルのコピー
COPY pyproject.toml poetry.lock ./

# Poetryを使用した依存関係のインストール
RUN poetry install --no-root