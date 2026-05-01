from enum import Enum

class StatusLote(Enum):
    ATIVO = "ativo"
    VENCIDO = "vencido"
    DESCARTADO = "descartado"
    PROXIMO_VENCIMENTO = "próximo_vencimento" # Vai vencer em até 30 dias