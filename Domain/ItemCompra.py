import datetime
import decimal

from sqlalchemy import String, Integer, Boolean, DateTime, func, ForeignKey, DECIMAL
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from Domain.Base import Base
from Domain.Enums.StatusCompra import StatusCompra


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
    status : Mapped[StatusCompra] = mapped_column(StatusCompra)
    
    created_at : Mapped[datetime.datetime] = mapped_column(DateTime, default=func.now())
    updated_at : Mapped[datetime.datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())