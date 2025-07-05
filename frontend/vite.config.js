import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react( )],
  resolve: {
    alias: {
      // Adiciona aliases para os módulos do FullCalendar
      // Isso ajuda o Vite a encontrar os módulos corretamente
      '@fullcalendar/react': '@fullcalendar/react',
      '@fullcalendar/daygrid': '@fullcalendar/daygrid',
      '@fullcalendar/timegrid': '@fullcalendar/timegrid',
      '@fullcalendar/interaction': '@fullcalendar/interaction',
      '@fullcalendar/list': '@fullcalendar/list',
      '@fullcalendar/core/locales/pt-br': '@fullcalendar/core/locales/pt-br',
      
      // Adiciona alias para o caminho base do projeto (o @/)
      '@': path.resolve(__dirname, './src'),
    },
  },
})
