# ⚡ Quick Start - Resumo Rápido

## 🎯 Em 30 Segundos

```
Terminal 1:
$ python -m uvicorn API.main:app --reload --host 0.0.0.0 --port 8000

Terminal 2:
$ python -m http.server 5500 --directory ./API

Navegador:
http://localhost:5500
```

---

## 📋 Arquivo de Referência Rápida

### Arquivos Criados para Você

```
COMO_RODAR.md          ← Guia completo passo a passo
REVISAO_CODIGOS.md     ← Resultado da revisão
GUIA_VISUAL.md         ← Guia com diagrama visual  
TROUBLESHOOTING.md     ← Soluções para problemas
QUICK_START.md         ← Este arquivo aqui
```

---

## 🔍 O Que Mudou no Seu Código

### script.js - ANTES E DEPOIS

**ANTES:**
```javascript
// Sem fetch, sem conexão com API
// Dados eram hardcoded
```

**DEPOIS:**
```javascript
const API_URL = 'http://localhost:8000';

// Nova função que carrega dados da API
async function loadDashboardData() {
  const response = await fetch(`${API_URL}/relatorios/dashboard`);
  const data = await response.json();
  updateKPIWithData(data);
}

// Novas funções para carregar dados
async function loadMedicamentos() { ... }
async function loadLotes() { ... }
async function loadAlertas() { ... }
```

---

## ✅ Checklist de Início

- [ ] `.venv` ativado
- [ ] Terminal 1: FastAPI rodando em 8000
- [ ] Terminal 2: HTTP Server rodando em 5500
- [ ] Navegador: http://localhost:5500
- [ ] Notificação verde: "Dados carregados com sucesso!"
- [ ] KPI Cards com valores reais
- [ ] Gráfico animado

---

## 🚀 URLs Úteis

| URL | Descrição |
|-----|-----------|
| http://localhost:5500 | Sua aplicação |
| http://localhost:8000 | API raiz (status check) |
| http://localhost:8000/docs | Swagger (testar endpoints) |
| http://localhost:8000/relatorios/dashboard | Endpoint de dados |

---

## 💾 Comandos Importantes

```powershell
# Ativar ambiente virtual
.\.venv\Scripts\Activate.ps1

# Rodar API
python -m uvicorn API.main:app --reload --host 0.0.0.0 --port 8000

# Rodar Frontend
python -m http.server 5500 --directory ./API

# Instalar dependências
pip install -r Requirements.txt

# Listar dependências
pip list

# Atualizar pip
python -m pip install --upgrade pip
```

---

## 🎓 Próximas Etapas

1. **Adicionar mais páginas**
   - Estoque, Vendas, Clientes, Relatórios

2. **Conectar ao banco de dados real**
   - Usar as classes em Domain/
   - SQLAlchemy + PostgreSQL/MySQL

3. **Adicionar autenticação**
   - JWT, Login/Logout

4. **Deploy**
   - Docker, Heroku, AWS, Azure

---

## 📞 Ajuda Rápida

**API não conecta?**
- Verifique Terminal 1: "Application startup complete"
- Teste: http://localhost:8000/

**Frontend em branco?**
- Verifique Terminal 2: "Serving HTTP on..."
- Hard refresh: Ctrl+Shift+R

**Dados não aparecem?**
- Abra DevTools: F12
- Aba Network: procure /relatorios/dashboard
- Aba Console: procure mensagens de erro

**Porta em uso?**
- Use outra: python -m http.server 5501 --directory ./API
- Depois: http://localhost:5501

---

## 📁 Estrutura do Projeto

```
ERPPharmacy/
├── .venv/                 ← Ambiente virtual
├── .gitignore
├── config.py
├── LICENSE
├── README.md
├── Requirements.txt
│
├── COMO_RODAR.md          ← 📖 Guia completo
├── REVISAO_CODIGOS.md     ← ✅ Revisão
├── GUIA_VISUAL.md         ← 🎨 Visual
├── TROUBLESHOOTING.md     ← 🔧 Problemas
├── QUICK_START.md         ← ⚡ Este arquivo
│
├── API/
│   ├── main.py            ← API FastAPI ✅
│   ├── index.html         ← Frontend ✅
│   ├── script.js          ← JS com fetch ✅ CORRIGIDO
│   └── Style.css          ← CSS ✅
│
├── Application/
├── Domain/                ← Modelos de dados
│   ├── Alerta.py
│   ├── Medicamento.py
│   ├── Lote.py
│   ├── Fornecedor.py
│   ├── Compra.py
│   ├── ItemCompra.py
│   ├── Base.py
│   └── Enums/
│
└── Infrastructure/        ← Banco de dados
    └── database.py
```

---

## 🎯 Status Atual

| Componente | Status | Versão |
|-----------|--------|---------|
| FastAPI | ✅ OK | 0.104+ |
| HTML | ✅ OK | - |
| CSS | ✅ OK | - |
| JavaScript | ✅ CORRIGIDO | - |
| Fetch API | ✅ ADICIONADO | - |
| CORS | ✅ OK | - |

---

## 🌟 Dicas Pro

1. **Use Swagger para testar:**
   ```
   http://localhost:8000/docs
   ```

2. **DevTools é seu amigo:**
   - F12 > Console: veja logs
   - F12 > Network: veja requisições
   - F12 > Application > LocalStorage: veja dados salvos

3. **Hard refresh no navegador:**
   - Ctrl+Shift+R (não apenas Ctrl+R)

4. **Para desativar o .venv:**
   ```powershell
   deactivate
   ```

---

## 📊 Fluxo de Dados

```
Navegador (localhost:5500)
        ↓
index.html + script.js
        ↓
fetch() → GET /relatorios/dashboard
        ↓
API (localhost:8000)
        ↓
Retorna JSON com dados
        ↓
updateKPIWithData(data)
        ↓
HTML atualiza com dados reais
```

---

## ✨ Tudo Pronto!

Siga os 3 passos no topo dessa página e em 1 minuto você terá tudo funcionando.

**Bem-vindo ao PharmacyERP! 🏥**
