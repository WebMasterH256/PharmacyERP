import datetime
import decimal

from typing import List
from sqlalchemy import String, Integer, Boolean, DateTime, func, ForeignKey, DECIMAL
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from Domain.Alerta import Alerta
from Domain.Base import Base
from Domain.Enums.StatusLote import StatusLote
from Domain.Fornecedor import Fornecedor
from Domain.Medicamento import Medicamento


class Lote(Base):
	__tablename__ = 'lote'
	
	id : Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
	codigo_lote : Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
	
	medicamento_id : Mapped[int] = mapped_column(Integer, ForeignKey('medicamento.id'))
	fornecedor_id : Mapped[int] = mapped_column(Integer, ForeignKey('fornecedor.id'))
	
	data_fabricacao : Mapped[datetime.datetime] = mapped_column(DateTime)
	data_validade : Mapped[datetime.datetime] = mapped_column(DateTime, index=True, nullable=False)
	
	quantidade_inicial : Mapped[int] = mapped_column(Integer, default=0)
	quantidade_vendida : Mapped[int] = mapped_column(Integer, default=0)
	
	preco_unitario : Mapped[decimal.Decimal] = mapped_column(DECIMAL, default=0)
	status : Mapped[StatusLote] = mapped_column(StatusLote)
	data_recebimento : Mapped[datetime.datetime] = mapped_column(DateTime)
	
	created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=func.now)
	updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=func.now, onupdate=func.now)


	medicamento: Mapped["Medicamento"] = relationship(
		"Medicamento",
		back_populates="lotes",
		foreign_keys=[medicamento_id]
	)
 
	fornecedor: Mapped["Fornecedor"] = relationship(
		"Fornecedor",
		back_populates="lotes",
		foreign_keys=[fornecedor_id]
	)
 
	alertas: Mapped[List["Alerta"]] = relationship(
		"Alerta",
		back_populates="lote",
		cascade="all, delete-orphan",
		foreign_keys="Alerta.lote_id"
	)
 
	# ============ PROPRIEDADE CALCULADA ============
 
	@property
	def quantidade_disponivel(self) -> int:
		return self.quantidade_inicial - self.quantidade_vendida