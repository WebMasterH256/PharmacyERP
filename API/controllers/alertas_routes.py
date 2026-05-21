from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session

from Infrastructure.database import get_db
from Application.services.alerta_service import AlertaService
from Application.schemas import AlertaResolverRequest
from Domain.Enums.TipoAlerta import TipoAlerta
from Domain.Enums.Urgencia import Urgencia

router = APIRouter(prefix="/api/alertas", tags=["Alertas"])


@router.post("/gerar-todos", response_model=dict, status_code=200, summary="Gerar todos alertas")
def gerar_todos_alertas(db: Session = Depends(get_db)):
	"""
	Executa a geração de TODOS os tipos de alerta automaticamente.
	
	Gera alertas para:
	- Medicamentos com estoque < mínimo
	- Lotes vencendo em até 30 dias
	- Lotes já vencidos (CRÍTICO)
	- Produtos parados
	
	Retorna contagem de alertas gerados por tipo.
	"""
	service = AlertaService(db)
	
	try:
		resultado = service.gerar_todos_os_alertas()
		return {
			'sucesso': True,
			'mensagem': f'Total de {resultado["total"]} alertas gerados',
			'detalhes': resultado
		}
	except Exception as e:
		raise HTTPException(status_code=500, detail=f"Erro ao gerar alertas: {str(e)}")


@router.get("/nao-resolvidos", response_model=dict, summary="Alertas não resolvidos")
def alertas_nao_resolvidos(db: Session = Depends(get_db)):
	"""
	Retorna TODOS os alertas ainda pendentes de resolução.
	
	Ordenados por urgência (CRÍTICO primeiro).
	Útil para o dashboard principal.
	"""
	service = AlertaService(db)
	resumo = service.obter_resumo_alertas()
	
	return {
		'total': resumo['total_nao_resolvidos'],
		'criticos': resumo['criticos'],
		'altos': resumo['altos'],
		'medios': resumo['medios'],
		'baixos': resumo['baixos']
	}


@router.get("/por-tipo", response_model=dict, summary="Alertas por tipo")
def alertas_por_tipo(
	tipo: str = Query(..., description="ESTOQUE_BAIXO, PROXIMO_VENCIMENTO, VENCIDO, PRODUTO_PARADO"),
	db: Session = Depends(get_db)
):
	"""
	Retorna alertas de um tipo específico não resolvidos.
	
	Tipos válidos:
	- ESTOQUE_BAIXO
	- PROXIMO_VENCIMENTO
	- VENCIDO
	- PRODUTO_PARADO
	"""
	# Validar tipo
	try:
		tipo_enum = TipoAlerta[tipo.upper()]
	except KeyError:
		raise HTTPException(
			status_code=400,
			detail=f"Tipo inválido. Use: ESTOQUE_BAIXO, PROXIMO_VENCIMENTO, VENCIDO, PRODUTO_PARADO"
		)
	
	service = AlertaService(db)
	# Usar repository direto porque AlertaService não tem método específico
	alertas = service.alerta_repo.get_por_tipo(tipo_enum)
	
	return {
		'tipo': tipo,
		'total': len(alertas),
		'alertas': [
			{
				'id': a.id,
				'medicamento': a.medicamento.nome if a.medicamento else None,
				'urgencia': a.urgencia.value,
				'mensagem': a.mensagem
			}
			for a in alertas
		]
	}


@router.get("/{alerta_id}", response_model=dict, summary="Detalhes do alerta")
def obter_alerta(
	alerta_id: int = Path(..., gt=0),
	db: Session = Depends(get_db)
):
	"""
	Retorna informações completas de um alerta específico.
	"""
	service = AlertaService(db)
	alerta = service.alerta_repo.get_by_id(alerta_id)
	
	if not alerta:
		raise HTTPException(status_code=404, detail="Alerta não encontrado")
	
	return {
		'id': alerta.id,
		'tipo': alerta.tipo.value,
		'urgencia': alerta.urgencia.value,
		'medicamento': alerta.medicamento.nome if alerta.medicamento else None,
		'lote': alerta.lote.codigo_lote if alerta.lote else None,
		'mensagem': alerta.mensagem,
		'resolvido': alerta.resolvido
	}


@router.put("/{alerta_id}/resolver", response_model=dict, summary="Resolver alerta")
def resolver_alerta(
	alerta_id: int,
	body: AlertaResolverRequest,
	db: Session = Depends(get_db)
):
	"""
	Marca um alerta como resolvido com uma observação opcional.
	
	Exemplo:
	```json
	{
		"observacao": "Compra realizada para repor estoque"
	}
	```
	"""
	service = AlertaService(db)
	
	sucesso = service.resolver_alerta(alerta_id, body.observacao or "")
	
	if not sucesso:
		raise HTTPException(status_code=404, detail="Alerta não encontrado")
	
	return {
		'sucesso': True,
		'mensagem': 'Alerta resolvido com sucesso'
	}


@router.post("/gerar-estoque-baixo", response_model=dict, summary="Alertas estoque baixo")
def gerar_alertas_estoque(db: Session = Depends(get_db)):
	"""
	Gera alertas para medicamentos com estoque < quantidade_minima.
	
	Urgência: MÉDIO
	"""
	service = AlertaService(db)
	
	try:
		alertas = service.gerar_alertas_estoque_baixo()
		return {
			'sucesso': True,
			'total': len(alertas),
			'mensagem': f'{len(alertas)} alertas de estoque baixo criados'
		}
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))


@router.post("/gerar-proximos-vencer", response_model=dict, summary="Alertas próximos vencer")
def gerar_alertas_vencimento(
	dias: int = Query(30, ge=1, le=365, description="Quantidade de dias para considerar"),
	db: Session = Depends(get_db)
):
	"""
	Gera alertas para lotes que VÃO VENCER em até X dias.
	
	- **dias**: Quantidade de dias (padrão 30)
	
	Urgência: MÉDIO (ALTO se < 7 dias)
	"""
	service = AlertaService(db)
	
	try:
		alertas = service.gerar_alertas_proximo_vencimento(dias=dias)
		return {
			'sucesso': True,
			'dias_filtro': dias,
			'total': len(alertas),
			'mensagem': f'{len(alertas)} alertas de vencimento gerados'
		}
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))


@router.post("/gerar-vencidos", response_model=dict, summary="Alertas lotes vencidos")
def gerar_alertas_vencidos(db: Session = Depends(get_db)):
	"""
	Gera alertas CRÍTICOS para lotes já vencidos.
	
	⚠️ CRÍTICO PARA COMPLIANCE!
	Estes lotes precisam ser descartados imediatamente.
	
	Urgência: CRÍTICO
	"""
	service = AlertaService(db)
	
	try:
		alertas = service.gerar_alertas_ja_vencido()
		return {
			'sucesso': True,
			'total': len(alertas),
			'urgencia': 'CRÍTICO',
			'mensagem': f'{len(alertas)} alertas CRÍTICOS de vencidos gerados'
		}
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))
