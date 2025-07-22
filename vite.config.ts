import { defineConfig } from 'vite'

export default defineConfig({
  root: 'templates', // Direktori tempat file index.html berada
  build: {
    outDir: 'dist', // Folder hasil build
    emptyOutDir: true,
  },
})
