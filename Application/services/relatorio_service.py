from typing import List, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from Domain.Medicamento import Medicamento
from Domain.Lote import Lote
from Domain.Alerta import Alerta
from Infrastructure.repositories.medicamento_repository import MedicamentoRepository
from Infrastructure.repositories.lote_repository import LoteRepository
from Infrastructure.repositories.alerta_repository import AlertaRepository
from Infrastructure.repositories.compra_repository import CompraRepository


class RelatorioService:

	def __init__(self, db: Session):
		self.db = db
		self.med_repo = MedicamentoRepository(db)
		self.lote_repo = LoteRepository(db)
		self.alerta_repo = AlertaRepository(db)
		self.compra_repo = CompraRepository(db)

	def obter_dashboard_geral(self) -> dict:
		medicamentos = self.med_repo.get_all(limit=10000)
		alertas = self.alerta_repo.get_nao_resolvidos()
		compras_pendentes = self.compra_repo.get_pendentes()

		total_estoque = sum(
			sum(lote.quantidade_disponivel for lote in med.lotes)
			for med in medicamentos
		)

		return {
			'resumo': {
				'total_medicamentos': self.med_repo.count(),
				'total_lotes': self.lote_repo.count(),
				'total_estoque_unidades': total_estoque,
				'total_alertas_nao_resolvidos': len(alertas),
				'compras_pendentes': len(compras_pendentes)
			},
			'alertas': {
				'criticos': self.alerta_repo.contar_por_urgencia(self._get_urgencia_critica()),
				'altos': self.alerta_repo.contar_por_urgencia(self._get_urgencia_alta()),
				'medios': self.alerta_repo.contar_por_urgencia(self._get_urgencia_media()),
			},
			'estoque': {
				'medicamentos_estoque_baixo': len(self.med_repo.get_com_estoque_baixo()),
				'lotes_proximos_vencimento': len(self.lote_repo.get_lotes_proximos_vencimento(dias=30)),
				'lotes_vencidos': len(self.lote_repo.get_lotes_vencidos())
			}
		}

	def obter_top_medicamentos(self, limite: int = 10) -> List[dict]:
		medicamentos = self.med_repo.get_all(limit=10000)
		
		dados = [
			{
				'id': m.id,
				'nome': m.nome,
				'estoque': sum(lote.quantidade_disponivel for lote in m.lotes),
				'valor_estoque_total': float(sum(lote.quantidade_disponivel * lote.preco_unitario for lote in m.lotes))
			}
			for m in medicamentos
		]
		
		dados.sort(key=lambda x: x['estoque'], reverse=True)
		return dados[:limite]

	def obter_relatorio_vencimentos(self, dias: int = 30) -> dict:
		lotes_vencer = self.lote_repo.get_lotes_proximos_vencimento(dias=dias)
		lotes_vencidos = self.lote_repo.get_lotes_vencidos()

		return {
			'proximos_vencimento': [
				{
					'lote_id': l.id,
					'numero_lote': l.codigo_lote,
					'medicamento': l.medicamento.nome,
					'data_validade': l.data_validade.strftime('%d/%m/%Y'),
					'dias_ate_vencer': (l.data_validade.date() - datetime.utcnow().date()).days,
					'quantidade': l.quantidade_disponivel
				}
				for l in lotes_vencer
			],
			'ja_vencidos': [
				{
					'lote_id': l.id,
					'numero_lote': l.codigo_lote,
					'medicamento': l.medicamento.nome,
					'data_validade': l.data_validade.strftime('%d/%m/%Y'),
					'dias_vencido': (datetime.utcnow().date() - l.data_validade.date()).days,
					'quantidade': l.quantidade_disponivel
				}
				for l in lotes_vencidos
			]
		}

	def obter_relatorio_fornecedores(self) -> List[dict]:
		"""Retorna dados consolidados por fornecedor"""
		# TODO: Precisa de uma query mais elaborada
		# Por enquanto, retorna estrutura vazia
		return []

	def obter_relatorio_estoque_por_medicamento(self) -> List[dict]:
		medicamentos = self.med_repo.get_all(limit=10000)

		return [
			{
				'id': m.id,
				'nome': m.nome,
				'ean': m.codigo_ean,
				'quantidade_total': sum(lote.quantidade_disponivel for lote in m.lotes),
				'quantidade_minima': m.quantidade_minima,
				'status': 'CRÍTICO' if sum(lote.quantidade_disponivel for lote in m.lotes) < m.quantidade_minima else 'OK',
				'total_lotes': len(m.lotes),
				'preco_custo': float(m.preco_custo_unitario),
				'preco_venda': float(m.preco_venda_unitario),
				'margem_lucro_percentual': ((m.preco_venda_unitario - m.preco_custo_unitario) / m.preco_venda_unitario * 100) if m.preco_venda_unitario > 0 else 0
			}
			for m in medicamentos
		]

	def obter_alertas_por_tipo(self) -> dict:
		from Domain.Enums.TipoAlerta import TipoAlerta
		
		alertas = self.alerta_repo.get_nao_resolvidos()
		
		contagem = {
			'estoque_baixo': 0,
			'proximo_vencimento': 0,
			'ja_vencido': 0,
			'produto_parado': 0
		}

		for alerta in alertas:
			if alerta.tipo == TipoAlerta.ESTOQUE_BAIXO:
				contagem['estoque_baixo'] += 1
			elif alerta.tipo == TipoAlerta.PROXIMO_VENCIDO:
				contagem['proximo_vencimento'] += 1
			elif alerta.tipo == TipoAlerta.VENCIDO:
				contagem['ja_vencido'] += 1
			elif alerta.tipo == TipoAlerta.PRODUTO_PARADO:
				contagem['produto_parado'] += 1

		return contagem

	def obter_resumo_compras(self) -> dict:
		from Domain.Enums.StatusCompra import StatusCompra
		
		todas_compras = self.compra_repo.get_all(limit=10000)

		resumo = {
			'total_compras': len(todas_compras),
			'pendentes': len([c for c in todas_compras if c.status == StatusCompra.PENDENTE]),
			'recebidas': len([c for c in todas_compras if c.status == StatusCompra.RECEBIDA]),
			'parciais': len([c for c in todas_compras if c.status == StatusCompra.PARCIAL]),
			'canceladas': len([c for c in todas_compras if c.status == StatusCompra.CANCELADA]),
			'valor_total_pendente': float(sum(c.valor_total for c in todas_compras if c.status == StatusCompra.PENDENTE)),
			'valor_total_recebido': float(sum(c.valor_total for c in todas_compras if c.status == StatusCompra.RECEBIDA))
		}

		return resumo

	def exportar_relatorio_completo(self) -> dict:
		return {
			'data_geracao': datetime.utcnow().isoformat(),
			'dashboard': self.obter_dashboard_geral(),
			'estoque_por_medicamento': self.obter_relatorio_estoque_por_medicamento(),
			'vencimentos': self.obter_relatorio_vencimentos(),
			'alertas_por_tipo': self.obter_alertas_por_tipo(),
			'resumo_compras': self.obter_resumo_compras(),
			'top_medicamentos': self.obter_top_medicamentos()
		}

	def _get_urgencia_critica(self):
		from Domain.Enums.Urgencia import Urgencia
		return Urgencia.CRITICO

	def _get_urgencia_alta(self):
		from Domain.Enums.Urgencia import Urgencia
		return Urgencia.ALTO

	def _get_urgencia_media(self):
		from Domain.Enums.Urgencia import Urgencia
		return Urgencia.MEDIO
