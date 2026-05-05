import datetime

from sqlalchemy import String, Integer, Boolean, DateTime, func, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

from Domain.Base import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from Domain.Compra import Compra
	from Domain.Lote import Lote


class Fornecedor(Base):
	__tablename__ = 'fornecedor'
	
	id : Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
	nome : Mapped[str] = mapped_column(String(255), nullable=False)
	razao_social : Mapped[str] = mapped_column(String(255), nullable=False)
	cnpj : Mapped[str] = mapped_column(String(18), nullable=False, unique=True)
	
	contato_vendedor : Mapped[str] = mapped_column(String(255), nullable=False)
	email : Mapped[str] = mapped_column(String(255), nullable=False)
	telefone: Mapped[str] = mapped_column(String(20), nullable=False)
	
	endereco : Mapped[str] = mapped_column(String(255), nullable=False)
	ativo : Mapped[bool] = mapped_column(Boolean, nullable=False)

	created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.now)
	updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

	compras: Mapped[List["Compra"]] = relationship(
		"Compra",
		back_populates="fornecedor",
		cascade="all, delete-orphan",
		foreign_keys="Compra.fornecedor_id"
	)
 
	lotes: Mapped[List["Lote"]] = relationship(
		"Lote",
		back_populates="fornecedor",
		cascade="all, delete-orphan",
		foreign_keys="Lote.fornecedor_id"
	)