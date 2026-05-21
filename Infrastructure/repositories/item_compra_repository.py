from typing import List, Optional, TYPE_CHECKING
from sqlalchemy.orm import Session

from Domain.Enums.StatusCompra import StatusCompra
from .base_repository import BaseRepository

from Domain.ItemCompra import ItemCompra


class ItemCompraRepository(BaseRepository['ItemCompra']):
	def __init__(self, db: Session):
		from Domain.ItemCompra import ItemCompra
		super().__init__(db, ItemCompra)
	
	def get_por_compra(self, compra_id: int) -> List['ItemCompra']:
		from Domain.ItemCompra import ItemCompra
		return self.db.query(ItemCompra).filter(
			ItemCompra.compra_id == compra_id
		).all()
	
	def get_pendentes_receber(self, compra_id: int) -> List['ItemCompra']:
		from Domain.ItemCompra import ItemCompra
		return self.db.query(ItemCompra).filter(
			ItemCompra.compra_id == compra_id,
			ItemCompra.status != StatusCompra.RECEBIDA
		).all()
	
	def get_por_medicamento(self, medicamento_id: int) -> List['ItemCompra']:
		from Domain.ItemCompra import ItemCompra
		return self.db.query(ItemCompra).filter(
			ItemCompra.medicamento_id == medicamento_id
		).all()
	
	def marcar_como_recebido(self, item_compra_id: int, quantidade_recebida: int = None) -> bool:
		from Domain.ItemCompra import ItemCompra
		item = self.get_by_id(item_compra_id)
		if not item:
			return False
		
		item.status = StatusCompra.RECEBIDA
		if quantidade_recebida:
			item.quantidade_recebida = quantidade_recebida
		
		self.db.commit()
		return True
	
	def calcular_valor_total_compra(self, compra_id: int) -> float:
		from Domain.ItemCompra import ItemCompra
		itens = self.get_por_compra(compra_id)
		return sum(item.preco_unitario * item.quantidade_recebida for item in itens)