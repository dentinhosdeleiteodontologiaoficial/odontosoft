import os
from app import app, db # Importa a instância do app e db do seu app.py

with app.app_context():
    print("Tentando criar todas as tabelas do banco de dados...")
    db.create_all()
    print("Tabelas criadas ou já existentes.")
