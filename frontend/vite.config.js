import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
    plugins: [react()],
    server: {
        host: true,     // コンテナ内で外部アクセスを許可（0.0.0.0 と同等）
        port: 3000,     // docker-compose.yml の "3000:3000" に合わせる
        proxy: {
            "/api": {
                target: "http://backend:8000", // Compose のサービス名 backend を使う
                changeOrigin: true,
            }
        }
    }
});



//vite.config.js