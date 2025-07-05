import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

// Importe os plugins do PostCSS diretamente
import tailwindcss from 'tailwindcss'
import autoprefixer from 'autoprefixer'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react( )],
  css: {
    postcss: {
      plugins: [
        tailwindcss(), // Chame como função
        autoprefixer(), // Chame como função
      ],
    },
  },
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  build: {
    rollupOptions: {
      // Mantenha esta seção comentada por enquanto.
      // Vamos tentar 'optimizeDeps' primeiro.
      // external: [
      //   '@fullcalendar/react',
      //   '@fullcalendar/daygrid',
      //   '@fullcalendar/timegrid',
      //   '@fullcalendar/interaction',
      //   '@fullcalendar/list',
      //   '@fullcalendar/core/locales/pt-br',
      // ],
    },
  },
  optimizeDeps: {
    // Força o Vite a pré-otimizar e incluir esses módulos.
    // Isso pode resolver problemas de resolução para certas bibliotecas.
    include: [
      '@fullcalendar/react',
      '@fullcalendar/daygrid',
      '@fullcalendar/timegrid',
      '@fullcalendar/interaction',
      '@fullcalendar/list',
      '@fullcalendar/core/locales/pt-br',
    ],
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
