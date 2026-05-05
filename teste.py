from Infrastructure.database import init_db, SessionLocal
from Domain.Medicamento import Medicamento
from Domain.Fornecedor import Fornecedor
from Domain.Lote import Lote
from Domain.Enums.StatusLote import StatusLote
import datetime

def test_database():
	
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
		print(f"✅ Fornecedor criado: {fornecedor.nome}")
		
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
		
		lote = Lote(
			codigo_lote="2024-ABC-001",
			medicamento_id=medicamento.id,
			fornecedor_id=fornecedor.id,
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
		lote_recuperado = db.query(Lote).first()
		print(f"\n🔗 Lote {lote_recuperado.codigo_lote} contém: {lote_recuperado.medicamento.nome}")
		
		print(f"🔗 Fornecedor: {lote_recuperado.fornecedor.nome}")
		
		print(f"🔗 Quantidade disponível: {lote_recuperado.quantidade_disponivel}")
		
		medicamento_recuperado = db.query(Medicamento).first()
		print(f"\n🔗 Medicamento {medicamento_recuperado.nome} tem {len(medicamento_recuperado.lotes)} lote(s)")

		print("\n✅ TESTES BEM SUCEDIDOS!")
		
	except Exception as e:
		print(f"❌ Erro: {e}")
		db.rollback()
	finally:
		db.close()

if __name__ == "__main__":
	test_database()