FROM node:18-alpine
WORKDIR /app

COPY package*.json ./
# CI 向けに確実なインストール。必要なら --legacy-peer-deps を追加
RUN npm ci --legacy-peer-deps

COPY . .
EXPOSE 3000
CMD ["npm", "run", "dev", "--", "--host"]




#frontend/Dockerfile