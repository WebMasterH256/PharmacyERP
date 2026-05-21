from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from Infrastructure.database import get_db
from Application.services.relatorio_service import RelatorioService

router = APIRouter(prefix="/api/relatorios", tags=["Relatórios"])

@router.get("/dashboard", response_model=dict)
def dashboard(db: Session = Depends(get_db)):
    service = RelatorioService(db)
    return service.obter_dashboard_geral()

@router.get("/estoque", response_model=list)
def relatorio_estoque(db: Session = Depends(get_db)):
    service = RelatorioService(db)
    return service.obter_relatorio_estoque_por_medicamento()

@router.get("/vencimentos", response_model=dict)
def relatorio_vencimentos(dias: int = Query(30, ge=1), db: Session = Depends(get_db)):
    service = RelatorioService(db)
    return service.obter_relatorio_vencimentos(dias=dias)

@router.get("/top-medicamentos", response_model=list)
def top_medicamentos(limite: int = Query(10, ge=1), db: Session = Depends(get_db)):
    service = RelatorioService(db)
    return service.obter_top_medicamentos(limite=limite)

@router.get("/alertas-por-tipo", response_model=dict)
def alertas_por_tipo(db: Session = Depends(get_db)):
    service = RelatorioService(db)
    return service.obter_alertas_por_tipo()

@router.get("/compras", response_model=dict)
def resumo_compras(db: Session = Depends(get_db)):
    service = RelatorioService(db)
    return service.obter_resumo_compras()

@router.get("/completo", response_model=dict)
def relatorio_completo(db: Session = Depends(get_db)):
    service = RelatorioService(db)
    return service.exportar_relatorio_completo()

@router.get("/medicamento/{medicamento_id}", response_model=dict)
def relatorio_medicamento(medicamento_id: int, db: Session = Depends(get_db)):
    service = RelatorioService(db)
    estoque_completo = service.obter_relatorio_estoque_por_medicamento()
    for item in estoque_completo:
        if item['id'] == medicamento_id:
            return item
    raise HTTPException(status_code=404, detail="Relatório não encontrado para este medicamento")

@router.get("/fornecedor/{fornecedor_id}", response_model=list)
def relatorio_fornecedor(fornecedor_id: int, db: Session = Depends(get_db)):
    service = RelatorioService(db)
    return service.obter_relatorio_fornecedores()

@router.get("/health", response_model=dict)
def health_check():
    return {"status": "ok"}