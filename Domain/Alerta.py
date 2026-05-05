import datetime

from sqlalchemy import Enum, String, Integer, Boolean, DateTime, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from Domain.Base import Base
from Domain.Enums.TipoAlerta import TipoAlerta
from Domain.Enums.Urgencia import Urgencia

from typing import TYPE_CHECKING

# ODEIO ESSA PORRA DE IMPORTAÇÃO CIRCULAR
if TYPE_CHECKING:
    from Domain.Lote import Lote
    from Domain.Medicamento import Medicamento

class Alerta(Base):
    __tablename__ = 'alerta'
    
    id : Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    medicamento_id : Mapped[int] = mapped_column(Integer, ForeignKey('medicamento.id'))
    lote_id : Mapped[int] = mapped_column(Integer, ForeignKey('lote.id'))

    tipo : Mapped[TipoAlerta] = mapped_column(Enum(TipoAlerta), nullable=False)
    urgencia : Mapped[Urgencia] = mapped_column(Enum(Urgencia), nullable=False)
    mensagem : Mapped[str] = mapped_column(String(500), nullable=False)
    resolvido : Mapped[bool] = mapped_column(Boolean, default=False)
    observacao : Mapped[str] = mapped_column(String(500), nullable=True)

    data_resolucao : Mapped[datetime.datetime] = mapped_column(DateTime, nullable=True)

    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.now)
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)


    medicamento: Mapped["Medicamento"] = relationship(
        "Medicamento",
        back_populates="alertas",
        foreign_keys=[medicamento_id]
    )
 
    lote: Mapped["Lote"] = relationship(
        "Lote",
        back_populates="alertas",
        foreign_keys=[lote_id]
    )
