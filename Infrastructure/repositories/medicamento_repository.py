from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_

from Domain.Medicamento import Medicamento
from .base_repository import BaseRepository


class MedicamentoRepository(BaseRepository[Medicamento]):
	def __init__(self, db: Session):
		super().__init__(db, Medicamento)
	
	def get_by_ean(self, codigo_ean: str) -> Optional[Medicamento]:
		return self.db.query(Medicamento).filter(
			Medicamento.codigo_ean == codigo_ean
		).first()
	
	def get_by_nome(self, nome: str) -> List[Medicamento]:
		return self.db.query(Medicamento).filter(
			Medicamento.nome.ilike(f"%{nome}%")
		).all()
	
	def get_ativos(self, skip: int = 0, limit: int = 100) -> List[Medicamento]:
		return self.db.query(Medicamento).filter(
			Medicamento.ativo == True
		).offset(skip).limit(limit).all()
	
	def get_com_estoque_baixo(self) -> List[Medicamento]:
		medicamentos = self.get_all(limit=1000)
		
		resultado = []
		for med in medicamentos:
			# Calcular estoque total de todos os lotes
			estoque_total = sum(
				lote.quantidade_disponivel for lote in med.lotes
			)
			
			if estoque_total < med.quantidade_minima:
				resultado.append(med)
		
		return resultado
	
	def get_por_fabricante(self, fabricante: str) -> List[Medicamento]:
		return self.db.query(Medicamento).filter(
			Medicamento.fabricante.ilike(f"%{fabricante}%")
		).all()
	
	def existe_ean(self, codigo_ean: str, excluir_id: Optional[int] = None) -> bool:
		query = self.db.query(Medicamento).filter(
			Medicamento.codigo_ean == codigo_ean
		)
		
		if excluir_id:
			query = query.filter(Medicamento.id != excluir_id)
		
		return query.first() is not None