from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Infrastructure.database import get_db
from Application.services.compra_service import CompraService
from Application.schemas import CompraCreate, ItemCompraCreate, ItemCompraReceber, CompraReceber

router = APIRouter(prefix="/api/compras", tags=["Compras"])

@router.post("/", response_model=dict, status_code=201)
def criar_compra(compra: CompraCreate, db: Session = Depends(get_db)):
    service = CompraService(db)
    resultado = service.criar_compra(
        fornecedor_id=compra.fornecedor_id,
        codigo_pedido=compra.codigo_pedido,
        data_entrega_esperada=compra.data_entrega_esperada
    )
    if not resultado.get('sucesso'):
        raise HTTPException(status_code=400, detail=resultado.get('mensagem'))
    return resultado

@router.post("/{compra_id}/itens", response_model=dict, status_code=201)
def adicionar_item(compra_id: int, item: ItemCompraCreate, db: Session = Depends(get_db)):
    service = CompraService(db)
    resultado = service.adicionar_item_compra(
        compra_id=compra_id,
        medicamento_id=item.medicamento_id,
        quantidade_solicitada=item.quantidade_solicitada,
        preco_unitario=item.preco_unitario
    )
    if not resultado.get('sucesso'):
        raise HTTPException(status_code=400, detail=resultado.get('mensagem'))
    return resultado

@router.post("/itens/{item_compra_id}/receber", response_model=dict)
def receber_item(item_compra_id: int, recebimento: ItemCompraReceber, db: Session = Depends(get_db)):
    service = CompraService(db)
    resultado = service.receber_item_compra(
        item_compra_id=item_compra_id,
        quantidade_recebida=recebimento.quantidade_recebida,
        numero_lote=recebimento.numero_lote,
        data_validade=recebimento.data_validade
    )
    if not resultado.get('sucesso'):
        raise HTTPException(status_code=400, detail=resultado.get('mensagem'))
    return resultado

@router.get("/", response_model=list)
def listar_compras(db: Session = Depends(get_db)):
    service = CompraService(db)
    compras = service.compra_repo.get_all()
    return [{"id": c.id, "codigo_pedido": c.codigo_pedido, "status": c.status.value, "valor_total": float(c.valor_total)} for c in compras]

@router.get("/pendentes/", response_model=list)
def listar_pendentes(db: Session = Depends(get_db)):
    service = CompraService(db)
    compras = service.obter_compras_pendentes()
    return [{"id": c.id, "codigo_pedido": c.codigo_pedido, "status": c.status.value, "valor_total": float(c.valor_total)} for c in compras]

@router.get("/{compra_id}", response_model=dict)
def detalhes_compra(compra_id: int, db: Session = Depends(get_db)):
    service = CompraService(db)
    resultado = service.obter_compra_com_detalhes(compra_id)
    if not resultado:
        raise HTTPException(status_code=404, detail="Compra não encontrada")
    return resultado

@router.put("/{compra_id}/receber", response_model=dict)
def finalizar_recebimento(compra_id: int, dados: CompraReceber, db: Session = Depends(get_db)):
    service = CompraService(db)
    resultado = service.receber_compra_completa(
        compra_id=compra_id,
        numero_nf=dados.numero_nf or "",
        data_nf=dados.data_nf
    )
    if not resultado.get('sucesso'):
        raise HTTPException(status_code=400, detail=resultado.get('mensagem'))
    return resultado

@router.delete("/{compra_id}", response_model=dict)
def cancelar_compra(compra_id: int, db: Session = Depends(get_db)):
    service = CompraService(db)
    resultado = service.cancelar_compra(compra_id)
    if not resultado.get('sucesso'):
        raise HTTPException(status_code=400, detail=resultado.get('mensagem'))
    return resultado