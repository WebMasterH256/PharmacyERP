import datetime

from sqlalchemy import String, Integer, Boolean, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from Domain.Base import Base

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
    
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())