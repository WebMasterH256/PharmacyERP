from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session

from Domain.Medicamento import Medicamento
from Infrastructure.repositories.medicamento_repository import MedicamentoRepository


class MedicamentoService:

	def __init__(self, db: Session):
		self.db = db
		self.med_repo = MedicamentoRepository(db)

	def criar_medicamento(self, nome: str, codigo_ean: str, principio_ativo: str,
						 apresentacao: str, fabricante: str, quantidade_minima: int,
						 preco_custo_unitario: float, preco_venda_unitario: float,
						 precisa_receita: bool = False) -> dict:

		if self.med_repo.existe_ean(codigo_ean):
			return {
				'sucesso': False,
				'mensagem': f'Medicamento com EAN {codigo_ean} já existe',
				'medicamento_id': None
			}

		if preco_venda_unitario <= preco_custo_unitario:
			return {
				'sucesso': False,
				'mensagem': 'Preço de venda deve ser maior que preço de custo',
				'medicamento_id': None
			}

		try:
			medicamento = Medicamento(
				nome=nome,
				codigo_ean=codigo_ean,
				principio_ativo=principio_ativo,
				apresentacao=apresentacao,
				fabricante=fabricante,
				quantidade_minima=quantidade_minima,
				preco_custo_unitario=preco_custo_unitario,
				preco_venda_unitario=preco_venda_unitario,
				precisa_receita=precisa_receita,
				ativo=True
			)
			self.db.add(medicamento)
			self.db.commit()
			self.db.refresh(medicamento)

			return {
				'sucesso': True,
				'mensagem': f'Medicamento {nome} criado com sucesso',
				'medicamento_id': medicamento.id
			}
		except Exception as e:
			self.db.rollback()
			return {
				'sucesso': False,
				'mensagem': f'Erro ao criar medicamento: {str(e)}',
				'medicamento_id': None
			}

	def atualizar_medicamento(self, medicamento_id: int, dados: dict) -> dict:
		medicamento = self.med_repo.get_by_id(medicamento_id)
		if not medicamento:
			return {'sucesso': False, 'mensagem': 'Medicamento não encontrado'}

		if 'codigo_ean' in dados and dados['codigo_ean'] != medicamento.codigo_ean:
			if self.med_repo.existe_ean(dados['codigo_ean'], excluir_id=medicamento_id):
				return {'sucesso': False, 'mensagem': 'EAN informado já existe'}

		preco_venda = dados.get('preco_venda_unitario', medicamento.preco_venda_unitario)
		preco_custo = dados.get('preco_custo_unitario', medicamento.preco_custo_unitario)
		if preco_venda <= preco_custo:
			return {'sucesso': False, 'mensagem': 'Preço de venda deve ser maior que custo'}

		try:
			self.med_repo.update(medicamento_id, dados)
			return {'sucesso': True, 'mensagem': 'Medicamento atualizado com sucesso'}
		except Exception as e:
			self.db.rollback()
			return {'sucesso': False, 'mensagem': f'Erro: {str(e)}'}

	def listar_medicamentos_ativos(self, skip: int = 0, limit: int = 100) -> List[dict]:
		medicamentos = self.med_repo.get_ativos(skip, limit)
		
		return [
			{
				'id': m.id,
				'nome': m.nome,
				'codigo_ean': m.codigo_ean,
				'principio_ativo': m.principio_ativo,
				'apresentacao': m.apresentacao,
				'fabricante': m.fabricante,
				'preco_venda': float(m.preco_venda_unitario),
				'quantidade_minima': m.quantidade_minima,
				'precisa_receita': m.precisa_receita
			}
			for m in medicamentos
		]

	def obter_medicamento_detalhado(self, medicamento_id: int) -> Optional[dict]:
		medicamento = self.med_repo.get_by_id(medicamento_id)
		if not medicamento:
			return None

		estoque_total = sum(lote.quantidade_disponivel for lote in medicamento.lotes)
		
		return {
			'id': medicamento.id,
			'nome': medicamento.nome,
			'codigo_ean': medicamento.codigo_ean,
			'principio_ativo': medicamento.principio_ativo,
			'apresentacao': medicamento.apresentacao,
			'fabricante': medicamento.fabricante,
			'preco_custo': float(medicamento.preco_custo_unitario),
			'preco_venda': float(medicamento.preco_venda_unitario),
			'quantidade_minima': medicamento.quantidade_minima,
			'precisa_receita': medicamento.precisa_receita,
			'ativo': medicamento.ativo,
			'estoque_total': estoque_total,
			'margem_lucro': ((medicamento.preco_venda_unitario - medicamento.preco_custo_unitario) / medicamento.preco_venda_unitario * 100) if medicamento.preco_venda_unitario > 0 else 0,
			'total_lotes': len(medicamento.lotes),
			'total_alertas': len([a for a in medicamento.alertas if not a.resolvido])
		}

	def buscar_medicamento(self, nome_ou_ean: str) -> List[dict]:
		medicamento = self.med_repo.get_by_ean(nome_ou_ean)
		if medicamento:
			return [self.obter_medicamento_detalhado(medicamento.id)]

		# Buscar por nome
		medicamentos = self.med_repo.get_by_nome(nome_ou_ean)
		return [self.obter_medicamento_detalhado(m.id) for m in medicamentos]

	def desativar_medicamento(self, medicamento_id: int) -> dict:
		medicamento = self.med_repo.get_by_id(medicamento_id)
		if not medicamento:
			return {'sucesso': False, 'mensagem': 'Medicamento não encontrado'}

		try:
			medicamento.ativo = False
			self.db.commit()
			return {'sucesso': True, 'mensagem': f'Medicamento {medicamento.nome} desativado'}
		except Exception as e:
			self.db.rollback()
			return {'sucesso': False, 'mensagem': f'Erro: {str(e)}'}

	def listar_medicamentos_com_estoque_baixo(self) -> List[dict]:
		medicamentos = self.med_repo.get_com_estoque_baixo()
		
		return [
			{
				'id': m.id,
				'nome': m.nome,
				'estoque_atual': sum(lote.quantidade_disponivel for lote in m.lotes),
				'estoque_minimo': m.quantidade_minima,
				'deficit': m.quantidade_minima - sum(lote.quantidade_disponivel for lote in m.lotes)
			}
			for m in medicamentos
		]
