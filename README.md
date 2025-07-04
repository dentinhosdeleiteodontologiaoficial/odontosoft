# OdontoSoft - Sistema de Gestão Odontológica

Sistema completo de gestão para consultórios de odontopediatria com integração WhatsApp.

## 🚀 Funcionalidades Implementadas

### ✅ Backend (Flask + SQLite)
- **API RESTful** completa com endpoints para:
  - Gestão de pacientes (CRUD)
  - Agendamentos de consultas
  - Orçamentos e controle financeiro
  - Integração com WhatsApp (endpoints preparados)
- **Banco de dados SQLite** com modelos para:
  - Pacientes (com dados do responsável para odontopediatria)
  - Agendamentos
  - Orçamentos e itens de orçamento
- **CORS habilitado** para comunicação com frontend
- **Estrutura preparada** para integração com seu bot WhatsApp existente

### ✅ Frontend (React + Tailwind CSS)
- **Interface moderna e responsiva** inspirada no Simples Dental
- **Dashboard** com métricas importantes:
  - Total de pacientes
  - Consultas agendadas
  - Orçamentos criados
  - Faturamento mensal
- **Gestão de Pacientes**:
  - Cadastro com campos específicos para odontopediatria
  - Lista de pacientes com dados do responsável
- **Agenda de Consultas**:
  - Visualização de agendamentos
  - Status das consultas
  - Botão para enviar confirmações via WhatsApp
- **Controle Financeiro**:
  - Visão geral de orçamentos
  - Controle de recebimentos
- **Integração WhatsApp**:
  - Interface para configurar confirmações automáticas
  - Lembretes de retorno
  - Status da conexão com o bot

## 📁 Estrutura do Projeto

```
odontosoft/
├── backend/
│   ├── venv/                 # Ambiente virtual Python
│   ├── app.py               # Aplicação Flask principal
│   ├── odontosoft.db        # Banco de dados SQLite
│   └── requirements.txt     # Dependências Python
└── frontend/
    ├── src/
    │   ├── App.jsx          # Componente principal
    │   ├── components/      # Componentes UI (shadcn/ui)
    │   └── ...
    ├── package.json         # Dependências Node.js
    └── vite.config.js       # Configuração do Vite
```

## 🛠️ Como Executar

### Backend (Flask)
```bash
cd backend
source venv/bin/activate
python app.py
```
O backend estará disponível em: `http://localhost:5000`

### Frontend (React)
```bash
cd frontend
npm run dev
```
O frontend estará disponível em: `http://localhost:5173`

## 🔗 Endpoints da API

### Pacientes
- `GET /patients` - Listar todos os pacientes
- `POST /patients` - Cadastrar novo paciente
- `GET /patients/<id>` - Obter paciente específico

### Agendamentos
- `GET /appointments` - Listar agendamentos
- `POST /appointments` - Criar novo agendamento

### Orçamentos
- `GET /budgets` - Listar orçamentos
- `POST /budgets` - Criar novo orçamento

### WhatsApp (Preparado para integração)
- `POST /whatsapp/send-message` - Enviar mensagem
- `POST /whatsapp/send-confirmation` - Enviar confirmação de consulta

## 🔄 Próximas Etapas

### Fase 4: Integração com o Chatbot WhatsApp
- [ ] Conectar com seu bot existente via API
- [ ] Implementar coleta de dados do bot para o sistema
- [ ] Configurar envio de mensagens do sistema para o bot

### Fase 5: Sistema de Agendamento e Notificações Automáticas
- [ ] Implementar agendador (cron jobs)
- [ ] Confirmações automáticas 24h antes
- [ ] Lembretes de retorno configuráveis
- [ ] Sistema de notificações

### Funcionalidades Adicionais
- [ ] Prontuário eletrônico
- [ ] Upload de documentos e imagens
- [ ] Criação de anamneses
- [ ] Emissão de notas fiscais (integração com gateway)
- [ ] Relatórios financeiros
- [ ] Sistema de backup

## 🔧 Tecnologias Utilizadas

- **Backend**: Python, Flask, SQLAlchemy, SQLite
- **Frontend**: React, Vite, Tailwind CSS, shadcn/ui
- **Integração**: REST API, CORS
- **Futuro**: WhatsApp Business API, Gateway NF-e

## 📝 Observações Importantes

1. **Isolamento do Bot**: O sistema foi desenvolvido para ser completamente separado do seu bot existente, garantindo que não haja interferência.

2. **Banco de Dados Separado**: Utiliza SQLite próprio, sem afetar os dados do seu bot.

3. **Comunicação via API**: A integração com o bot será feita via chamadas de API, mantendo a independência dos sistemas.

4. **Hospedagem Separada**: Pode ser hospedado em local diferente do seu bot para evitar conflitos de recursos.

## 🚀 Deploy

O sistema está preparado para deploy em plataformas como:
- **Backend**: Render, Heroku, DigitalOcean
- **Frontend**: Vercel, Netlify, Render

Para deploy em produção, será necessário:
1. Configurar variáveis de ambiente
2. Migrar para PostgreSQL (recomendado)
3. Configurar domínio personalizado
4. Implementar SSL/HTTPS

