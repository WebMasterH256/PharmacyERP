from typing import List
from datetime import datetime
from sqlalchemy.orm import Session

from Domain.Alerta import Alerta
from Domain.Enums.TipoAlerta import TipoAlerta
from Domain.Enums.Urgencia import Urgencia
from Infrastructure.repositories.medicamento_repository import MedicamentoRepository
from Infrastructure.repositories.lote_repository import LoteRepository
from Infrastructure.repositories.alerta_repository import AlertaRepository


class AlertaService:

    def __init__(self, db: Session):
        self.db = db
        self.med_repo = MedicamentoRepository(db)
        self.lote_repo = LoteRepository(db)
        self.alerta_repo = AlertaRepository(db)

    def gerar_alertas_estoque_baixo(self) -> List[Alerta]:
        medicamentos_com_alerta = self.med_repo.get_com_estoque_baixo()
        alertas_criados = []

        for medicamento in medicamentos_com_alerta:
            alertas_existentes = self.alerta_repo.get_por_medicamento(medicamento.id)
            if any(a.tipo == TipoAlerta.ESTOQUE_BAIXO and not a.resolvido for a in alertas_existentes):
                continue

            estoque_total = sum(lote.quantidade_disponivel for lote in medicamento.lotes)
            alerta = Alerta(
                medicamento_id=medicamento.id,
                lote_id=None,
                tipo=TipoAlerta.ESTOQUE_BAIXO,
                urgencia=Urgencia.MEDIO,
                mensagem=f"{medicamento.nome}: Estoque baixo ({estoque_total} unidades, mínimo {medicamento.quantidade_minima})",
                resolvido=False
            )
            self.db.add(alerta)
            alertas_criados.append(alerta)

        self.db.commit()
        return alertas_criados

    def gerar_alertas_proximo_vencimento(self, dias: int = 30) -> List[Alerta]:
        lotes_proximos_vencer = self.lote_repo.get_lotes_proximos_vencimento(dias=dias)
        alertas_criados = []

        for lote in lotes_proximos_vencer:
            alertas_existentes = self.alerta_repo.get_por_lote(lote.id)
            if any(a.tipo == TipoAlerta.PROXIMO_VENCIDO and not a.resolvido for a in alertas_existentes):
                continue

            dias_ate_vencer = (lote.data_validade.date() - datetime.utcnow().date()).days
            alerta = Alerta(
                medicamento_id=lote.medicamento_id,
                lote_id=lote.id,
                tipo=TipoAlerta.PROXIMO_VENCIDO,
                urgencia=Urgencia.ALTO if dias_ate_vencer < 7 else Urgencia.MEDIO,
                mensagem=f"Lote {lote.codigo_lote} do {lote.medicamento.nome} vence em {dias_ate_vencer} dias",
                resolvido=False
            )
            self.db.add(alerta)
            alertas_criados.append(alerta)

        self.db.commit()
        return alertas_criados

    def gerar_alertas_ja_vencido(self) -> List[Alerta]:
        lotes_vencidos = self.lote_repo.get_lotes_vencidos()
        alertas_criados = []

        for lote in lotes_vencidos:
            self.lote_repo.marcar_como_vencido(lote.id)

            alerta = Alerta(
                medicamento_id=lote.medicamento_id,
                lote_id=lote.id,
                tipo=TipoAlerta.VENCIDO,
                urgencia=Urgencia.CRITICO,
                mensagem=f"🚨 CRÍTICO: Lote {lote.codigo_lote} do {lote.medicamento.nome} JÁ VENCEU em "
                         f"{lote.data_validade.strftime('%d/%m/%Y')}. DESCARTAR IMEDIATAMENTE!",
                resolvido=False
            )
            self.db.add(alerta)
            alertas_criados.append(alerta)

        self.db.commit()
        return alertas_criados

    def gerar_alertas_produto_parado(self, dias_sem_venda: int = 60) -> List[Alerta]:
        """Cria alertas para produtos que não vendem há muito tempo"""
        # Nota: Implementação simplificada - precisa de VendaRepository para ser real
        # Por enquanto, retorna vazio
        return []

    def gerar_todos_os_alertas(self) -> dict:
        alertas_estoque = self.gerar_alertas_estoque_baixo()
        alertas_vencer = self.gerar_alertas_proximo_vencimento()
        alertas_vencido = self.gerar_alertas_ja_vencido()
        alertas_parado = self.gerar_alertas_produto_parado()

        return {
            'estoque_baixo': len(alertas_estoque),
            'proximo_vencimento': len(alertas_vencer),
            'ja_vencido': len(alertas_vencido),
            'produto_parado': len(alertas_parado),
            'total': len(alertas_estoque) + len(alertas_vencer) + len(alertas_vencido) + len(alertas_parado)
        }

    def resolver_alerta(self, alerta_id: int, observacao: str = "") -> bool:
        return self.alerta_repo.marcar_como_resolvido(alerta_id, observacao)

    def limpar_alertas_resolvidos_antigos(self, dias: int = 30) -> int:
        alertas_resolvidos = self.alerta_repo.get_resolvidos()
        contador = 0

        for alerta in alertas_resolvidos:
            if alerta.data_resolucao and (datetime.utcnow() - alerta.data_resolucao).days > dias:
                self.alerta_repo.delete(alerta.id)
                contador += 1

        return contador

    def obter_resumo_alertas(self) -> dict:
        nao_resolvidos = self.alerta_repo.get_nao_resolvidos()

        return {
            'total_nao_resolvidos': len(nao_resolvidos),
            'criticos': self.alerta_repo.contar_por_urgencia(Urgencia.CRITICO),
            'altos': self.alerta_repo.contar_por_urgencia(Urgencia.ALTO),
            'medios': self.alerta_repo.contar_por_urgencia(Urgencia.MEDIO),
            'baixos': self.alerta_repo.contar_por_urgencia(Urgencia.BAIXO),
        }