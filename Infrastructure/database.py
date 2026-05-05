from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from config import DATABASE_URL
from Domain.Base import Base

engine = create_engine(
	DATABASE_URL,
	connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
	echo=True  # Mostra as consultas SQL
)

SessionLocal = sessionmaker(
	autocommit=False,
	autoflush=False,
	bind=engine
)

def get_db() -> Session:
	# fornece uma sessão para cada operação
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()

def init_db():
	# Cria todas as tabelas no banco de dados
	#todo EXECUTAR ISSO APENAS UMA VEZ QUANDO O PROJETO ESTIVER PRONTO
	Base.metadata.create_all(bind=engine)
	print("✅ Banco de dados inicializado com sucesso!")

def drop_db():
	# Deleta todas as tabelas
	#todo EXECUTAR APENAS EM DESENVOLVIMENTO
	Base.metadata.drop_all(bind=engine)
	print("⚠️ Todas as tabelas foram deletadas!")