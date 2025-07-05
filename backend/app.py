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
    # phone = db.Column(db.String(20), unique=True, nullable=False) # Removido conforme solicitado
    email = db.Column(db.String(100), unique=True, nullable=True)
    responsible_name = db.Column(db.String(100), nullable=False) # Tornando obrigatório
    responsible_
