from typing import List, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from Domain.Lote import Lote
from Domain.Enums.StatusLote import StatusLote
from .base_repository import BaseRepository


class LoteRepository(BaseRepository[Lote]):
	def __init__(self, db: Session):
		super().__init__(db, Lote)

	def get_by_numero_lote(self, numero_lote: str) -> Optional[Lote]:
		return self.db.query(Lote).filter(
			Lote.codigo_lote == numero_lote
		).first()

	def get_por_medicamento(self, medicamento_id: int) -> List[Lote]:
		return self.db.query(Lote).filter(
			Lote.medicamento_id == medicamento_id,
			Lote.status != StatusLote.DESCARTADO  # Ignora descartados
		).order_by(Lote.data_validade.asc()).all()  # FIFO - mais antigos primeiro

	def get_lotes_vencidos(self) -> List[Lote]:
		hoje = datetime.utcnow().date()
		return self.db.query(Lote).filter(
			and_(
				Lote.data_validade < hoje,
				Lote.status != StatusLote.DESCARTADO
			)
		).all()

	def get_lotes_proximos_vencimento(self, dias: int = 30) -> List[Lote]:
		hoje = datetime.utcnow().date()
		data_limite = hoje + timedelta(days=dias)

		return self.db.query(Lote).filter(
			and_(
				Lote.data_validade >= hoje,
				Lote.data_validade <= data_limite,
				Lote.status == StatusLote.ATIVO
			)
		).order_by(Lote.data_validade.asc()).all()

	def get_lotes_ativos(self, skip: int = 0, limit: int = 100) -> List[Lote]:
		return self.db.query(Lote).filter(
			Lote.status == StatusLote.ATIVO
		).offset(skip).limit(limit).all()

	def get_por_fornecedor(self, fornecedor_id: int) -> List[Lote]:
		return self.db.query(Lote).filter(
			Lote.fornecedor_id == fornecedor_id,
			Lote.status != StatusLote.DESCARTADO
		).all()

	def estoque_total_medicamento(self, medicamento_id: int) -> int:
		lotes = self.get_por_medicamento(medicamento_id)
		return sum(lote.quantidade_disponivel for lote in lotes)

	def marcar_como_vencido(self, lote_id: int) -> bool:
		lote = self.get_by_id(lote_id)
		if not lote:
			return False

		lote.status = StatusLote.VENCIDO
		self.db.commit()
		return True

	def marcar_como_descartado(self, lote_id: int) -> bool:
		lote = self.get_by_id(lote_id)
		if not lote:
			return False

		lote.status = StatusLote.DESCARTADO
		self.db.commit()
		return True

	def atualizar_quantidade_vendida(self, lote_id: int, quantidade: int) -> bool:
		lote = self.get_by_id(lote_id)
		if not lote:
			return False

		if lote.quantidade_disponivel < quantidade:
			return False

		lote.quantidade_vendida += quantidade
		self.db.commit()
		return True