# 🚀 Guia Completo de Deploy - OdontoSoft

Este documento fornece instruções detalhadas para fazer o deploy do OdontoSoft em produção, garantindo que seu sistema de gestão odontológica funcione de forma estável e segura.

## 📋 Índice

1. [Pré-requisitos](#pré-requisitos)
2. [Preparação do Ambiente](#preparação-do-ambiente)
3. [Deploy do Backend](#deploy-do-backend)
4. [Deploy do Frontend](#deploy-do-frontend)
5. [Configuração do Banco de Dados](#configuração-do-banco-de-dados)
6. [Integração WhatsApp](#integração-whatsapp)
7. [Configuração de Domínio e SSL](#configuração-de-domínio-e-ssl)
8. [Monitoramento e Logs](#monitoramento-e-logs)
9. [Backup e Recuperação](#backup-e-recuperação)
10. [Manutenção](#manutenção)

## 🔧 Pré-requisitos

### Recursos Mínimos Recomendados

**Para uso pessoal (1 usuário):**
- **CPU:** 1 vCore
- **RAM:** 1GB
- **Armazenamento:** 20GB SSD
- **Largura de banda:** 1TB/mês

**Para uso expandido (2-5 usuários):**
- **CPU:** 2 vCores
- **RAM:** 2GB
- **Armazenamento:** 40GB SSD
- **Largura de banda:** 2TB/mês

### Plataformas Recomendadas

1. **Render** (Recomendado para iniciantes)
   - Fácil configuração
   - Deploy automático via Git
   - SSL gratuito
   - Planos a partir de $7/mês

2. **DigitalOcean App Platform**
   - Boa relação custo-benefício
   - Escalabilidade automática
   - Planos a partir de $5/mês

3. **Heroku**
   - Interface amigável
   - Muitos add-ons disponíveis
   - Planos a partir de $7/mês

4. **VPS Próprio** (Para usuários avançados)
   - Controle total
   - Menor custo a longo prazo
   - Requer conhecimento em administração de servidores

## 🏗️ Preparação do Ambiente

### 1. Configuração do Repositório Git

```bash
# Clone o projeto
git clone <seu-repositorio-odontosoft>
cd odontosoft

# Crie branches para produção
git checkout -b production
git push origin production
```

### 2. Variáveis de Ambiente

Crie um arquivo `.env` na raiz do backend:

```bash
# Backend/.env
FLASK_ENV=production
SECRET_KEY=sua_chave_secreta_muito_forte_aqui
DATABASE_URL=postgresql://usuario:senha@host:5432/odontosoft_prod
WHATSAPP_BOT_URL=https://seu-bot-whatsapp.com
WHATSAPP_API_KEY=sua_chave_api_whatsapp
CORS_ORIGINS=https://seu-frontend.com
```

### 3. Configuração do Frontend

Crie um arquivo `.env` na raiz do frontend:

```bash
# Frontend/.env
VITE_API_BASE_URL=https://seu-backend.com
VITE_APP_NAME=OdontoSoft
VITE_APP_VERSION=1.0.0
```

## 🖥️ Deploy do Backend

### Opção 1: Deploy no Render

1. **Conecte seu repositório:**
   - Acesse [render.com](https://render.com)
   - Clique em "New +" → "Web Service"
   - Conecte seu repositório GitHub

2. **Configure o serviço:**
   ```yaml
   # render.yaml (na raiz do projeto)
   services:
     - type: web
       name: odontosoft-backend
       env: python
       buildCommand: cd backend && pip install -r requirements.txt
       startCommand: cd backend && python app.py
       envVars:
         - key: FLASK_ENV
           value: production
         - key: SECRET_KEY
           generateValue: true
         - key: DATABASE_URL
           fromDatabase:
             name: odontosoft-db
             property: connectionString
   
   databases:
     - name: odontosoft-db
       databaseName: odontosoft
       user: odontosoft_user
   ```

3. **Configure as variáveis de ambiente:**
   - No dashboard do Render, vá em "Environment"
   - Adicione todas as variáveis do arquivo `.env`

### Opção 2: Deploy no DigitalOcean

1. **Crie um App:**
   ```yaml
   # .do/app.yaml
   name: odontosoft
   services:
   - name: backend
     source_dir: /backend
     github:
       repo: seu-usuario/odontosoft
       branch: production
     run_command: python app.py
     environment_slug: python
     instance_count: 1
     instance_size_slug: basic-xxs
     envs:
     - key: FLASK_ENV
       value: production
     - key: DATABASE_URL
       value: ${db.DATABASE_URL}
   
   databases:
   - name: db
     engine: PG
     num_nodes: 1
     size: db-s-dev-database
     version: "13"
   ```

### Opção 3: VPS Próprio

```bash
# Conecte ao seu VPS
ssh usuario@seu-servidor.com

# Instale dependências
sudo apt update
sudo apt install python3 python3-pip nginx postgresql postgresql-contrib

# Clone o projeto
git clone <seu-repositorio>
cd odontosoft/backend

# Configure ambiente virtual
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure Gunicorn
pip install gunicorn

# Crie arquivo de serviço
sudo nano /etc/systemd/system/odontosoft.service
```

Conteúdo do arquivo de serviço:

```ini
[Unit]
Description=OdontoSoft Backend
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/odontosoft/backend
Environment="PATH=/home/ubuntu/odontosoft/backend/venv/bin"
ExecStart=/home/ubuntu/odontosoft/backend/venv/bin/gunicorn --workers 3 --bind unix:odontosoft.sock -m 007 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# Inicie o serviço
sudo systemctl start odontosoft
sudo systemctl enable odontosoft
```

## 🌐 Deploy do Frontend

### Opção 1: Netlify

```bash
# Build do projeto
cd frontend
npm run build

# Deploy manual
# Arraste a pasta dist/ para netlify.com

# Deploy automático via Git
# Conecte o repositório no Netlify
# Configure:
# Build command: npm run build
# Publish directory: dist
```

### Opção 2: Vercel

```bash
# Instale Vercel CLI
npm i -g vercel

# Deploy
cd frontend
vercel --prod
```

### Opção 3: Render (Static Site)

```yaml
# render.yaml (adicione ao existente)
services:
  - type: web
    name: odontosoft-frontend
    env: static
    buildCommand: cd frontend && npm install && npm run build
    staticPublishPath: frontend/dist
```

## 🗄️ Configuração do Banco de Dados

### PostgreSQL em Produção

1. **Migração do SQLite para PostgreSQL:**

```python
# migration_script.py
import sqlite3
import psycopg2
import os

def migrate_sqlite_to_postgres():
    # Conectar ao SQLite
    sqlite_conn = sqlite3.connect('odontosoft.db')
    sqlite_cursor = sqlite_conn.cursor()
    
    # Conectar ao PostgreSQL
    postgres_conn = psycopg2.connect(os.environ['DATABASE_URL'])
    postgres_cursor = postgres_conn.cursor()
    
    # Migrar dados das tabelas
    tables = ['patient', 'appointment', 'budget', 'budget_item', 'whats_app_message']
    
    for table in tables:
        # Buscar dados do SQLite
        sqlite_cursor.execute(f"SELECT * FROM {table}")
        rows = sqlite_cursor.fetchall()
        
        # Inserir no PostgreSQL
        if rows:
            placeholders = ','.join(['%s'] * len(rows[0]))
            postgres_cursor.executemany(
                f"INSERT INTO {table} VALUES ({placeholders})",
                rows
            )
    
    postgres_conn.commit()
    print("Migração concluída!")

if __name__ == "__main__":
    migrate_sqlite_to_postgres()
```

2. **Configuração de Backup Automático:**

```bash
#!/bin/bash
# backup_db.sh

DB_NAME="odontosoft"
BACKUP_DIR="/backups"
DATE=$(date +%Y%m%d_%H%M%S)

# Criar backup
pg_dump $DATABASE_URL > $BACKUP_DIR/odontosoft_$DATE.sql

# Manter apenas os últimos 7 backups
find $BACKUP_DIR -name "odontosoft_*.sql" -mtime +7 -delete

echo "Backup criado: odontosoft_$DATE.sql"
```

## 📱 Integração WhatsApp

### 1. Configuração do Bot Existente

Adicione estes endpoints ao seu bot:

```javascript
// bot_integration.js
const express = require('express');
const app = express();

// Endpoint para receber comandos do OdontoSoft
app.post('/api/send-message', async (req, res) => {
    try {
        const { phone, message, type } = req.body;
        
        // Sua lógica de envio aqui
        const result = await sendWhatsAppMessage(phone, message);
        
        res.json({
            success: true,
            message_id: result.id,
            phone: phone
        });
    } catch (error) {
        res.status(500).json({
            success: false,
            error: error.message
        });
    }
});

// Webhook para respostas
app.post('/webhook/whatsapp', (req, res) => {
    const { phone, message } = req.body;
    
    // Enviar para OdontoSoft
    fetch('https://seu-odontosoft-backend.com/whatsapp/webhook', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ phone, message })
    });
    
    res.json({ status: 'received' });
});
```

### 2. Configuração no OdontoSoft

```bash
# Configure a integração
curl -X POST https://seu-backend.com/whatsapp/configure \
  -H "Content-Type: application/json" \
  -d '{
    "bot_url": "https://seu-bot.com/api",
    "api_key": "sua_chave_api"
  }'
```

## 🔒 Configuração de Domínio e SSL

### 1. Configuração de Domínio

```bash
# Configure DNS (exemplo com Cloudflare)
# A record: backend.seudominio.com → IP_DO_BACKEND
# A record: app.seudominio.com → IP_DO_FRONTEND
# CNAME: www.seudominio.com → app.seudominio.com
```

### 2. SSL com Let's Encrypt (VPS)

```bash
# Instale Certbot
sudo apt install certbot python3-certbot-nginx

# Obtenha certificados
sudo certbot --nginx -d app.seudominio.com -d backend.seudominio.com

# Configure renovação automática
sudo crontab -e
# Adicione: 0 12 * * * /usr/bin/certbot renew --quiet
```

### 3. Configuração Nginx

```nginx
# /etc/nginx/sites-available/odontosoft
server {
    listen 80;
    server_name backend.seudominio.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl;
    server_name backend.seudominio.com;
    
    ssl_certificate /etc/letsencrypt/live/backend.seudominio.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/backend.seudominio.com/privkey.pem;
    
    location / {
        include proxy_params;
        proxy_pass http://unix:/home/ubuntu/odontosoft/backend/odontosoft.sock;
    }
}
```

## 📊 Monitoramento e Logs

### 1. Configuração de Logs

```python
# logging_config.py
import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logging(app):
    if not app.debug:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        
        file_handler = RotatingFileHandler(
            'logs/odontosoft.log', 
            maxBytes=10240000, 
            backupCount=10
        )
        
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('OdontoSoft startup')
```

### 2. Monitoramento com Uptime Robot

```bash
# Configure monitoramento em:
# https://uptimerobot.com

# URLs para monitorar:
# https://seu-backend.com/
# https://seu-frontend.com/
# https://seu-bot.com/health
```

### 3. Alertas por Email

```python
# email_alerts.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_alert(subject, message):
    msg = MIMEMultipart()
    msg['From'] = "alerts@seudominio.com"
    msg['To'] = "seu@email.com"
    msg['Subject'] = subject
    
    msg.attach(MIMEText(message, 'plain'))
    
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("alerts@seudominio.com", "sua_senha")
    server.send_message(msg)
    server.quit()
```

## 💾 Backup e Recuperação

### 1. Script de Backup Completo

```bash
#!/bin/bash
# full_backup.sh

BACKUP_DIR="/backups/$(date +%Y%m%d)"
mkdir -p $BACKUP_DIR

# Backup do banco de dados
pg_dump $DATABASE_URL > $BACKUP_DIR/database.sql

# Backup dos arquivos de configuração
cp /home/ubuntu/odontosoft/backend/.env $BACKUP_DIR/
cp /home/ubuntu/odontosoft/backend/scheduler_config.json $BACKUP_DIR/

# Backup dos logs
tar -czf $BACKUP_DIR/logs.tar.gz /home/ubuntu/odontosoft/backend/logs/

# Upload para cloud storage (opcional)
# aws s3 sync $BACKUP_DIR s3://seu-bucket/backups/$(date +%Y%m%d)/

echo "Backup completo criado em $BACKUP_DIR"
```

### 2. Script de Recuperação

```bash
#!/bin/bash
# restore.sh

BACKUP_DATE=$1
BACKUP_DIR="/backups/$BACKUP_DATE"

if [ ! -d "$BACKUP_DIR" ]; then
    echo "Backup não encontrado: $BACKUP_DIR"
    exit 1
fi

# Restaurar banco de dados
psql $DATABASE_URL < $BACKUP_DIR/database.sql

# Restaurar configurações
cp $BACKUP_DIR/.env /home/ubuntu/odontosoft/backend/
cp $BACKUP_DIR/scheduler_config.json /home/ubuntu/odontosoft/backend/

# Reiniciar serviços
sudo systemctl restart odontosoft

echo "Restauração concluída"
```

## 🔧 Manutenção

### 1. Atualizações Automáticas

```bash
#!/bin/bash
# update.sh

cd /home/ubuntu/odontosoft

# Backup antes da atualização
./full_backup.sh

# Atualizar código
git pull origin production

# Atualizar dependências backend
cd backend
source venv/bin/activate
pip install -r requirements.txt

# Atualizar dependências frontend
cd ../frontend
npm install
npm run build

# Reiniciar serviços
sudo systemctl restart odontosoft
sudo systemctl reload nginx

echo "Atualização concluída"
```

### 2. Monitoramento de Performance

```python
# performance_monitor.py
import psutil
import requests
import time
from datetime import datetime

def check_system_health():
    # CPU
    cpu_percent = psutil.cpu_percent(interval=1)
    
    # Memória
    memory = psutil.virtual_memory()
    
    # Disco
    disk = psutil.disk_usage('/')
    
    # Verificar se API está respondendo
    try:
        response = requests.get('https://seu-backend.com/', timeout=10)
        api_status = response.status_code == 200
    except:
        api_status = False
    
    # Log do status
    status = {
        'timestamp': datetime.now().isoformat(),
        'cpu_percent': cpu_percent,
        'memory_percent': memory.percent,
        'disk_percent': disk.percent,
        'api_status': api_status
    }
    
    print(f"Status: {status}")
    
    # Alertas
    if cpu_percent > 80:
        send_alert("CPU Alta", f"CPU em {cpu_percent}%")
    
    if memory.percent > 80:
        send_alert("Memória Alta", f"Memória em {memory.percent}%")
    
    if not api_status:
        send_alert("API Offline", "API não está respondendo")

if __name__ == "__main__":
    while True:
        check_system_health()
        time.sleep(300)  # Verifica a cada 5 minutos
```

### 3. Limpeza Automática

```bash
#!/bin/bash
# cleanup.sh

# Limpar logs antigos
find /home/ubuntu/odontosoft/backend/logs/ -name "*.log" -mtime +30 -delete

# Limpar backups antigos
find /backups/ -type d -mtime +30 -exec rm -rf {} +

# Limpar cache do sistema
sudo apt autoremove -y
sudo apt autoclean

echo "Limpeza concluída"
```

## 🚨 Troubleshooting

### Problemas Comuns

1. **Erro 502 Bad Gateway**
   ```bash
   # Verificar se o serviço está rodando
   sudo systemctl status odontosoft
   
   # Verificar logs
   sudo journalctl -u odontosoft -f
   ```

2. **Banco de dados não conecta**
   ```bash
   # Verificar variáveis de ambiente
   echo $DATABASE_URL
   
   # Testar conexão
   psql $DATABASE_URL -c "SELECT 1;"
   ```

3. **WhatsApp não envia mensagens**
   ```bash
   # Verificar configuração
   curl -X GET https://seu-backend.com/whatsapp/config
   
   # Testar envio manual
   curl -X POST https://seu-backend.com/whatsapp/send-message \
     -H "Content-Type: application/json" \
     -d '{"phone": "5511999999999", "message": "Teste"}'
   ```

## 📞 Suporte

Para suporte técnico:

1. Verifique os logs primeiro
2. Consulte a documentação
3. Teste em ambiente local
4. Verifique conectividade de rede
5. Confirme configurações de ambiente

## 🎯 Próximos Passos

Após o deploy bem-sucedido:

1. Configure monitoramento completo
2. Implemente backup automático
3. Configure alertas
4. Teste recuperação de desastres
5. Documente procedimentos operacionais
6. Treine usuários finais

---

**Nota:** Este guia assume conhecimento básico de administração de sistemas. Para usuários iniciantes, recomenda-se começar com plataformas como Render ou Netlify que simplificam o processo de deploy.

