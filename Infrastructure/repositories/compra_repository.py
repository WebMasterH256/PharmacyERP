from typing import List, Optional, TYPE_CHECKING
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import and_

from Domain.Enums.StatusCompra import StatusCompra
from .base_repository import BaseRepository
from Domain.Compra import Compra


class CompraRepository(BaseRepository['Compra']):
	def __init__(self, db: Session):
		from Domain.Compra import Compra
		super().__init__(db, Compra)
	
	def get_by_codigo_pedido(self, codigo_pedido: str) -> Optional['Compra']:
		from Domain.Compra import Compra
		return self.db.query(Compra).filter(
			Compra.codigo_pedido == codigo_pedido
		).first()
	
	def get_pendentes(self) -> List['Compra']:
		from Domain.Compra import Compra
		return self.db.query(Compra).filter(
			Compra.status == StatusCompra.PENDENTE
		).all()
	
	def get_por_fornecedor(self, fornecedor_id: int) -> List['Compra']:
		from Domain.Compra import Compra
		return self.db.query(Compra).filter(
			Compra.fornecedor_id == fornecedor_id
		).all()
	
	def get_por_periodo(self, data_inicio: datetime, data_fim: datetime) -> List['Compra']:
		from Domain.Compra import Compra
		return self.db.query(Compra).filter(
			Compra.data_pedido.between(data_inicio, data_fim)
		).all()
	
	def get_por_status(self, status: StatusCompra) -> List['Compra']:
		from Domain.Compra import Compra
		return self.db.query(Compra).filter(
			Compra.status == status
		).all()
	
	def marcar_como_recebida(self, compra_id: int, numero_nf: str = "", data_nf: datetime = None) -> bool:
		from Domain.Compra import Compra
		compra = self.get_by_id(compra_id)
		if not compra:
			return False
		
		compra.status = StatusCompra.RECEBIDA
		compra.data_entrega_real = datetime.utcnow()
		if numero_nf:
			compra.numero_nf = numero_nf
		if data_nf:
			compra.data_nf = data_nf
		
		self.db.commit()
		return True