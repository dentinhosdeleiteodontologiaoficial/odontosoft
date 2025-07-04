"""
Sistema de Agendamento Automático para OdontoSoft
Responsável por enviar confirmações, lembretes e outras notificações automáticas.
"""

import schedule
import time
import requests
import logging
from datetime import datetime, timedelta
from typing import List, Dict
import threading
import json
import os

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scheduler.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class OdontoSoftScheduler:
    def __init__(self, api_base_url: str = "http://localhost:5000"):
        """
        Inicializa o agendador do OdontoSoft.
        
        Args:
            api_base_url: URL base da API do OdontoSoft
        """
        self.api_base_url = api_base_url
        self.running = False
        self.thread = None
        
        # Configurações padrão
        self.config = {
            'confirmation_hours_before': 24,  # Horas antes para enviar confirmação
            'reminder_days_after': [30, 90, 180],  # Dias após consulta para lembretes
            'working_hours': {
                'start': 8,  # 8h
                'end': 18    # 18h
            },
            'working_days': [0, 1, 2, 3, 4],  # Segunda a sexta (0=segunda)
            'retry_attempts': 3,
            'retry_delay': 300  # 5 minutos
        }
        
        self.load_config()
        self.setup_schedule()
    
    def load_config(self):
        """Carrega configurações de um arquivo JSON se existir."""
        config_file = 'scheduler_config.json'
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    file_config = json.load(f)
                    self.config.update(file_config)
                logger.info("Configurações carregadas do arquivo")
            except Exception as e:
                logger.error(f"Erro ao carregar configurações: {e}")
    
    def save_config(self):
        """Salva as configurações atuais em um arquivo JSON."""
        try:
            with open('scheduler_config.json', 'w') as f:
                json.dump(self.config, f, indent=2)
            logger.info("Configurações salvas")
        except Exception as e:
            logger.error(f"Erro ao salvar configurações: {e}")
    
    def setup_schedule(self):
        """Configura os agendamentos automáticos."""
        # Confirmações de consulta (diariamente às 9h)
        schedule.every().day.at("09:00").do(self.send_daily_confirmations)
        
        # Lembretes de retorno (diariamente às 10h)
        schedule.every().day.at("10:00").do(self.send_return_reminders)
        
        # Limpeza de logs antigos (semanalmente às 2h de domingo)
        schedule.every().sunday.at("02:00").do(self.cleanup_old_logs)
        
        # Verificação de saúde do sistema (a cada hora)
        schedule.every().hour.do(self.health_check)
        
        logger.info("Agendamentos configurados")
    
    def is_working_time(self) -> bool:
        """Verifica se está dentro do horário de trabalho."""
        now = datetime.now()
        
        # Verifica dia da semana
        if now.weekday() not in self.config['working_days']:
            return False
        
        # Verifica horário
        current_hour = now.hour
        if (current_hour < self.config['working_hours']['start'] or 
            current_hour >= self.config['working_hours']['end']):
            return False
        
        return True
    
    def make_api_request(self, endpoint: str, method: str = 'GET', data: Dict = None) -> Dict:
        """
        Faz uma requisição para a API do OdontoSoft.
        
        Args:
            endpoint: Endpoint da API
            method: Método HTTP
            data: Dados para enviar
            
        Returns:
            Resposta da API
        """
        url = f"{self.api_base_url}{endpoint}"
        headers = {'Content-Type': 'application/json'}
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=30)
            elif method == 'POST':
                response = requests.post(url, headers=headers, json=data, timeout=30)
            else:
                raise ValueError(f"Método {method} não suportado")
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro na requisição para {url}: {e}")
            return {'error': str(e)}
    
    def send_daily_confirmations(self):
        """Envia confirmações de consulta para o dia seguinte."""
        logger.info("Iniciando envio de confirmações diárias")
        
        try:
            # Busca consultas que precisam de confirmação
            response = self.make_api_request('/automation/pending-confirmations')
            
            if 'error' in response:
                logger.error(f"Erro ao buscar confirmações pendentes: {response['error']}")
                return
            
            appointments = response.get('appointments', [])
            
            if not appointments:
                logger.info("Nenhuma confirmação pendente")
                return
            
            logger.info(f"Encontradas {len(appointments)} consultas para confirmação")
            
            # Envia confirmações
            result = self.make_api_request('/automation/send-all-confirmations', 'POST')
            
            if 'error' in result:
                logger.error(f"Erro ao enviar confirmações: {result['error']}")
            else:
                logger.info(f"Confirmações enviadas: {result.get('message', 'Sucesso')}")
                
        except Exception as e:
            logger.error(f"Erro no envio de confirmações diárias: {e}")
    
    def send_return_reminders(self):
        """Envia lembretes de retorno baseados na configuração."""
        logger.info("Iniciando envio de lembretes de retorno")
        
        try:
            # Para cada período configurado, busca pacientes que precisam de lembrete
            for days_after in self.config['reminder_days_after']:
                target_date = datetime.now() - timedelta(days=days_after)
                
                # Busca consultas realizadas na data alvo
                response = self.make_api_request(
                    f'/automation/return-reminders?days_after={days_after}'
                )
                
                if 'error' in response:
                    logger.error(f"Erro ao buscar lembretes para {days_after} dias: {response['error']}")
                    continue
                
                patients = response.get('patients', [])
                
                if patients:
                    logger.info(f"Enviando {len(patients)} lembretes para retorno de {days_after} dias")
                    
                    for patient in patients:
                        # Determina o tipo de retorno baseado no período
                        if days_after <= 30:
                            return_type = "revisão pós-tratamento"
                        elif days_after <= 90:
                            return_type = "consulta de acompanhamento"
                        else:
                            return_type = "revisão semestral"
                        
                        # Envia lembrete
                        result = self.make_api_request(
                            f'/whatsapp/send-reminder/{patient["id"]}',
                            'POST',
                            {'return_type': return_type}
                        )
                        
                        if 'error' in result:
                            logger.error(f"Erro ao enviar lembrete para paciente {patient['id']}: {result['error']}")
                        else:
                            logger.info(f"Lembrete enviado para {patient['name']}")
                        
                        # Pequena pausa entre envios
                        time.sleep(2)
                
        except Exception as e:
            logger.error(f"Erro no envio de lembretes de retorno: {e}")
    
    def cleanup_old_logs(self):
        """Remove logs antigos para economizar espaço."""
        logger.info("Iniciando limpeza de logs antigos")
        
        try:
            # Remove logs de mensagens WhatsApp mais antigos que 90 dias
            cutoff_date = datetime.now() - timedelta(days=90)
            
            response = self.make_api_request(
                '/automation/cleanup-logs',
                'POST',
                {'cutoff_date': cutoff_date.isoformat()}
            )
            
            if 'error' in response:
                logger.error(f"Erro na limpeza de logs: {response['error']}")
            else:
                logger.info(f"Limpeza concluída: {response.get('message', 'Sucesso')}")
                
        except Exception as e:
            logger.error(f"Erro na limpeza de logs: {e}")
    
    def health_check(self):
        """Verifica a saúde do sistema."""
        try:
            response = self.make_api_request('/')
            
            if 'error' in response:
                logger.warning(f"Sistema pode estar com problemas: {response['error']}")
            else:
                logger.debug("Sistema funcionando normalmente")
                
        except Exception as e:
            logger.error(f"Erro na verificação de saúde: {e}")
    
    def run_pending(self):
        """Executa tarefas pendentes do agendador."""
        while self.running:
            try:
                schedule.run_pending()
                time.sleep(60)  # Verifica a cada minuto
            except Exception as e:
                logger.error(f"Erro no loop principal do agendador: {e}")
                time.sleep(60)
    
    def start(self):
        """Inicia o agendador em uma thread separada."""
        if self.running:
            logger.warning("Agendador já está rodando")
            return
        
        self.running = True
        self.thread = threading.Thread(target=self.run_pending, daemon=True)
        self.thread.start()
        logger.info("Agendador iniciado")
    
    def stop(self):
        """Para o agendador."""
        if not self.running:
            logger.warning("Agendador não está rodando")
            return
        
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
        logger.info("Agendador parado")
    
    def get_status(self) -> Dict:
        """Retorna o status atual do agendador."""
        return {
            'running': self.running,
            'next_jobs': [
                {
                    'job': str(job.job_func.__name__),
                    'next_run': job.next_run.isoformat() if job.next_run else None
                }
                for job in schedule.jobs
            ],
            'config': self.config
        }
    
    def update_config(self, new_config: Dict):
        """Atualiza as configurações do agendador."""
        self.config.update(new_config)
        self.save_config()
        logger.info("Configurações atualizadas")
    
    def force_run_job(self, job_name: str) -> Dict:
        """Força a execução de um job específico."""
        jobs = {
            'confirmations': self.send_daily_confirmations,
            'reminders': self.send_return_reminders,
            'cleanup': self.cleanup_old_logs,
            'health_check': self.health_check
        }
        
        if job_name not in jobs:
            return {'error': f'Job {job_name} não encontrado'}
        
        try:
            logger.info(f"Executando job {job_name} manualmente")
            jobs[job_name]()
            return {'message': f'Job {job_name} executado com sucesso'}
        except Exception as e:
            logger.error(f"Erro ao executar job {job_name}: {e}")
            return {'error': str(e)}

# Instância global do agendador
scheduler = OdontoSoftScheduler()

def start_scheduler():
    """Inicia o agendador."""
    scheduler.start()

def stop_scheduler():
    """Para o agendador."""
    scheduler.stop()

def get_scheduler_status():
    """Retorna o status do agendador."""
    return scheduler.get_status()

if __name__ == "__main__":
    # Execução standalone do agendador
    logger.info("Iniciando OdontoSoft Scheduler")
    
    try:
        scheduler.start()
        
        # Mantém o processo rodando
        while True:
            time.sleep(60)
            
    except KeyboardInterrupt:
        logger.info("Parando agendador...")
        scheduler.stop()
        logger.info("Agendador parado")

