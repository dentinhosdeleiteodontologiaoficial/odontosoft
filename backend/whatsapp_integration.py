"""
Módulo de integração com o WhatsApp Bot existente.
Este módulo gerencia a comunicação entre o OdontoSoft e o bot do WhatsApp.
"""

import requests
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional

class WhatsAppIntegration:
    def __init__(self, bot_api_url: str = None, api_key: str = None):
        """
        Inicializa a integração com o WhatsApp Bot.
        
        Args:
            bot_api_url: URL da API do seu bot WhatsApp
            api_key: Chave de API para autenticação (se necessário)
        """
        self.bot_api_url = bot_api_url or "http://localhost:3000"  # URL padrão do seu bot
        self.api_key = api_key
        self.headers = {
            'Content-Type': 'application/json'
        }
        if api_key:
            self.headers['Authorization'] = f'Bearer {api_key}'
    
    def send_message(self, phone: str, message: str) -> Dict:
        """
        Envia uma mensagem via WhatsApp.
        
        Args:
            phone: Número do telefone (formato: 5511999999999)
            message: Mensagem a ser enviada
            
        Returns:
            Dict com o resultado da operação
        """
        try:
            payload = {
                'phone': phone,
                'message': message,
                'timestamp': datetime.now().isoformat()
            }
            
            # Aqui você faria a chamada para a API do seu bot
            # Por enquanto, simulamos o envio
            response = {
                'success': True,
                'message_id': f'msg_{datetime.now().timestamp()}',
                'phone': phone,
                'status': 'sent'
            }
            
            print(f"[WhatsApp] Mensagem enviada para {phone}: {message}")
            return response
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'phone': phone
            }
    
    def send_confirmation_message(self, patient_data: Dict, appointment_data: Dict) -> Dict:
        """
        Envia mensagem de confirmação de consulta.
        
        Args:
            patient_data: Dados do paciente
            appointment_data: Dados do agendamento
            
        Returns:
            Dict com o resultado da operação
        """
        # Determina o telefone para envio (responsável ou paciente)
        phone = patient_data.get('responsible_phone') or patient_data.get('phone')
        name = patient_data.get('responsible_name') or patient_data.get('name')
        
        # Formata a data e hora
        appointment_datetime = datetime.fromisoformat(appointment_data['start_time'])
        formatted_date = appointment_datetime.strftime('%d/%m/%Y')
        formatted_time = appointment_datetime.strftime('%H:%M')
        
        # Monta a mensagem
        message = f"""🦷 *Confirmação de Consulta - Dentinhos de Leite*

Olá {name}! 

Sua consulta está agendada para:
📅 Data: {formatted_date}
🕐 Horário: {formatted_time}

Por favor, confirme sua presença respondendo:
✅ *SIM* - para confirmar
❌ *NÃO* - para cancelar
🔄 *REAGENDAR* - para remarcar

Aguardamos sua confirmação! 😊"""

        return self.send_message(phone, message)
    
    def send_return_reminder(self, patient_data: Dict, return_type: str = "revisão") -> Dict:
        """
        Envia lembrete de retorno.
        
        Args:
            patient_data: Dados do paciente
            return_type: Tipo de retorno (revisão, profilaxia, etc.)
            
        Returns:
            Dict com o resultado da operação
        """
        phone = patient_data.get('responsible_phone') or patient_data.get('phone')
        name = patient_data.get('responsible_name') or patient_data.get('name')
        
        message = f"""🦷 *Lembrete de Retorno - Dentinhos de Leite*

Olá {name}! 

É hora do retorno para {return_type}! 

Para agendar sua consulta:
📞 Entre em contato conosco
💬 Responda esta mensagem
🌐 Acesse nosso site

Cuidar dos dentinhos é muito importante! 😊"""

        return self.send_message(phone, message)
    
    def send_post_appointment_files(self, patient_data: Dict, files: List[str], custom_message: str = None) -> Dict:
        """
        Envia arquivos pós-consulta (PDFs, orientações).
        
        Args:
            patient_data: Dados do paciente
            files: Lista de caminhos dos arquivos
            custom_message: Mensagem personalizada
            
        Returns:
            Dict com o resultado da operação
        """
        phone = patient_data.get('responsible_phone') or patient_data.get('phone')
        name = patient_data.get('responsible_name') or patient_data.get('name')
        
        base_message = custom_message or f"""🦷 *Orientações Pós-Consulta - Dentinhos de Leite*

Olá {name}! 

Seguem as orientações importantes para o cuidado após a consulta.

Por favor, leia com atenção e siga as recomendações.

Qualquer dúvida, estamos à disposição! 😊"""

        # Por enquanto, simulamos o envio de arquivos
        # Na implementação real, você integraria com a API do seu bot para envio de arquivos
        result = self.send_message(phone, base_message)
        
        if result['success']:
            result['files_sent'] = files
            print(f"[WhatsApp] Arquivos enviados: {files}")
        
        return result
    
    def process_incoming_message(self, message_data: Dict) -> Dict:
        """
        Processa mensagens recebidas do WhatsApp.
        
        Args:
            message_data: Dados da mensagem recebida
            
        Returns:
            Dict com a resposta processada
        """
        phone = message_data.get('phone')
        message = message_data.get('message', '').upper().strip()
        
        # Processa respostas de confirmação
        if message in ['SIM', 'S', 'CONFIRMO', 'OK']:
            return {
                'action': 'confirm_appointment',
                'phone': phone,
                'status': 'confirmed'
            }
        elif message in ['NÃO', 'NAO', 'N', 'CANCELO']:
            return {
                'action': 'cancel_appointment',
                'phone': phone,
                'status': 'cancelled'
            }
        elif message in ['REAGENDAR', 'REMARCAR']:
            return {
                'action': 'reschedule_appointment',
                'phone': phone,
                'status': 'reschedule_requested'
            }
        else:
            return {
                'action': 'unknown',
                'phone': phone,
                'message': message
            }
    
    def get_patient_by_phone(self, phone: str) -> Optional[Dict]:
        """
        Busca paciente pelo número de telefone.
        Esta função deve ser implementada para consultar o banco de dados.
        
        Args:
            phone: Número do telefone
            
        Returns:
            Dados do paciente ou None
        """
        # Esta função deve ser implementada para consultar o banco de dados
        # Por enquanto, retorna None
        return None
    
    def update_appointment_status(self, phone: str, status: str) -> bool:
        """
        Atualiza o status de um agendamento baseado no telefone.
        
        Args:
            phone: Número do telefone
            status: Novo status
            
        Returns:
            True se atualizado com sucesso
        """
        # Esta função deve ser implementada para atualizar o banco de dados
        # Por enquanto, retorna True
        print(f"[WhatsApp] Status do agendamento atualizado: {phone} -> {status}")
        return True

# Instância global para uso na aplicação
whatsapp = WhatsAppIntegration()

def configure_whatsapp_integration(bot_url: str, api_key: str = None):
    """
    Configura a integração com o WhatsApp.
    
    Args:
        bot_url: URL da API do bot
        api_key: Chave de API (opcional)
    """
    global whatsapp
    whatsapp = WhatsAppIntegration(bot_url, api_key)

