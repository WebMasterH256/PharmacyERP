import datetime
import decimal

from sqlalchemy import String, Integer, Float, Boolean, DateTime, func, DECIMAL
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from typing import List

from Domain.Base import Base
from Domain.Lote import Lote


class Medicamento(Base):
    __tablename__ = 'medicamento'

    id : Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome : Mapped[str] = mapped_column(String(100), nullable=False)
    codigo_ean : Mapped[str] = mapped_column(String(13), unique=True, nullable=False)

    principio_ativo : Mapped[str] = mapped_column(String(100))
    apresentacao : Mapped[str] = mapped_column(String(100))
    fabricante : Mapped[str] = mapped_column(String(255))
    
    quantidade_minima : Mapped[int] = mapped_column(Integer, default=0)
    preco_custo_unitario : Mapped[decimal.Decimal] = mapped_column(DECIMAL)
    preco_venda_unitario : Mapped[decimal.Decimal] = mapped_column(DECIMAL)
    
    precisa_receita : Mapped[bool] = mapped_column(Boolean, default=False)
    ativo : Mapped[bool] = mapped_column(Boolean, default=True)
    
    created_at : Mapped[datetime.datetime] = mapped_column(DateTime, default=func.now) # "func.now" faz o banco de dados gerenciar a data
    updated_at : Mapped[datetime.datetime] = mapped_column(DateTime, default=func.now, onupdate=func.now())

    # Relacionamentos 1:N
    lotes: Mapped[List[Lote]] = relationship(back_populates="medicamento")
    alertas: Mapped[List[Alertas]] = relationship(back_populates="medicamento")
    itens_compra: Mapped[List[ItemCompra]] = relationship(back_populates="medicamento")