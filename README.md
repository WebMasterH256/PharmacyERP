# 🏥 PharmacyERP

Um sistema de gestão de compra de suprimentos para farmácias, desenvolvido como projeto de portfólio em Python com FastAPI, SQLAlchemy e SQLite.

## 🎯 Objetivo

Demonstrar conhecimento em desenvolvimento backend profissional através de um sistema real que gerencia:
- Medicamentos com rastreamento por EAN
- Lotes com controle de validade (crítico em farmácia)
- Compras e recebimento de fornecedores
- Sistema de alertas automáticos (estoque baixo, vencimento, produtos parados)
- Relatórios e dashboard

## ✨ Features

### 📦 Gestão de Estoque
- Cálculo automático de estoque total consolidando todos os lotes
- Validação de quantidade antes de vender
- Processamento de vendas em ordem FIFO (primeiro a vencer, primeiro a sair)
- Previsão de dias até faltar baseada em histórico

### 🚨 Sistema de Alertas
- **Estoque Baixo**: Quando quantidade < mínimo configurado
- **Próximo Vencimento**: Lotes vencendo em até 30 dias
- **Já Vencido**: Lotes expirados (CRÍTICO - compliance)
- **Produto Parado**: Medicamentos sem venda há 60 dias

### 🛒 Gestão de Compras
- Criação de pedidos ao fornecedor
- Recebimento parcial de itens
- Criação automática de lotes no recebimento
- Rastreabilidade completa

### 📊 Relatórios e Dashboard
- Dashboard geral com KPIs
- Análise de vencimentos
- Estoque por medicamento
- Resumo de compras
- Exportação consolidada

## 🏗️ Arquitetura

Projeto estruturado em **4 camadas** separando responsabilidades:

```
┌─────────────────────────────────────┐
│      API / Routes (FastAPI)         │ ← HTTP Endpoints
├─────────────────────────────────────┤
│   Services (Lógica de Negócio)      │ ← Regras farmacêuticas
├─────────────────────────────────────┤
│   Repositories (Acesso a Dados)     │ ← Queries ao BD
├─────────────────────────────────────┤
│   Domain + Infrastructure (BD)      │ ← Modelos e DB
└─────────────────────────────────────┘
```

### Domain
- **6 Entidades**: Medicamento, Lote, Fornecedor, Compra, ItemCompra, Alerta
- Relacionamentos 1:N com integridade referencial
- Timestamps automáticos (created_at, updated_at)
- Type hints 100%

### Infrastructure
- SQLAlchemy ORM com SQLite
- Session factory para dependency injection
- Migrations ready (Alembic compatible)
- Circular imports resolvidos com TYPE_CHECKING

### Repositories (7 classes)
- **BaseRepository**: CRUD genérico herdado por todos
- **MedicamentoRepository**: Buscas por EAN, nome, estoque baixo
- **LoteRepository**: Lotes vencidos, próximos vencimento, FIFO, agregações
- **FornecedorRepository**: CNPJ, nome, fornecedor ativo
- **CompraRepository**: Status, período, fornecedor
- **ItemCompraRepository**: Por compra, pendentes receber
- **AlertaRepository**: Por tipo, urgência, não resolvidos

### Services (5 classes)
- **EstoqueService**: Cálculos, validações, previsões
- **AlertaService**: Geração e resolução de alertas
- **CompraService**: Pedidos e recebimento
- **MedicamentoService**: CRUD com validações
- **RelatorioService**: Dados consolidados

## 🛠️ Tech Stack

| Camada | Tecnologia |
|--------|-----------|
| **Backend** | Python 3.14 |
| **Framework Web** | FastAPI |
| **Banco de Dados** | SQLAlchemy + SQLite |
| **Validação** | Pydantic |
| **Migrations** | Alembic (ready to use) |
| **Type Hints** | 100% com mypy |

## 📋 Estrutura do Projeto

```
PharmacyERP/
├── Domain/
│   ├── Enums/
│   │   ├── StatusCompra.py
│   │   ├── StatusLote.py
│   │   ├── TipoAlerta.py
│   │   └── Urgencia.py
│   ├── Base.py
│   ├── Medicamento.py
│   ├── Lote.py
│   ├── Fornecedor.py
│   ├── Compra.py
│   ├── ItemCompra.py
│   └── Alerta.py
│
├── Infrastructure/
│   ├── database.py
│   ├── __init__.py
│   └── repositories/
│       ├── base_repository.py
│       ├── medicamento_repository.py
│       ├── lote_repository.py
│       ├── fornecedor_repository.py
│       ├── compra_repository.py
│       ├── item_compra_repository.py
│       └── alerta_repository.py
│
├── Application/
│   └── services/
│       ├── estoque_service.py
│       ├── alerta_service.py
│       ├── compra_service.py
│       ├── medicamento_service.py
│       └── relatorio_service.py
│
├── API/
│   └── routes/
│       ├── medicamentos.py
│       ├── lotes.py
│       ├── compras.py
│       ├── alertas.py
│       └── relatorios.py
│
├── config.py
├── main.py
├── requirements.txt
└── README.md
```

