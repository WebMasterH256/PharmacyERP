from enum import Enum

class StatusCompra(Enum):
    RECEBIDA = "recebida"
    CANCELADA = "cancelada"
    PARCIAL = "parcial"
    PENDENTE = "pendente"
        