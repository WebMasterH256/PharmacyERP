import datetime
import decimal

from sqlalchemy import String, Integer, Boolean, DateTime, func, ForeignKey, DECIMAL
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from Domain.Base import Base
from Domain.Enums.StatusCompra import StatusCompra


class Compra(Base):
    __tablename__ = 'compra'
    
    id : Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    codigo_pedido : Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    fornecedor_id : Mapped[int] = mapped_column(Integer, ForeignKey('fornecedor.id'))
    
    data_pedido : Mapped[datetime.datetime] = mapped_column(DateTime)
    data_entrega_esperada : Mapped[datetime.datetime] = mapped_column(DateTime)
    data_entrega_real : Mapped[datetime.datetime] = mapped_column(DateTime, nullable=True)
    
    valor_total : [decimal.Decimal] = mapped_column(DECIMAL, default=decimal.Decimal(0))
    status : Mapped[StatusCompra] = mapped_column(StatusCompra)
    
    numero_nf : Mapped[str] = mapped_column(String(50), nullable=True)
    data_nf : Mapped[datetime.datetime] = mapped_column(DateTime, nullable=True)
    
    observacao : Mapped[str] = mapped_column(String(500), nullable=True)
    
    created_at : Mapped[datetime.datetime] = mapped_column(DateTime, default=func.now())
    updated_at : Mapped[datetime.datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
    