import datetime
import decimal

from sqlalchemy import String, Integer, DateTime, func, ForeignKey, DECIMAL, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, TYPE_CHECKING

from Domain.Base import Base
from Domain.Enums.StatusCompra import StatusCompra

if TYPE_CHECKING:
    from Domain.Fornecedor import Fornecedor
    from Domain.ItemCompra import ItemCompra


class Compra(Base):
	__tablename__ = 'compra'
	
	id : Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
	codigo_pedido : Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
	fornecedor_id : Mapped[int] = mapped_column(Integer, ForeignKey('fornecedor.id'))
	
	data_pedido : Mapped[datetime.datetime] = mapped_column(DateTime)
	data_entrega_esperada : Mapped[datetime.datetime] = mapped_column(DateTime)
	data_entrega_real : Mapped[datetime.datetime] = mapped_column(DateTime, nullable=True)
	
	valor_total : Mapped[decimal.Decimal] = mapped_column(DECIMAL, default=decimal.Decimal(0))
	status : Mapped[StatusCompra] = mapped_column(Enum(StatusCompra))
	
	numero_nf : Mapped[str] = mapped_column(String(50), nullable=True)
	data_nf : Mapped[datetime.datetime] = mapped_column(DateTime, nullable=True)
	
	observacao : Mapped[str] = mapped_column(String(500), nullable=True)
	
	created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.now)
	updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

	fornecedor: Mapped["Fornecedor"] = relationship(
		"Fornecedor",
		back_populates="compras",
		foreign_keys=[fornecedor_id]
	)
 
	itens_compra: Mapped[List["ItemCompra"]] = relationship(
		"ItemCompra",
		back_populates="compra",
		cascade="all, delete-orphan",
		foreign_keys="ItemCompra.compra_id"
	)
