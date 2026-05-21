from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from Infrastructure.database import get_db
from Infrastructure.repositories.lote_repository import LoteRepository
from Application.services.estoque_service import EstoqueService

router = APIRouter(prefix="/api/lotes", tags=["Lotes"])

@router.get("/medicamento/{medicamento_id}", response_model=list)
def lotes_por_medicamento(medicamento_id: int, db: Session = Depends(get_db)):
    service = EstoqueService(db)
    lotes = service.obter_lotes_ativo(medicamento_id)
    return [{"id": l.id, "codigo_lote": l.codigo_lote, "data_validade": l.data_validade, "quantidade_disponivel": l.quantidade_disponivel, "status": l.status.value} for l in lotes]

@router.get("/vencidos/", response_model=list)
def lotes_vencidos(db: Session = Depends(get_db)):
    repo = LoteRepository(db)
    lotes = repo.get_lotes_vencidos()
    return [{"id": l.id, "codigo_lote": l.codigo_lote, "data_validade": l.data_validade, "quantidade_disponivel": l.quantidade_disponivel, "medicamento_id": l.medicamento_id} for l in lotes]

@router.get("/proximos-vencer/", response_model=list)
def lotes_proximos_vencer(dias: int = Query(30, ge=1), db: Session = Depends(get_db)):
    repo = LoteRepository(db)
    lotes = repo.get_lotes_proximos_vencimento(dias)
    return [{"id": l.id, "codigo_lote": l.codigo_lote, "data_validade": l.data_validade, "quantidade_disponivel": l.quantidade_disponivel, "medicamento_id": l.medicamento_id} for l in lotes]

@router.get("/{lote_id}", response_model=dict)
def detalhes_lote(lote_id: int, db: Session = Depends(get_db)):
    repo = LoteRepository(db)
    lote = repo.get_by_id(lote_id)
    if not lote:
        raise HTTPException(status_code=404, detail="Lote não encontrado")
    return {
        "id": lote.id,
        "codigo_lote": lote.codigo_lote,
        "medicamento_id": lote.medicamento_id,
        "fornecedor_id": lote.fornecedor_id,
        "data_fabricacao": lote.data_fabricacao,
        "data_validade": lote.data_validade,
        "quantidade_inicial": lote.quantidade_inicial,
        "quantidade_vendida": lote.quantidade_vendida,
        "quantidade_disponivel": lote.quantidade_disponivel,
        "preco_unitario": float(lote.preco_unitario),
        "status": lote.status.value
    }

@router.put("/{lote_id}/marcar-vencido", response_model=dict)
def marcar_vencido(lote_id: int, db: Session = Depends(get_db)):
    repo = LoteRepository(db)
    sucesso = repo.marcar_como_vencido(lote_id)
    if not sucesso:
        raise HTTPException(status_code=404, detail="Lote não encontrado")
    return {"sucesso": True}

@router.put("/{lote_id}/marcar-descartado", response_model=dict)
def marcar_descartado(lote_id: int, db: Session = Depends(get_db)):
    repo = LoteRepository(db)
    sucesso = repo.marcar_como_descartado(lote_id)
    if not sucesso:
        raise HTTPException(status_code=404, detail="Lote não encontrado")
    return {"sucesso": True}

@router.get("/estoque/total-medicamento/{medicamento_id}", response_model=dict)
def estoque_total(medicamento_id: int, db: Session = Depends(get_db)):
    service = EstoqueService(db)
    total = service.calcular_estoque_total(medicamento_id)
    return {"medicamento_id": medicamento_id, "estoque_total": total}