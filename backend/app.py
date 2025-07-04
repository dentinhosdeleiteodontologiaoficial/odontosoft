from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_cors import CORS # Importa a extensão Flask-CORS
import os # Importa o módulo os para acessar variáveis de ambiente

app = Flask(__name__)

# Configuração do CORS
# O Render vai definir a variável de ambiente CORS_ORIGINS.
# Se não estiver definida (ex: em desenvolvimento local sem .env), usará '*' (todas as origens).
# Para produção, você DEVE substituir '*' pela URL do seu frontend no Render.
cors_origins = os.environ.get("CORS_ORIGINS", "*").split(',')
CORS(app, resources={r"/*": {"origins": cors_origins}})

# Configuração do Banco de Dados
# O Render vai definir a variável de ambiente DATABASE_URL para PostgreSQL.
# Se não estiver definida (ex: em desenvolvimento local), usará SQLite.
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///odontosoft.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Configuração da SECRET_KEY (essencial para segurança do Flask)
# O Render vai definir a variável de ambiente SECRET_KEY.
# Se não estiver definida, a aplicação pode não funcionar corretamente ou ser insegura.
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "uma_chave_secreta_padrao_muito_insegura") # Substitua por uma chave forte em produção!

db = SQLAlchemy(app)

# Definição dos modelos de dados
class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=True)
    # Adicione os campos de responsável que você mencionou no frontend
    responsible_name = db.Column(db.String(100), nullable=True)
    responsible_phone = db.Column(db.String(20), nullable=True)
    appointments = db.relationship('Appointment', backref='patient', lazy=True)

    def __repr__(self):
        return f'<Patient {self.name}>'

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(50), default='Agendado') # Ex: Agendado, Confirmado, Cancelado, Compareceu, Faltou
    notes = db.Column(db.Text, nullable=True)
    treatment_type = db.Column(db.String(100), nullable=True) # Adicionado para corresponder ao frontend

    def __repr__(self):
        return f'<Appointment {self.start_time} - {self.patient.name}>'

# Classe Budget (Orçamento) - Adicionada com base na sua documentação
class Budget(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    total_value = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default='Pendente') # Ex: Pendente, Aprovado, Recusado
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # Relacionamento com Patient
    patient = db.relationship('Patient', backref='budgets', lazy=True)

    def __repr__(self):
        return f'<Budget {self.id} - {self.description}>'

# Exemplo de endpoint de teste
@app.route('/')
def hello():
    return 'Hello, OdontoSoft Backend!'

@app.route('/patients', methods=['POST'])
def add_patient():
    data = request.get_json()
    # Incluindo os novos campos para responsável
    new_patient = Patient(
        name=data['name'],
        phone=data['phone'],
        email=data.get('email'),
        responsible_name=data.get('responsible_name'),
        responsible_phone=data.get('responsible_phone')
    )
    db.session.add(new_patient)
    db.session.commit()
    return jsonify({'message': 'Patient added successfully!', 'patient_id': new_patient.id}), 201

@app.route('/patients', methods=['GET'])
def get_patients():
    patients = Patient.query.all()
    output = []
    for patient in patients:
        patient_data = {
            'id': patient.id,
            'name': patient.name,
            'phone': patient.phone,
            'email': patient.email,
            'responsible_name': patient.responsible_name,
            'responsible_phone': patient.responsible_phone
        }
        output.append(patient_data)
    return jsonify({'patients': output})

@app.route('/appointments', methods=['POST'])
def add_appointment():
    data = request.get_json()
    patient_id = data['patient_id']
    start_time_str = data['start_time']
    end_time_str = data['end_time']

    # Convertendo strings para objetos datetime
    start_time = datetime.fromisoformat(start_time_str)
    end_time = datetime.fromisoformat(end_time_str)

    new_appointment = Appointment(
        patient_id=patient_id,
        start_time=start_time,
        end_time=end_time,
        notes=data.get('notes'),
        treatment_type=data.get('treatment_type') # Adicionado
    )
    db.session.add(new_appointment)
    db.session.commit()
    return jsonify({'message': 'Appointment added successfully!', 'appointment_id': new_appointment.id}), 201

@app.route('/appointments', methods=['GET'])
def get_appointments():
    appointments = Appointment.query.all()
    output = []
    for appt in appointments:
        appointment_data = {
            'id': appt.id,
            'patient_id': appt.patient_id,
            'patient_name': appt.patient.name, # Acessando o nome do paciente através do relacionamento
            'start_time': appt.start_time.isoformat(),
            'end_time': appt.end_time.isoformat(),
            'status': appt.status,
            'notes': appt.notes,
            'treatment_type': appt.treatment_type # Adicionado
        }
        output.append(appointment_data)
    return jsonify({'appointments': output})

# Endpoints para Orçamentos (Budgets)
@app.route('/budgets', methods=['POST'])
def add_budget():
    data = request.get_json()
    new_budget = Budget(
        patient_id=data['patient_id'],
        description=data['description'],
        total_value=data['total_value'],
        status=data.get('status', 'Pendente')
    )
    db.session.add(new_budget)
    db.session.commit()
    return jsonify({'message': 'Budget added successfully!', 'budget_id': new_budget.id}), 201

