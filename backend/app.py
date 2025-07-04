from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///odontosoft.db"  # Usando SQLite
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Definição dos modelos de dados
class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=True)
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

    def __repr__(self):
        return f'<Appointment {self.start_time} - {self.patient.name}>'

# Exemplo de endpoint de teste
@app.route('/')
def hello():
    return 'Hello, OdontoSoft Backend!'

@app.route('/patients', methods=['POST'])
def add_patient():
    data = request.get_json()
    new_patient = Patient(name=data['name'], phone=data['phone'], email=data.get('email'))
    db.session.add(new_patient)
    db.session.commit()
    return jsonify({'message': 'Patient added successfully!', 'patient_id': new_patient.id}), 201

@app.route('/patients', methods=['GET'])
def get_patients():
    patients = Patient.query.all()
    output = []
    for patient in patients:
        patient_data = {'id': patient.id, 'name': patient.name, 'phone': patient.phone, 'email': patient.email}
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

    new_appointment = Appointment(patient_id=patient_id, start_time=start_time, end_time=end_time, notes=data.get('notes'))
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
            'notes': appt.notes
        }
        output.append(appointment_data)
    return jsonify({'appointments': output})

if __name__ == '__main__':
    with app.app_context():
        db.create_all() # Cria as tabelas no banco de dados, se não existirem
    app.run(debug=True, host='0.0.0.0')


