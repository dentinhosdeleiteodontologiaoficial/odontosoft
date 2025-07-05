import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react( )],
  css: {
    postcss: {
      plugins: [
        require('tailwindcss'), // Use require para o plugin tailwindcss
        require('autoprefixer'), // Autoprefixer é importante para compatibilidade de navegadores
      ],
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
