from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


# ============ MEDICAMENTO SCHEMAS ============

class MedicamentoCreate(BaseModel):
	"""Schema para criar medicamento"""
	nome: str = Field(..., min_length=1, description="Nome do medicamento")
	codigo_ean: str = Field(..., min_length=1, description="Código EAN único")
	principio_ativo: str = Field(..., min_length=1)
	apresentacao: str = Field(..., min_length=1)
	fabricante: str = Field(..., min_length=1)
	quantidade_minima: int = Field(..., gt=0)
	preco_custo_unitario: float = Field(..., gt=0)
	preco_venda_unitario: float = Field(..., gt=0)
	precisa_receita: bool = False


class MedicamentoUpdate(BaseModel):
	"""Schema para atualizar medicamento"""
	nome: Optional[str] = None
	codigo_ean: Optional[str] = None
	quantidade_minima: Optional[int] = None
	preco_custo_unitario: Optional[float] = None
	preco_venda_unitario: Optional[float] = None
	precisa_receita: Optional[bool] = None


class MedicamentoResponse(BaseModel):
	"""Schema de resposta do medicamento"""
	id: int
	nome: str
	codigo_ean: str
	principio_ativo: str
	apresentacao: str
	fabricante: str
	preco_custo_unitario: float
	preco_venda_unitario: float
	quantidade_minima: int
	precisa_receita: bool
	ativo: bool

	class Config:
		from_attributes = True


# ============ COMPRA SCHEMAS ============

class CompraCreate(BaseModel):
	"""Schema para criar compra"""
	fornecedor_id: int = Field(..., gt=0)
	codigo_pedido: str = Field(..., min_length=1)
	data_entrega_esperada: datetime


class ItemCompraCreate(BaseModel):
	"""Schema para adicionar item à compra"""
	medicamento_id: int = Field(..., gt=0)
	quantidade_solicitada: int = Field(..., gt=0)
	preco_unitario: float = Field(..., gt=0)


class ItemCompraReceber(BaseModel):
	"""Schema para receber item de compra"""
	quantidade_recebida: int = Field(..., gt=0)
	numero_lote: str = Field(..., min_length=1)
	data_validade: datetime


class CompraReceber(BaseModel):
	"""Schema para marcar compra como recebida"""
	numero_nf: Optional[str] = None
	data_nf: Optional[datetime] = None


class CompraResponse(BaseModel):
	"""Schema de resposta da compra"""
	id: int
	codigo_pedido: str
	fornecedor_id: int
	status: str
	data_pedido: datetime
	valor_total: float

	class Config:
		from_attributes = True


# ============ ALERTA SCHEMAS ============

class AlertaResolverRequest(BaseModel):
	"""Schema para resolver alerta"""
	observacao: Optional[str] = None