## 🚀 Como Rodar

### Pré-requisitos
- Python 3.14+
- pip

### Instalação

1. Clone o repositório
```bash
git clone https://github.com/WebMasterH256/PharmacyERP.git
cd PharmacyERP
```

2. Crie um ambiente virtual
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. Instale as dependências
```bash
pip install -r requirements.txt
```

4. Rode o servidor
```bash
python main.py
```

O servidor estará disponível em `http://localhost:8000`

### Documentação da API
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📚 Exemplos de Uso

### Criar um Medicamento
```python
from Infrastructure.database import SessionLocal
from Application.services import MedicamentoService

db = SessionLocal()
service = MedicamentoService(db)

resultado = service.criar_medicamento(
    nome="Dipirona 500mg",
    codigo_ean="7896045401234",
    principio_ativo="Dipirona Monoidratada",
    apresentacao="Comprimido",
    fabricante="Laboratório Genérico",
    quantidade_minima=50,
    preco_custo_unitario=0.50,
    preco_venda_unitario=2.50,
    precisa_receita=False
)
print(resultado)  # {'sucesso': True, 'mensagem': '...', 'medicamento_id': 1}
```

### Processar uma Venda
```python
from Application.services import EstoqueService

service = EstoqueService(db)

# Validar antes de vender
validacao = service.pode_vender(medicamento_id=1, quantidade=100)
if validacao['pode']:
    # Processar venda FIFO
    resultado = service.processar_venda(medicamento_id=1, quantidade=100)
    print(resultado)  # {'sucesso': True, 'lotes_afetados': [1, 2], ...}
```

### Gerar Alertas
```python
from Application.services import AlertaService

service = AlertaService(db)

# Gerar todos os alertas automáticos
resultado = service.gerar_todos_os_alertas()
print(resultado)
# {
#     'estoque_baixo': 3,
#     'proximo_vencimento': 5,
#     'ja_vencido': 1,
#     'produto_parado': 0,
#     'total': 9
# }
```

## 🎓 Aprendizados Técnicos

### 1. Circular Imports em Python
Python executa código no import (diferente de Java/C# que apenas compilam). Resolvido com:
- `TYPE_CHECKING` para imports condicional
- Forward references com strings em `relationship()`

### 2. Padrão Repository
Encapsula lógica de acesso a dados:
- Métodos complexos ficam reutilizáveis
- Fácil de testar (mock repositories)
- Isolamento de mudanças no BD

### 3. Padrão Service
Implementa regras de negócio combinando repositórios:
- Validações complexas (EAN único, preço válido, estoque real)
- Operações multi-tabela (vender deduz de lotes em FIFO)
- Lógica que seria perigosa em controllers

### 4. FIFO em Farmácia
Crítico vender lotes mais antigos primeiro para evitar vencimentos. EstoqueService.processar_venda() implementa isso automaticamente.

## 📈 Status do Projeto

| Camada | Status |
|--------|--------|
| Domain | ✅ Completo |
| Infrastructure | ✅ Completo |
| Repositories | ✅ Completo |
| Services | ✅ Completo |
| API Routes | 🔄 Em progresso |
| Frontend | ⏳ Planejado |
| Testes | ⏳ Planejado |
| Deploy | ⏳ Planejado |

## 🔮 Próximos Passos

1. **API Routes** (FastAPI endpoints)
    - CRUD endpoints para cada entidade
    - Documentação Swagger automática
    - Error handling robusto

2. **Frontend** (HTML/CSS/JavaScript)
    - Dashboard com gráficos
    - Gerenciamento de medicamentos
    - Alertas em tempo real

3. **Testes**
    - Testes unitários (pytest)
    - Testes de integração
    - Coverage > 80%

4. **Melhorias**
    - Autenticação e autorização
    - Paginação em endpoints
    - Cache com Redis
    - Logging estruturado
    - CI/CD com GitHub Actions

## 📖 Documentação

- [Architecture.md](./docs/ARCHITECTURE.md) - Detalhes da arquitetura
- [API.md](./docs/API.md) - Documentação dos endpoints (em breve)
- [Services.md](./docs/SERVICES.md) - Guia de services (em breve)

## 🤝 Contribuições

Este é um projeto de portfólio, mas sugestões são bem-vindas!

Se você tiver ideias de melhorias ou encontrou algum bug, abra uma issue ou envie um PR.

## 📄 Licença

MIT License - veja [LICENSE](./LICENSE) para detalhes

## 👨‍💻 Autor

**Mateus Siqueira** - [GitHub](https://github.com/WebMasterH256) | [LinkedIn](https://linkedin.com/in/mateus-siqueira)

---

⭐ Se esse projeto foi útil, considere dar uma estrela! Isso ajuda outros a descobrir.

Desenvolvido como projeto de portfólio para demonstrar conhecimento em:
- Arquitetura de software em camadas
- Python profissional com type hints
- SQLAlchemy ORM
- Design Patterns (Repository, Service, Factory)
- Lógica de negócio complexa