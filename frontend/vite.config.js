import { defineConfig } from "vite"
import react from "@vitejs/plugin-react"

// https://vitejs.dev/config/
export default defineConfig({
  server: {
    port: 3000,
    proxy: {
      "/api": `http://localhost:8080`,
      "/.well-known": `http://localhost:8080`,
    },
  },
  plugins: [react()],
  build: {
    outDir: "dist",
  },
})
