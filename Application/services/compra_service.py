from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session

from Domain.Compra import Compra
from Domain.ItemCompra import ItemCompra
from Domain.Lote import Lote
from Domain.Enums.StatusCompra import StatusCompra
from Domain.Enums.StatusLote import StatusLote
from Infrastructure.repositories.compra_repository import CompraRepository
from Infrastructure.repositories.item_compra_repository import ItemCompraRepository
from Infrastructure.repositories.lote_repository import LoteRepository
from Infrastructure.repositories.fornecedor_repository import FornecedorRepository
from Infrastructure.repositories.medicamento_repository import MedicamentoRepository


class CompraService:

	def __init__(self, db: Session):
		self.db = db
		self.compra_repo = CompraRepository(db)
		self.item_compra_repo = ItemCompraRepository(db)
		self.lote_repo = LoteRepository(db)
		self.fornecedor_repo = FornecedorRepository(db)
		self.med_repo = MedicamentoRepository(db)

	def criar_compra(self, fornecedor_id: int, codigo_pedido: str, data_entrega_esperada: datetime) -> dict:
		fornecedor = self.fornecedor_repo.get_by_id(fornecedor_id)
		if not fornecedor or not fornecedor.ativo:
			return {
				'sucesso': False,
				'mensagem': 'Fornecedor inválido ou inativo',
				'compra_id': None
			}

		try:
			compra = Compra(
				codigo_pedido=codigo_pedido,
				fornecedor_id=fornecedor_id,
				data_pedido=datetime.utcnow(),
				data_entrega_esperada=data_entrega_esperada,
				status=StatusCompra.PENDENTE,
				valor_total=0
			)
			self.db.add(compra)
			self.db.commit()
			self.db.refresh(compra)

			return {
				'sucesso': True,
				'mensagem': f'Compra {codigo_pedido} criada com sucesso',
				'compra_id': compra.id
			}
		except Exception as e:
			self.db.rollback()
			return {
				'sucesso': False,
				'mensagem': f'Erro ao criar compra: {str(e)}',
				'compra_id': None
			}

	def adicionar_item_compra(self, compra_id: int, medicamento_id: int, quantidade_solicitada: int, 
							  preco_unitario: float) -> dict:
		compra = self.compra_repo.get_by_id(compra_id)
		if not compra:
			return {'sucesso': False, 'mensagem': 'Compra não encontrada'}

		medicamento = self.med_repo.get_by_id(medicamento_id)
		if not medicamento:
			return {'sucesso': False, 'mensagem': 'Medicamento não encontrado'}

		try:
			item = ItemCompra(
				compra_id=compra_id,
				medicamento_id=medicamento_id,
				quantidade_solicitada=quantidade_solicitada,
				quantidade_recebida=0,
				preco_unitario=preco_unitario,
				numero_lote="",
				data_validade=datetime.utcnow(),
				status=StatusCompra.PENDENTE
			)
			self.db.add(item)
			
			compra.valor_total += (quantidade_solicitada * preco_unitario)
			self.db.commit()

			return {'sucesso': True, 'mensagem': 'Item adicionado', 'item_id': item.id}
		except Exception as e:
			self.db.rollback()
			return {'sucesso': False, 'mensagem': f'Erro: {str(e)}'}

	def receber_item_compra(self, item_compra_id: int, quantidade_recebida: int, 
						   numero_lote: str, data_validade: datetime) -> dict:
		item = self.item_compra_repo.get_by_id(item_compra_id)
		if not item:
			return {'sucesso': False, 'mensagem': 'Item de compra não encontrado'}

		if quantidade_recebida > item.quantidade_solicitada:
			return {'sucesso': False, 'mensagem': 'Quantidade recebida maior que solicitada'}

		try:
			item.quantidade_recebida = quantidade_recebida
			item.numero_lote = numero_lote
			item.data_validade = data_validade
			item.status = StatusCompra.RECEBIDA

			lote = Lote(
				codigo_lote=numero_lote,
				medicamento_id=item.medicamento_id,
				fornecedor_id=item.compra.fornecedor_id,
				data_fabricacao=datetime.utcnow(),
				data_validade=data_validade,
				quantidade_inicial=quantidade_recebida,
				quantidade_vendida=0,
				preco_unitario=item.preco_unitario,
				status=StatusLote.ATIVO,
				data_recebimento=datetime.utcnow()
			)
			self.db.add(lote)
			self.db.commit()

			return {
				'sucesso': True,
				'mensagem': f'Item recebido. Lote {numero_lote} criado',
				'lote_id': lote.id
			}
		except Exception as e:
			self.db.rollback()
			return {'sucesso': False, 'mensagem': f'Erro: {str(e)}'}

	def receber_compra_completa(self, compra_id: int, numero_nf: str = "", data_nf: datetime = None) -> dict:
		return_repo = self.compra_repo.marcar_como_recebida(compra_id, numero_nf, data_nf)
		
		if return_repo:
			return {
				'sucesso': True,
				'mensagem': f'Compra {compra_id} marcada como recebida'
			}
		return {
			'sucesso': False,
			'mensagem': 'Compra não encontrada'
		}

	def obter_compras_pendentes(self) -> List[Compra]:
		return self.compra_repo.get_pendentes()

	def obter_compra_com_detalhes(self, compra_id: int) -> Optional[dict]:
		compra = self.compra_repo.get_by_id(compra_id)
		if not compra:
			return None

		itens = self.item_compra_repo.get_por_compra(compra_id)
		
		return {
			'compra_id': compra.id,
			'codigo_pedido': compra.codigo_pedido,
			'fornecedor': compra.fornecedor.nome,
			'status': compra.status.value,
			'data_pedido': compra.data_pedido,
			'data_entrega_esperada': compra.data_entrega_esperada,
			'data_entrega_real': compra.data_entrega_real,
			'valor_total': float(compra.valor_total),
			'items': [
				{
					'item_id': i.id,
					'medicamento': i.medicamento.nome,
					'solicitado': i.quantidade_solicitada,
					'recebido': i.quantidade_recebida,
					'preco_unitario': float(i.preco_unitario),
					'status': i.status.value
				}
				for i in itens
			]
		}

	def cancelar_compra(self, compra_id: int) -> dict:
		compra = self.compra_repo.get_by_id(compra_id)
		if not compra:
			return {'sucesso': False, 'mensagem': 'Compra não encontrada'}

		if compra.status != StatusCompra.PENDENTE:
			return {'sucesso': False, 'mensagem': 'Só compras pendentes podem ser canceladas'}

		try:
			compra.status = StatusCompra.CANCELADA
			self.db.commit()
			return {'sucesso': True, 'mensagem': f'Compra {compra_id} cancelada'}
		except Exception as e:
			self.db.rollback()
			return {'sucesso': False, 'mensagem': f'Erro: {str(e)}'}
