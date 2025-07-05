import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from 'tailwindcss' // Importe tailwindcss
import path from 'path'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react( )], // Remova tailwindcss daqui
  css: {
    postcss: {
      plugins: [tailwindcss()], // Adicione tailwindcss como um plugin PostCSS
    },
  },
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  server: {
    host: '0.0.0.0',
    port: 5173,
    allowedHosts: [
      'all',
      '5173-ix7pxn4xgjiujmuz4q11c-7dcf92b7.manusvm.computer',
      '.manusvm.computer'
    ]
  }
})
