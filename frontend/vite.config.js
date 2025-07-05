import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react( )],
  resolve: {
    alias: {
      // Mantém o alias para o caminho base do projeto (o @/)
      '@': path.resolve(__dirname, './src'),
    },
  },
  // Adiciona uma configuração para otimizar as dependências do FullCalendar
  optimizeDeps: {
    include: [
      '@fullcalendar/react',
      '@fullcalendar/daygrid',
      '@fullcalendar/timegrid',
      '@fullcalendar/interaction',
      '@fullcalendar/list',
      '@fullcalendar/core/locales/pt-br',
    ],
  },
})
