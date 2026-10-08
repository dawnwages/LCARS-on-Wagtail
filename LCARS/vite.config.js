import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  // Port 8080 is the origin allowed by the Wagtail backend's CORS settings
  server: { port: 8080 },
  preview: { port: 8080 },
})
