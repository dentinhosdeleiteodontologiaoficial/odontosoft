from app import db, app # Importa db e app do seu app.py

with app.app_context():
    print("Tentando apagar todas as tabelas do banco de dados (se existirem)...")
    db.drop_all() # Apaga todas as tabelas existentes
    print("Tabelas apagadas.")

    print("Tentando criar todas as tabelas do banco de dados...")
    db.create_all() # Cria todas as tabelas definidas nos modelos
    print("Tabelas criadas ou já existentes.")
