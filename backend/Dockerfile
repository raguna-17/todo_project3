# -----------------------------
# build stage
# -----------------------------
FROM python:3.11-slim AS builder

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# ビルドに必要なライブラリ
RUN apt-get update && \
    apt-get install -y build-essential gcc libpq-dev --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# requirements をコピーして wheel を作成
COPY requirements.txt /app/requirements.txt
RUN python -m pip install --upgrade pip
RUN pip wheel -r requirements.txt -w /wheels

# -----------------------------
# final stage
# -----------------------------
FROM python:3.11-slim

# 非 root ユーザー作成
RUN addgroup --system app && adduser --system --ingroup app app

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# requirements のインストール
COPY --from=builder /wheels /wheels
COPY requirements.txt /app/requirements.txt
RUN pip install --no-index --find-links=/wheels -r /app/requirements.txt

# アプリケーションコードをコピー
COPY . /app/

# 作業ディレクトリと pytest cache ディレクトリの権限を app に変更
RUN mkdir -p /tmp/.pytest_cache && chown -R app:app /app /tmp/.pytest_cache

COPY ./entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh
# 作業ユーザーを app に変更
USER app

# expose and run on 3333
EXPOSE 3333


ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["gunicorn", "project.wsgi:application", "--bind", "0.0.0.0:3333", "--workers", "3", "--log-level", "info"]


#backend/Dockerfile