# Application/services/estoque_service.py
from typing import Optional, List
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from Domain.Medicamento import Medicamento
from Domain.Lote import Lote
from Domain.Enums.StatusLote import StatusLote
from Infrastructure.repositories.medicamento_repository import MedicamentoRepository
from Infrastructure.repositories.lote_repository import LoteRepository
from Infrastructure.repositories.alerta_repository import AlertaRepository


class EstoqueService:

    def __init__(self, db: Session):
        self.db = db
        self.med_repo = MedicamentoRepository(db)
        self.lote_repo = LoteRepository(db)
        self.alerta_repo = AlertaRepository(db)

    def calcular_estoque_total(self, medicamento_id: int) -> int:
        return self.lote_repo.estoque_total_medicamento(medicamento_id)

    def obter_lotes_ativo(self, medicamento_id: int) -> List[Lote]:
        return self.lote_repo.get_por_medicamento(medicamento_id)

    def pode_vender(self, medicamento_id: int, quantidade: int) -> dict:
        estoque_total = self.calcular_estoque_total(medicamento_id)

        if estoque_total < quantidade:
            return {
                'pode': False,
                'estoque_disponivel': estoque_total,
                'motivo': f'Estoque insuficiente. Disponível: {estoque_total}, Solicitado: {quantidade}'
            }

        medicamento = self.med_repo.get_by_id(medicamento_id)
        if not medicamento or not medicamento.ativo:
            return {
                'pode': False,
                'estoque_disponivel': estoque_total,
                'motivo': 'Medicamento inativo ou não encontrado'
            }

        return {
            'pode': True,
            'estoque_disponivel': estoque_total,
            'motivo': 'OK'
        }

    def has_estoque_baixo(self, medicamento_id: int) -> bool:
        medicamento = self.med_repo.get_by_id(medicamento_id)
        if not medicamento:
            return False

        estoque = self.calcular_estoque_total(medicamento_id)
        return estoque < medicamento.quantidade_minima

    def processar_venda(self, medicamento_id: int, quantidade: int) -> dict:

        validacao = self.pode_vender(medicamento_id, quantidade)
        if not validacao['pode']:
            return {
                'sucesso': False,
                'quantidade_vendida': 0,
                'lotes_afetados': [],
                'mensagem': validacao['motivo']
            }

        lotes = self.obter_lotes_ativo(medicamento_id)

        quantidade_restante = quantidade
        lotes_afetados = []

        for lote in lotes:
            if quantidade_restante <= 0:
                break

            quantidade_a_vender = min(lote.quantidade_disponivel, quantidade_restante)

            self.lote_repo.atualizar_quantidade_vendida(
                lote.id,
                quantidade_a_vender
            )

            lotes_afetados.append(lote.id)
            quantidade_restante -= quantidade_a_vender

        medicamento = self.med_repo.get_by_id(medicamento_id)
        medicamento.updated_at = datetime.utcnow()
        self.db.commit()

        return {
            'sucesso': True,
            'quantidade_vendida': quantidade,
            'lotes_afetados': lotes_afetados,
            'mensagem': f'Venda de {quantidade} unidades processada com sucesso'
        }

    def prever_dias_ate_faltar(self, medicamento_id: int, dias_historico: int = 7) -> Optional[int]:
        """
        Calcula em quantos dias o medicamento vai acabar baseado no histórico.
        Assume venda média linear dos últimos dias.
        """
        estoque = self.calcular_estoque_total(medicamento_id)

        if estoque <= 0:
            return 0

        # Buscar lotes e calcular média de venda
        lotes = self.obter_lotes_ativo(medicamento_id)
        if not lotes:
            return None

        # Calcular quantidade total vendida (somando quantidade_vendida de todos lotes)
        total_vendido = sum(lote.quantidade_vendida for lote in lotes)

        if total_vendido == 0:
            return None

        lote_mais_antigo = min(lotes, key=lambda l: l.data_recebimento)
        dias_existencia = (datetime.utcnow() - lote_mais_antigo.data_recebimento).days

        if dias_existencia == 0:
            return None

        velocidade_diaria = total_vendido / dias_existencia

        if velocidade_diaria == 0:
            return None

        dias_até_faltar = int(estoque / velocidade_diaria)

        return dias_até_faltar if dias_até_faltar > 0 else 0