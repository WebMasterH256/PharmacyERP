from typing import List, Optional, TYPE_CHECKING
from datetime import datetime
from sqlalchemy.orm import Session

from Domain.Enums.TipoAlerta import TipoAlerta
from Domain.Enums.Urgencia import Urgencia
from .base_repository import BaseRepository

if TYPE_CHECKING:
	from Domain.Alerta import Alerta


class AlertaRepository(BaseRepository['Alerta']):
	def __init__(self, db: Session):
		from Domain.Alerta import Alerta
		super().__init__(db, Alerta)
	
	def get_nao_resolvidos(self) -> List['Alerta']:
		from Domain.Alerta import Alerta
		return self.db.query(Alerta).filter(
			Alerta.resolvido == False
		).order_by(Alerta.urgencia.desc()).all()
	
	def get_por_tipo(self, tipo: TipoAlerta) -> List['Alerta']:
		from Domain.Alerta import Alerta
		return self.db.query(Alerta).filter(
			Alerta.tipo == tipo,
			Alerta.resolvido == False
		).all()
	
	def get_por_urgencia(self, urgencia: Urgencia) -> List['Alerta']:
		from Domain.Alerta import Alerta
		return self.db.query(Alerta).filter(
			Alerta.urgencia == urgencia,
			Alerta.resolvido == False
		).all()
	
	def get_por_medicamento(self, medicamento_id: int) -> List['Alerta']:
		from Domain.Alerta import Alerta
		return self.db.query(Alerta).filter(
			Alerta.medicamento_id == medicamento_id
		).all()
	
	def get_por_lote(self, lote_id: int) -> List['Alerta']:
		"""Retorna alertas de um lote"""
		from Domain.Alerta import Alerta
		return self.db.query(Alerta).filter(
			Alerta.lote_id == lote_id
		).all()
	
	def get_resolvidos(self) -> List['Alerta']:
		"""Retorna alertas já resolvidos"""
		from Domain.Alerta import Alerta
		return self.db.query(Alerta).filter(
			Alerta.resolvido == True
		).all()
	
	def marcar_como_resolvido(self, alerta_id: int, observacao: str = "") -> bool:
		from Domain.Alerta import Alerta
		alerta = self.get_by_id(alerta_id)
		if not alerta:
			return False
		
		alerta.resolvido = True
		alerta.data_resolucao = datetime.utcnow()
		if observacao:
			alerta.observacao = observacao
		
		self.db.commit()
		return True
	
	def contar_nao_resolvidos(self) -> int:
		from Domain.Alerta import Alerta
		return self.db.query(Alerta).filter(
			Alerta.resolvido == False
		).count()
	
	def contar_por_urgencia(self, urgencia: Urgencia) -> int:
		from Domain.Alerta import Alerta
		return self.db.query(Alerta).filter(
			Alerta.urgencia == urgencia,
			Alerta.resolvido == False
		).count()