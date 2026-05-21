# 📚 Documentação da API

A API do PharmacyERP é construída com FastAPI e oferece documentação automática via Swagger.

## 🚀 Como Iniciar

```bash
python main.py
```

A API estará disponível em `http://localhost:8080`

### Documentação Interativa
- **Swagger UI**: http://localhost:8080/docs
- **ReDoc**: http://localhost:8080/redoc
- **JSON Schema**: http://localhost:8080/openapi.json

---

## 📋 Endpoints Disponíveis

### 🏥 Medicamentos (`/api/medicamentos`)

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/` | Criar novo medicamento |
| GET | `/` | Listar medicamentos ativos |
| GET | `/{medicamento_id}` | Obter detalhes do medicamento |
| GET | `/buscar?termo=...` | Buscar por nome ou EAN |
| PUT | `/{medicamento_id}` | Atualizar medicamento |
| DELETE | `/{medicamento_id}` | Desativar medicamento |
| GET | `/estoque/baixo/` | Medicamentos com estoque baixo |

#### Exemplo: Criar medicamento
```bash
curl -X POST "http://localhost:8000/api/medicamentos/" \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Dipirona 500mg",
    "codigo_ean": "7896045401234",
    "principio_ativo": "Dipirona Monoidratada",
    "apresentacao": "Comprimido",
    "fabricante": "Laboratório Genérico",
    "quantidade_minima": 50,
    "preco_custo_unitario": 0.50,
    "preco_venda_unitario": 2.50,
    "precisa_receita": false
  }'
```

---

### 📦 Lotes (`/api/lotes`)

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/medicamento/{medicamento_id}` | Lotes de um medicamento |
| GET | `/vencidos/` | Lotes já vencidos |
| GET | `/proximos-vencer/?dias=30` | Lotes vencendo em X dias |
| GET | `/{lote_id}` | Detalhes do lote |
| PUT | `/{lote_id}/marcar-vencido` | Marcar lote como vencido |
| PUT | `/{lote_id}/marcar-descartado` | Marcar lote como descartado |
| GET | `/estoque/total-medicamento/{medicamento_id}` | Estoque total consolidado |

---

### 🛒 Compras (`/api/compras`)

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/` | Criar nova compra |
| POST | `/{compra_id}/itens` | Adicionar item à compra |
| POST | `/itens/{item_compra_id}/receber` | Receber item (cria lote) |
| GET | `/` | Listar compras |
| GET | `/{compra_id}` | Detalhes da compra |
| GET | `/pendentes/` | Compras ainda não recebidas |
| PUT | `/{compra_id}/receber` | Marcar compra como recebida |
| DELETE | `/{compra_id}` | Cancelar compra pendente |

#### Exemplo: Criar compra
```bash
curl -X POST "http://localhost:8000/api/compras/" \
  -H "Content-Type: application/json" \
  -d '{
    "fornecedor_id": 1,
    "codigo_pedido": "PED-2024-001",
    "data_entrega_esperada": "2024-02-15T00:00:00"
  }'
```

---

### 🚨 Alertas (`/api/alertas`)

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/gerar-todos` | Gerar todos os tipos de alerta |
| POST | `/gerar-estoque-baixo` | Gerar alertas de estoque baixo |
| POST | `/gerar-vencimento?dias=30` | Gerar alertas de vencimento |
| POST | `/gerar-vencidos` | Gerar alertas de vencidos (CRÍTICO) |
| GET | `/nao-resolvidos/` | Alertas pendentes de resolução |
| GET | `/por-tipo?tipo=ESTOQUE_BAIXO` | Filtrar por tipo |
| GET | `/por-urgencia?urgencia=CRITICO` | Filtrar por urgência |
| GET | `/{alerta_id}` | Detalhes do alerta |
| PUT | `/{alerta_id}/resolver` | Marcar alerta como resolvido |
| GET | `/` | Resumo de alertas para dashboard |

#### Exemplo: Gerar alertas
```bash
curl -X POST "http://localhost:8000/api/alertas/gerar-todos"
```

---

### 📊 Relatórios (`/api/relatorios`)

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/dashboard` | Dashboard principal com KPIs |
| GET | `/estoque` | Relatório detalhado de estoque |
| GET | `/vencimentos?dias=30` | Análise de vencimentos |
| GET | `/top-medicamentos?limite=10` | Medicamentos com maior estoque |
| GET | `/alertas-por-tipo` | Distribuição de alertas |
| GET | `/compras` | Resumo de compras |
| GET | `/completo` | Relatório completo consolidado |
| GET | `/medicamento/{medicamento_id}` | Análise detalhada de medicamento |
| GET | `/fornecedor/{fornecedor_id}` | Análise de fornecedor |
| GET | `/health` | Verificação de status |

#### Exemplo: Dashboard
```bash
curl "http://localhost:8080/api/relatorios/dashboard"
```

---

## 🔄 Fluxo Típico de Uso

### 1. Criar Medicamento
```
POST /api/medicamentos
→ medicamento_id = 1
```

### 2. Criar Compra
```
POST /api/compras
→ compra_id = 1
```

### 3. Adicionar Item à Compra
```
POST /api/compras/1/itens
medicamento_id = 1, quantidade = 100, preco = 0.50
→ item_compra_id = 1
```

### 4. Receber Item (Cria Lote)
```
POST /api/compras/itens/1/receber
quantidade_recebida = 100, numero_lote = "LOTE001", data_validade = "2025-12-31"
→ lote_id = 1
```

### 5. Gerar Alertas
```
POST /api/alertas/gerar-todos
```

### 6. Processar Venda (via Service, não tem endpoint direto)
```
EstoqueService.processar_venda(medicamento_id=1, quantidade=10)
→ Deduz de lotes em ordem FIFO
```

### 7. Consultar Dashboard
```
GET /api/relatorios/dashboard
```

---

## 🔐 Autenticação

Atualmente, não há autenticação. Isso será adicionado em futuras versões.

---

## 📈 Códigos de Status HTTP

| Código | Significado |
|--------|-----------|
| 200 | OK - Requisição bem-sucedida |
| 201 | Created - Recurso criado |
| 400 | Bad Request - Erro na validação |
| 404 | Not Found - Recurso não encontrado |
| 500 | Internal Server Error - Erro do servidor |

---

## 💾 Estrutura de Resposta

### Sucesso
```json
{
  "sucesso": true,
  "mensagem": "Operação realizada com sucesso",
  "dados": { ... }
}
```

### Erro
```json
{
  "detail": "Mensagem de erro específica"
}
```

---

## 🧪 Testar Localmente

Use **Swagger UI** em `http://localhost:8080/docs` para testar os endpoints interativamente.

Ou use `curl`:
```bash
curl -X GET "http://localhost:8080/api/medicamentos/" \
  -H "accept: application/json"
```

---

## 📚 Mais Informações

Para detalhes sobre Services, Repositories e Domain, veja os arquivos na pasta `/docs`.
