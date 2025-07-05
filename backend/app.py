# backend/app.py

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_cors import CORS
import os

app = Flask(__name__)

cors_origins = os.environ.get("CORS_ORIGINS", "*").split(',')
CORS(app, resources={r"/*": {"origins": cors_origins}})

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///odontosoft.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "uma_chave_secreta_padrao_muito_insegura")

db = SQLAlchemy(app)

# Definição dos modelos de dados
class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    # REMOVIDO: phone = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=True)
    
    # Campos do Responsável
    responsible_name = db.Column(db.String(100), nullable=True)
    responsible_phone = db.Column(db.String(20), nullable=True)
    responsible_cpf = db.Column(db.String(14), unique=True, nullable=True) # Novo campo para CPF

    # Campos de Endereço
    address_street = db.Column(db.String(255), nullable=True)
    address_number = db.Column(db.String(20), nullable=True)
    address_complement = db.Column(db.String(100), nullable=True)
    address_neighborhood = db.Column(db.String(100), nullable=True)
    address_city = db.Column(db.String(100), nullable=True)
    address_state = db.Column(db.String(2), nullable=True) # UF do estado
    address_zip_code = db.Column(db.String(10), nullable=True) # CEP

    appointments = db.relationship('Appointment', backref='patient', lazy=True)
    budgets = db.relationship('Budget', backref='patient', lazy=True) # Garante o relacionamento com Budget

    def __repr__(self):
        return f'<Patient {self.name}>'

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(50), default='Agendado')
    notes = db.Column(db.Text, nullable=True)
    treatment_type = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return f'<Appointment {self.start_time} - {self.patient.name}>'

class Budget(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    total_value = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default='Pendente')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    patient = db.relationship('Patient', backref='budgets_rel', lazy=True) # Renomeado backref para evitar conflito

    def __repr__(self):
        return f'<Budget {self.id} - {self.description}>'

@app.route('/')
def hello():
    return 'Hello, OdontoSoft Backend!'

@app.route('/patients', methods=['POST'])
def add_patient():
    data = request.get_json()
    new_patient = Patient(
        name=data['name'],
        email=data.get('email'),
        responsible_name=data.get('responsible_name'),
        responsible_phone=data.get('responsible_phone'),
        responsible_cpf=data.get('responsible_cpf'), # Novo campo
        address_street=data.get('address_street'), # Novo campo
        address_number=data.get('address_number'), # Novo campo
        address_complement=data.get('address_complement'), # Novo campo
        address_neighborhood=data.get('address_neighborhood'), # Novo campo
        address_city=data.get('address_city'), # Novo campo
        address_state=data.get('address_state'), # Novo campo
        address_zip_code=data.get('address_zip_code') # Novo campo
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
            # REMOVIDO: 'phone': patient.phone,
            'email': patient.email,
            'responsible_name': patient.responsible_name,
            'responsible_phone': patient.responsible_phone,
            'responsible_cpf': patient.responsible_cpf, # Novo campo
            'address_street': patient.address_street, # Novo campo
            'address_number': patient.address_number, # Novo campo
            'address_complement': patient.address_complement, # Novo campo
            'address_neighborhood': patient.address_neighborhood, # Novo campo
            'address_city': patient.address_city, # Novo campo
            'address_state': patient.address_state, # Novo campo
            'address_zip_code': patient.address_zip_code # Novo campo
        }
        output.append(patient_data)
    return jsonify({'patients': output})

@app.route('/appointments', methods=['POST'])
def add_appointment():
    data = request.get_json()
    patient_id = data['patient_id']
    start_time_str = data['start_time']
    end_time_str = data['end_time']

    start_time = datetime.fromisoformat(start_time_str)
    end_time = datetime.fromisoformat(end_time_str)

    new_appointment = Appointment(
        patient_id=patient_id,
        start_time=start_time,
        end_time=end_time,
        notes=data.get('notes'),
        treatment_type=data.get('treatment_type')
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
            'patient_name': appt.patient.name,
            'start_time': appt.start_time.isoformat(),
            'end_time': appt.end_time.isoformat(),
            'status': appt.status,
            'notes': appt.notes,
            'treatment_type': appt.treatment_type
        }
        output.append(appointment_data)
    return jsonify({'appointments': output})

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

@app.route('/whatsapp/send-confirmation', methods=['POST'])
def send_whatsapp_confirmation():
    data = request.get_json()
    appointment_id = data.get('appointment_id')
    print(f"Simulando envio de confirmação para agendamento {appointment_id} via WhatsApp.")
    return jsonify({'message': f'Confirmação para agendamento {appointment_id} enviada com sucesso (simulado)!'})

@app.route('/whatsapp/send-reminder/<int:patient_id>', methods=['POST'])
def send_whatsapp_reminder(patient_id):
    data = request.get_json()
    return_type = data.get('return_type', 'revisão')
    print(f"Simulando envio de lembrete de retorno para paciente {patient_id} ({return_type}) via WhatsApp.")
    return jsonify({'message': f'Lembrete de retorno para paciente {patient_id} enviado com sucesso (simulado)!'})

@app.route('/automation/pending-confirmations', methods=['GET'])
def get_pending_confirmations():
    appointments = Appointment.query.filter_by(status='Agendado').all()
    output = []
    for appt in appointments:
        output.append({
            'id': appt.id,
            'patient_id': appt.patient_id,
            'patient_name': appt.patient.name,
            'phone': appt.patient.responsible_phone, # Usando o telefone do responsável
            'responsible_phone': appt.patient.responsible_phone
        })
    return jsonify({'appointments': output})

@app.route('/automation/send-all-confirmations', methods=['POST'])
def send_all_confirmations_automation():
    print("Simulando envio de todas as confirmações pendentes.")
    return jsonify({'message': 'Todas as confirmações pendentes enviadas (simulado)!'})

@app.route('/automation/return-reminders', methods=['GET'])
def get_return_reminders():
    days_after = request.args.get('days_after', type=int)
    patients = Patient.query.all()
    output = []
    for patient in patients:
        output.append({
            'id': patient.id,
            'name': patient.name,
            'phone': patient.responsible_phone, # Usando o telefone do responsável
            'responsible_phone': patient.responsible_phone
        })
    return jsonify({'patients': output})

@app.route('/automation/cleanup-logs', methods=['POST'])
def cleanup_logs_automation():
    cutoff_date_str = request.get_json().get('cutoff_date')
    print(f"Simulando limpeza de logs antigos antes de {cutoff_date_str}.")
    return jsonify({'message': 'Limpeza de logs concluída (simulado)!'})

@app.route('/whatsapp/webhook', methods=['POST'])
def whatsapp_webhook():
    data = request.get_json()
    phone = data.get('phone')
    message_text = data.get('message')
    timestamp = data.get('timestamp')

    print(f"Mensagem recebida do WhatsApp: De {phone}, Mensagem: '{message_text}', Tempo: {timestamp}")

    if "SIM" in message_text.upper():
        response_message = "Obrigado por confirmar! Seu agendamento está mantido."
    elif "CANCELAR" in message_text.upper():
        response_message = "Seu agendamento foi cancelado. Entre em contato para reagendar."
    else:
        response_message = "Recebi sua mensagem. Em breve entraremos em contato."
    
    return jsonify({'status': 'success', 'response': response_message}), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0')
