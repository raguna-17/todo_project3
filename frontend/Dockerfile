FROM node:18-alpine AS frontend-build
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm ci --legacy-peer-deps
COPY frontend/ .
RUN npm run build

### python runtime stage (Django)
FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app
# 必要なら apt パッケージを追加（例: build deps）
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential git curl && rm -rf /var/lib/apt/lists/*

# 依存関係
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリコードをコピー
COPY . .

# frontend のビルド成果物を Django プロジェクトにコピー
# （ビルド済み index.html と assets が /app/frontend/dist に置かれる）
COPY --from=frontend-build /app/frontend/dist /app/frontend/dist

# collectstatic 用フォルダを作成
RUN mkdir -p /vol/static

# エントリポイント、権限付与
COPY deploy/entrypoint.sh /app/deploy/entrypoint.sh
RUN chmod +x /app/deploy/entrypoint.sh

EXPOSE 3333
CMD ["/app/deploy/entrypoint.sh"]
#frontend/Dockerfile