import { defineConfig } from "vite"
import react from "@vitejs/plugin-react"
import adapter from "@sveltejs/adapter-static"

// https://vitejs.dev/config/
export default defineConfig({
  server: {
    port: 3000,
    proxy: {
      "/api": `http://localhost:8000`,
    },
  },
  plugins: [react()],
  kit: {
    adapter: adapter(),
  },
})
