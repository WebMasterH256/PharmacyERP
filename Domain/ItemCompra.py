import datetime
import decimal

from sqlalchemy import String, Integer, DateTime, func, ForeignKey, DECIMAL, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from Domain.Base import Base
from Domain.Enums.StatusCompra import StatusCompra

from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from Domain.Compra import Compra
	from Domain.Medicamento import Medicamento


class ItemCompra(Base):
	__tablename__ = 'item_compra'
	
	id : Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
	compra_id : Mapped[int] = mapped_column(Integer, ForeignKey('compra.id'))
	medicamento_id : Mapped[int] = mapped_column(Integer, ForeignKey('medicamento.id'))
	
	quantidade_solicitada : Mapped[int] = mapped_column(Integer)
	quantidade_recebida : Mapped[int] = mapped_column(Integer)
	
	preco_unitario : Mapped[decimal.Decimal] = mapped_column(DECIMAL, default=decimal.Decimal(0))
	numero_lote : Mapped[str] = mapped_column(String(50), nullable=False)
	
	data_validade : Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
	status : Mapped[StatusCompra] = mapped_column(Enum(StatusCompra))

	created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.now)
	updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

	compra: Mapped["Compra"] = relationship(
		"Compra",
		back_populates="itens_compra",
		foreign_keys=[compra_id]
	)

	medicamento: Mapped["Medicamento"] = relationship(
		"Medicamento",
		back_populates="itens_compra",
		foreign_keys=[medicamento_id]
	)
