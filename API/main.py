from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import datetime

app = FastAPI(
    title="PharmacyERP API (Mock)",
    description="Endpoints temporários para desenvolvimento do Frontend em paralelo."
)

# ==============================================================================
# CONFIGURAÇÃO DE CORS (MUITO IMPORTANTE PARA O FRONTEND)
# ==============================================================================
# O CORS permite que o frontend (rodando em http://localhost:3000 ou 5500, por exemplo)
# consiga fazer requisições para esta API sem ser bloqueado pelo navegador.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, você limitará isso para a URL do seu frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==============================================================================
# ENDPOINTS DE MEDICAMENTOS
# Mapeados a partir da classe Medicamento[cite: 10]
# ==============================================================================

@app.get("/medicamentos")
def listar_medicamentos():
    return [
        {
            "id": 1,
            "nome": "Dipirona 500mg",
            "codigo_ean": "7896045401234",
            "principio_ativo": "Dipirona Monoidratada",
            "apresentacao": "Comprimido",
            "fabricante": "Laboratório Genérico",
            "quantidade_minima": 50,
            "preco_custo_unitario": 0.50,
            "preco_venda_unitario": 2.50,
            "precisa_receita": False,
            "ativo": True
        },
        {
            "id": 2,
            "nome": "Amoxicilina 500mg",
            "codigo_ean": "7891234567890",
            "principio_ativo": "Amoxicilina",
            "apresentacao": "Cápsula",
            "fabricante": "MedFarma",
            "quantidade_minima": 20,
            "preco_custo_unitario": 5.00,
            "preco_venda_unitario": 15.00,
            "precisa_receita": True,
            "ativo": True
        }
    ]

@app.get("/medicamentos/{medicamento_id}")
def obter_medicamento(medicamento_id: int):
    # Retorna um item fixo apenas para o frontend conseguir testar o fluxo de "detalhes"
    return {
        "id": medicamento_id,
        "nome": "Dipirona 500mg",
        "codigo_ean": "7896045401234",
        "principio_ativo": "Dipirona Monoidratada",
        "apresentacao": "Comprimido",
        "fabricante": "Laboratório Genérico",
        "quantidade_minima": 50,
        "preco_custo_unitario": 0.50,
        "preco_venda_unitario": 2.50,
        "precisa_receita": False,
        "ativo": True
    }

@app.post("/medicamentos")
def criar_medicamento(dados: dict):
    # Simula a criação devolvendo o que o frontend enviou, mas injetando um ID falso
    resposta = dados.copy()
    resposta["id"] = 999
    return resposta

# ==============================================================================
# ENDPOINTS DE LOTES
# Mapeados a partir da classe Lote[cite: 9]
# ==============================================================================

@app.get("/lotes")
def listar_lotes():
    return [
        {
            "id": 1,
            "codigo_lote": "2024-ABC-001",
            "medicamento_id": 1,
            "fornecedor_id": 1,
            "data_fabricacao": "2024-01-15T00:00:00",
            "data_validade": "2026-01-15T00:00:00",
            "quantidade_inicial": 1000,
            "quantidade_vendida": 250,
            "quantidade_disponivel": 750, # Propriedade calculada incluída no JSON[cite: 9]
            "preco_unitario": 0.50,
            "status": "ATIVO",
            "data_recebimento": "2024-01-20T14:30:00"
        }
    ]

# ==============================================================================
# ENDPOINTS DE ALERTAS
# Mapeados a partir da classe Alerta[cite: 5]
# ==============================================================================

@app.get("/alertas")
def listar_alertas():
    return [
        {
            "id": 1,
            "medicamento_id": 2,
            "lote_id": None,
            "tipo": "ESTOQUE_BAIXO",
            "urgencia": "ALTA",
            "mensagem": "Amoxicilina 500mg atingiu o estoque mínimo (restam 5 unidades).",
            "resolvido": False,
            "observacao": "Fazer pedido com urgência",
            "data_resolucao": None
        },
        {
            "id": 2,
            "medicamento_id": 1,
            "lote_id": 1,
            "tipo": "VENCIMENTO_PROXIMO",
            "urgencia": "MEDIA",
            "mensagem": "Lote 2024-ABC-001 de Dipirona vence em 60 dias.",
            "resolvido": False,
            "observacao": None,
            "data_resolucao": None
        }
    ]

# ==============================================================================
# ENDPOINT DE DASHBOARD (RELATÓRIOS)
# ==============================================================================

@app.get("/relatorios/dashboard")
def dashboard():
    return {
        "resumo": {
            "total_medicamentos_ativos": 142,
            "alertas_pendentes": 2,
            "lotes_vencendo_30_dias": 5,
            "compras_em_transito": 3
        },
        "financeiro_mes": {
            "receita_bruta": 15400.50,
            "custo_produtos_vendidos": 6200.00,
            "lucro_bruto": 9200.50
        },
        "produtos_mais_vendidos": [
            {"id": 1, "nome": "Dipirona 500mg", "quantidade_vendida": 250},
            {"id": 5, "nome": "Ibuprofeno 400mg", "quantidade_vendida": 180}
        ]
    }