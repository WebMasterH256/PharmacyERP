from Infrastructure.database import init_db, SessionLocal
from Domain.Medicamento import Medicamento
from Domain.Fornecedor import Fornecedor
from Domain.Lote import Lote
from Domain.Enums.StatusLote import StatusLote
import datetime

def test_database():
	"""Testa se o banco funciona"""
	
	# 1. Inicialização do banco
	init_db()
	
	# 2. Inicia uma sessão local
	db = SessionLocal()
	
	try:
		# 3. Criar dados de teste
		
		# Criar fornecedor
		fornecedor = Fornecedor(
			nome="Distribuidora MedFarma",
			razao_social="MedFarma Distribuição LTDA",
			cnpj="12.345.678/0001-90",
			contato_vendedor="João Silva",
			email="contato@medfarma.com.br",
			telefone="(11) 99999-9999",
			endereco="Rua das Flores, 123, São Paulo, SP",
			ativo=True
		)
		db.add(fornecedor)
		db.commit()  # Salva no banco
		print(f"✅ Fornecedor criado: {fornecedor.nome}")
		
		# Criar medicamento
		medicamento = Medicamento(
			nome="Dipirona 500mg",
			codigo_ean="7896045401234",
			principio_ativo="Dipirona Monoidratada",
			apresentacao="Comprimido",
			fabricante="Laboratório Genérico",
			quantidade_minima=50,
			preco_custo_unitario=0.50,
			preco_venda_unitario=2.50,
			precisa_receita=False,
			ativo=True
		)
		db.add(medicamento)
		db.commit()
		print(f"✅ Medicamento criado: {medicamento.nome}")
		
		# Criar lote (conectado ao medicamento e fornecedor)
		lote = Lote(
			codigo_lote="2024-ABC-001",
			medicamento_id=medicamento.id,  # Conectar ao medicamento
			fornecedor_id=fornecedor.id,     # Conectar ao fornecedor
			data_fabricacao=datetime.date(2024, 1, 15),
			data_validade=datetime.date(2026, 1, 15),
			quantidade_inicial=1000,
			quantidade_vendida=0,
			preco_unitario=0.50,
			status=StatusLote.ATIVO
		)
		db.add(lote)
		db.commit()
		print(f"✅ Lote criado: {lote.codigo_lote}")
		
		# 4. TESTAR RELACIONAMENTOS
		
		# Acessar medicamento a partir do lote
		lote_recuperado = db.query(Lote).first()
		print(f"\n🔗 Lote {lote_recuperado.codigo_lote} contém: {lote_recuperado.medicamento.nome}")
		
		# Acessar fornecedor a partir do lote
		print(f"🔗 Fornecedor: {lote_recuperado.fornecedor.nome}")
		
		# Acessar quantidade_disponivel (propriedade calculada)
		print(f"🔗 Quantidade disponível: {lote_recuperado.quantidade_disponivel}")
		
		# Acessar lotes a partir do medicamento
		medicamento_recuperado = db.query(Medicamento).first()
		print(f"\n🔗 Medicamento {medicamento_recuperado.nome} tem {len(medicamento_recuperado.lotes)} lote(s)")

		print("\n✅ TODOS OS TESTES PASSARAM!")
		
	except Exception as e:
		print(f"❌ Erro: {e}")
		db.rollback()
	finally:
		db.close()

if __name__ == "__main__":
	test_database()