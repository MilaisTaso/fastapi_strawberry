RUN_CONTEXT ?= docker compose exec app
TARGET ?= src
APP_NAME ?= graphql_fastapi

up: #起動
	docker compose up -d

build: #ビルド
	docker compose build

down: #停止（コンテナ削除）
	docker compose down

destroy: # コンテナ, image, volumeすべて消去
	docker-compose down --rmi all --volumes --remove-orphans

log: # uvicornのログ確認
	docker compose logs -f app

shell: #appコンテナ疎通
	${RUN_CONTEXT} bash

sql: # データベースとの接続
	docker compose exec db bash -c 'psql -U $$POSTGRES_USER -d $$POSTGRES_DB'

revision: # マイグレーションファイルの作成
	${RUN_CONTEXT} poetry run alembic revision --autogenerate -m "${comment}"

restart: down up # コンテナの再起動

lint:	lint-mypy lint-flake8 # linterの実行

format: fmt/.isort fmt/.black # formatterの実行

test: # テストの実行
	poetry run pytest tests/

migrate: # マイグレーションの実行
	${RUN_CONTEXT} poetry run alembic upgrade head

seed: #初期データの挿入
	${RUN_CONTEXT} poetry run python src/databases/seeders/seed.py

# 詳細-------------------------------------
lint-mypy:
	poetry run pyright ${TARGET}

lint-flake8:
	poetry run flake8 ${TARGET}

fmt/.black:
	poetry run black ${TARGET}

fmt/.isort:
	poetry run isort ${TARGET}
