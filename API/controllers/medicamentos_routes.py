from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session

from Infrastructure.database import get_db
from Application.services.medicamento_service import MedicamentoService
from Application.schemas import MedicamentoCreate, MedicamentoUpdate, MedicamentoResponse

router = APIRouter(prefix="/api/medicamentos", tags=["Medicamentos"])


@router.post("/", response_model=dict, status_code=201, summary="Criar medicamento")
def criar_medicamento(
	medicamento: MedicamentoCreate,
	db: Session = Depends(get_db)
):
	"""
	Cria um novo medicamento com validações de EAN único e preço válido.
	
	- **nome**: Nome do medicamento (obrigatório)
	- **codigo_ean**: EAN único (obrigatório)
	- **quantidade_minima**: Quantidade mínima de estoque
	- **preco_venda_unitario**: Deve ser > preco_custo_unitario
	"""
	service = MedicamentoService(db)
	resultado = service.criar_medicamento(
		nome=medicamento.nome,
		codigo_ean=medicamento.codigo_ean,
		principio_ativo=medicamento.principio_ativo,
		apresentacao=medicamento.apresentacao,
		fabricante=medicamento.fabricante,
		quantidade_minima=medicamento.quantidade_minima,
		preco_custo_unitario=medicamento.preco_custo_unitario,
		preco_venda_unitario=medicamento.preco_venda_unitario,
		precisa_receita=medicamento.precisa_receita
	)
	
	if not resultado['sucesso']:
		raise HTTPException(status_code=400, detail=resultado['mensagem'])
	
	return resultado


@router.get("/", response_model=list, summary="Listar medicamentos")
def listar_medicamentos(
	skip: int = Query(0, ge=0, description="Quantos pular"),
	limit: int = Query(100, ge=1, le=1000, description="Quantos retornar"),
	db: Session = Depends(get_db)
):
	"""
	Lista medicamentos ativos com paginação.
	
	- **skip**: Número de registros a pular (padrão 0)
	- **limit**: Número máximo de registros (padrão 100, máximo 1000)
	"""
	service = MedicamentoService(db)
	return service.listar_medicamentos_ativos(skip=skip, limit=limit)


@router.get("/{medicamento_id}", response_model=dict, summary="Obter medicamento")
def obter_medicamento(
	medicamento_id: int = Path(..., gt=0, description="ID do medicamento"),
	db: Session = Depends(get_db)
):
	"""
	Retorna detalhes completos de um medicamento incluindo estoque total.
	"""
	service = MedicamentoService(db)
	resultado = service.obter_medicamento_detalhado(medicamento_id)
	
	if not resultado:
		raise HTTPException(status_code=404, detail="Medicamento não encontrado")
	
	return resultado


@router.get("/buscar/termo", response_model=list, summary="Buscar medicamento")
def buscar_medicamento(
	termo: str = Query(..., min_length=1, description="Nome ou EAN para buscar"),
	db: Session = Depends(get_db)
):
	"""
	Busca medicamentos por nome (parcial) ou EAN (exato).
	
	- **termo**: Palavra-chave para buscar por nome ou EAN completo
	
	Exemplo: `/buscar/dipirona` ou `/buscar/7896045401234`
	"""
	service = MedicamentoService(db)
	resultado = service.buscar_medicamento(termo)
	
	if not resultado:
		raise HTTPException(status_code=404, detail="Nenhum medicamento encontrado")
	
	return resultado


@router.put("/{medicamento_id}", response_model=dict, summary="Atualizar medicamento")
def atualizar_medicamento(
	medicamento_id: int,
	dados: MedicamentoUpdate,
	db: Session = Depends(get_db)
):
	"""
	Atualiza informações de um medicamento.
	Todos os campos são opcionais (atualiza apenas os fornecidos).
	"""
	service = MedicamentoService(db)
	
	# Converter para dict e remover None
	dados_dict = {k: v for k, v in dados.dict().items() if v is not None}
	
	if not dados_dict:
		raise HTTPException(status_code=400, detail="Nenhum campo para atualizar")
	
	resultado = service.atualizar_medicamento(medicamento_id, dados_dict)
	
	if not resultado['sucesso']:
		raise HTTPException(status_code=400, detail=resultado['mensagem'])
	
	return resultado


@router.delete("/{medicamento_id}", response_model=dict, summary="Desativar medicamento")
def desativar_medicamento(
	medicamento_id: int,
	db: Session = Depends(get_db)
):
	"""
	Desativa um medicamento (soft delete).
	O registro é mantido no banco de dados mas não aparece em listagens.
	"""
	service = MedicamentoService(db)
	resultado = service.desativar_medicamento(medicamento_id)
	
	if not resultado['sucesso']:
		raise HTTPException(status_code=404, detail=resultado['mensagem'])
	
	return resultado


@router.get("/estoque/baixo", response_model=list, summary="Medicamentos com estoque baixo")
def medicamentos_estoque_baixo(db: Session = Depends(get_db)):
	"""
	Retorna apenas medicamentos com estoque abaixo da quantidade mínima.
	
	Útil para alertar sobre reposição necessária.
	"""
	service = MedicamentoService(db)
	return service.listar_medicamentos_com_estoque_baixo()