@app.route('/budgets', methods=['GET'])
def get_budgets():
    budgets = Budget.query.all()
    output = []
    for budget in budgets:
        budget_data = {
            'id': budget.id,
            'patient_id': budget.patient_id,
            'patient_name': budget.patient.name,
            'description': budget.description,
            'total_value': budget.total_value,
            'status': budget.status,
            'created_at': budget.created_at.isoformat()
        }
        output.append(budget_data)
    return jsonify({'budgets': output})

# Endpoints de integração com WhatsApp (simulados por enquanto)
# Estes endpoints seriam chamados pelo seu scheduler ou diretamente pelo frontend
@app.route('/whatsapp/send-confirmation', methods=['POST'])
def send_whatsapp_confirmation():
    data = request.get_json()
    appointment_id = data.get('appointment_id')
    
    # Simula o envio de confirmação via WhatsApp
    # Em uma implementação real, você chamaria a lógica do whatsapp_integration.py aqui
    print(f"Simulando envio de confirmação para agendamento {appointment_id} via WhatsApp.")
    return jsonify({'message': f'Confirmação para agendamento {appointment_id} enviada com sucesso (simulado)!'})

@app.route('/whatsapp/send-reminder/<int:patient_id>', methods=['POST'])
def send_whatsapp_reminder(patient_id):
    data = request.get_json()
    return_type = data.get('return_type', 'revisão')
    
    # Simula o envio de lembrete de retorno via WhatsApp
    # Em uma implementação real, você chamaria a lógica do whatsapp_integration.py aqui
    print(f"Simulando envio de lembrete de retorno para paciente {patient_id} ({return_type}) via WhatsApp.")
    return jsonify({'message': f'Lembrete de retorno para paciente {patient_id} enviado com sucesso (simulado)!'})

# Endpoints para automação (chamados pelo scheduler.py)
@app.route('/automation/pending-confirmations', methods=['GET'])
def get_pending_confirmations():
    # Retorna agendamentos que precisam de confirmação (ex: para o dia seguinte)
    # Lógica real: buscar agendamentos com status 'Agendado' para as próximas 24h
    
    # Por enquanto, retorna todos os agendamentos como exemplo
    appointments = Appointment.query.filter_by(status='Agendado').all()
    output = []
    for appt in appointments:
        output.append({
            'id': appt.id,
            'patient_id': appt.patient_id,
            'patient_name': appt.patient.name,
            'start_time': appt.start_time.isoformat(),
            'phone': appt.patient.phone, # Ou responsible_phone
            'responsible_phone': appt.patient.responsible_phone
        })
    return jsonify({'appointments': output})

@app.route('/automation/send-all-confirmations', methods=['POST'])
def send_all_confirmations_automation():
    # Este endpoint seria chamado pelo scheduler para enviar todas as confirmações pendentes
    # Lógica real: iterar sobre agendamentos pendentes e chamar o módulo WhatsApp
    
    # Simula o processo
    print("Simulando envio de todas as confirmações pendentes.")
    return jsonify({'message': 'Todas as confirmações pendentes enviadas (simulado)!'})

@app.route('/automation/return-reminders', methods=['GET'])
def get_return_reminders():
    days_after = request.args.get('days_after', type=int)
    # Lógica real: buscar pacientes que tiveram consulta X dias atrás e precisam de lembrete
    
    # Por enquanto, retorna todos os pacientes como exemplo
    patients = Patient.query.all()
    output = []
    for patient in patients:
        output.append({
            'id': patient.id,
            'name': patient.name,
            'phone': patient.phone,
            'responsible_phone': patient.responsible_phone
        })
    return jsonify({'patients': output})

@app.route('/automation/cleanup-logs', methods=['POST'])
def cleanup_logs_automation():
    cutoff_date_str = request.get_json().get('cutoff_date')
    # Lógica real: limpar logs ou dados antigos no banco de dados
    print(f"Simulando limpeza de logs antigos antes de {cutoff_date_str}.")
    return jsonify({'message': 'Limpeza de logs concluída (simulado)!'})


# Webhook para receber mensagens do WhatsApp (do seu bot externo)
@app.route('/whatsapp/webhook', methods=['POST'])
def whatsapp_webhook():
    data = request.get_json()
    phone = data.get('phone')
    message_text = data.get('message')
    timestamp = data.get('timestamp')

    print(f"Mensagem recebida do WhatsApp: De {phone}, Mensagem: '{message_text}', Tempo: {timestamp}")

    # Aqui você processaria a mensagem (ex: confirmar agendamento, cancelar, etc.)
    # Você pode integrar com a lógica do whatsapp_integration.py aqui
    
    # Exemplo simples de resposta baseada na mensagem
    if "SIM" in message_text.upper():
        response_message = "Obrigado por confirmar! Seu agendamento está mantido."
        # Lógica para atualizar o status do agendamento no DB
    elif "CANCELAR" in message_text.upper():
        response_message = "Seu agendamento foi cancelado. Entre em contato para reagendar."
        # Lógica para atualizar o status do agendamento no DB
    else:
        response_message = "Recebi sua mensagem. Em breve entraremos em contato."
    
    # Em uma aplicação real, você enviaria essa resposta de volta via seu bot WhatsApp
    # Ex: whatsapp_integration.send_message(phone, response_message)
    
    return jsonify({'status': 'success', 'response': response_message}), 200


if __name__ == '__main__':
    with app.app_context():
        db.create_all() # Cria as tabelas no banco de dados, se não existirem
    app.run(debug=True, host='0.0.0.0')

