from enum import Enum

class TipoAlerta(Enum):
    VENCIDO = "vencido"
    ESTOQUE_BAIXO = "estoque_baixo"
    PROXIMO_VENCIDO = "proximo_vencido"
    PRODUTO_PARADO = "produto_parado"