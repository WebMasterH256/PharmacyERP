# 🔧 Troubleshooting - Problemas Comuns

## ❌ Problema 1: CORS Error

**Erro que você vê:**
```
Access to XMLHttpRequest at 'http://localhost:8000/relatorios/dashboard' 
from origin 'http://localhost:5500' has been blocked by CORS policy
```

**Causa:**
A API não está respondendo requisições do frontend

**Solução:**

1. **Verifique se a API está rodando:**
   ```powershell
   # Na Terminal 1, procure por:
   INFO:     Application startup complete
   ```

2. **Verifique o script.js:**
   - Abra `API/script.js`
   - Procure pela linha: `const API_URL = 'http://localhost:8000'`
   - Se não estiver lá, o arquivo não foi atualizado corretamente

3. **Reinicie tudo:**
   ```powershell
   # Terminal 1 (Ctrl+C para parar)
   # Depois:
   python -m uvicorn API.main:app --reload --host 0.0.0.0 --port 8000
   
   # Terminal 2 (Ctrl+C para parar)
   # Depois:
   python -m http.server 5500 --directory ./API
   
   # Navegador: Ctrl+Shift+R (hard refresh)
   ```

---

## ❌ Problema 2: API Retorna 404

**Erro que você vê:**
```json
{"detail":"Not Found"}
```

**Causa:**
O endpoint não existe ou a URL está errada

**Solução:**

1. **Verifique os endpoints disponíveis:**
   ```
   http://localhost:8000/docs
   ```
   
   Você deve ver uma lista completa de endpoints

2. **Teste um endpoint simples:**
   ```
   http://localhost:8000/
   ```
   
   Deve retornar: `{"status":"ok"}`

3. **Se não funcionar, a API pode estar down:**
   - Verifique se a API está realmente rodando
   - Olhe erros na Terminal 1

---

## ❌ Problema 3: Frontend não carrega

**Erro que você vê:**
```
Cannot GET /
```

**Causa:**
O arquivo `index.html` não está sendo servido

**Solução:**

```powershell
# Verifique que o arquivo existe:
ls C:\Users\Vinicius\Desktop\ERPPharmacy\API\index.html

# Se não existir, você tem um problema maior

# Se existir, a Terminal 2 pode estar com problema:
# Ctrl+C na Terminal 2

# Rode novamente com atenção ao --directory:
python -m http.server 5500 --directory ./API

# Verifique que diz:
# Serving HTTP on 0.0.0.0 port 5500
```

---

## ❌ Problema 4: Porta já em uso

**Erro que você vê:**
```
ERROR: Address already in use
```

**Causa:**
Algo já está usando a porta 5500 ou 8000

**Solução:**

**Para Terminal 1 (API porta 8000):**
```powershell
# Encontrar o que está usando a porta 8000:
netstat -ano | findstr :8000

# Se encontrar, execute:
taskkill /PID <NUMERO_DO_PID> /F

# OU use uma porta diferente:
python -m uvicorn API.main:app --reload --host 0.0.0.0 --port 8001
```

**Para Terminal 2 (Frontend porta 5500):**
```powershell
# Use outra porta:
python -m http.server 5501 --directory ./API

# Depois acesse:
# http://localhost:5501
```

---

## ❌ Problema 5: DevTools mostra erro 500 na API

**Erro que você vê:**
```
GET /relatorios/dashboard 500 Internal Server Error
```

**Causa:**
Há um erro no código Python da API

**Solução:**

1. **Olhe a Terminal 1:**
   ```
   Traceback (most recent call last):
     File "...", line X, in <function>
   ERROR: ...
   ```

2. **Identifique o erro** (geralmente está escrito lá)

3. **Se não conseguir resolver:**
   - Verifique se `main.py` foi modificado incorretamente
   - Restaure o arquivo original
   - Rode novamente

---

## ❌ Problema 6: Dados não aparecem nos KPI Cards

**Sintomas:**
- Notificação diz "Dados carregados com sucesso!"
- Mas os cards continuam vazios

**Causa:**
A função `updateKPIWithData()` não está funcionando corretamente

**Solução:**

1. **Abra DevTools (F12)**
2. **Na aba Console, procure por:**
   ```javascript
   console.log('KPI Values:', data);
   ```

3. **Se não ver nada, os dados não estão sendo retornados:**
   - Vá para a aba Network
   - Procure a requisição `/relatorios/dashboard`
   - Clique nela
   - Vá para Response
   - Veja os dados retornados

4. **Se os dados estão lá, é um problema do updateKPIWithData():**
   - Verifique se os seletores CSS estão corretos:
     ```javascript
     .kpi-primary .kpi-value
     .kpi-success .kpi-value
     .kpi-warning .kpi-value
     .kpi-danger .kpi-value
     ```

---

## ❌ Problema 7: Gráfico não aparece

**Sintomas:**
- Tudo carrega menos o gráfico

**Causa:**
Chart.js não está carregando ou há erro no contexto do canvas

**Solução:**

1. **Verifique a CDN no HTML:**
   ```html
   <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/3.9.1/chart.min.js"></script>
   ```

2. **DevTools > Network > Procure por chart.min.js**
   - Se status for 404, a CDN está down
   - Tente recarregar a página

3. **DevTools > Console > Procure por erros:**
   ```
   Uncaught ReferenceError: Chart is not defined
   ```
   - Significa que Chart.js não carregou

4. **Verifique se o canvas existe:**
   ```html
   <canvas id="salesChart"></canvas>
   ```
   - Deve estar no HTML

---

## ✅ Checklist de Troubleshooting

Se nada funcionar:

- [ ] Terminal 1 rodando (api em 8000)
- [ ] Terminal 2 rodando (frontend em 5500)
- [ ] Navegador consegue acessar http://localhost:5500
- [ ] Arquivo index.html existe em API/
- [ ] Arquivo script.js foi atualizado com const API_URL
- [ ] DevTools Console não mostra erros vermelhos
- [ ] DevTools Network mostra requisições 200 para endpoints
- [ ] Network tem GET /relatorios/dashboard com Response JSON

---

## 🎯 Debug passo a passo

Se não conseguiu resolver com os passos acima:

1. **Reinicie tudo do zero:**
   ```powershell
   # Feche as 2 terminais (Ctrl+C em cada uma)
   # Feche o navegador (ou Ctrl+W)
   
   # Abra Terminal 1 novo:
   cd C:\Users\Vinicius\Desktop\ERPPharmacy
   .\.venv\Scripts\Activate.ps1
   python -m uvicorn API.main:app --reload --host 0.0.0.0 --port 8000
   
   # Espere 3 segundos
   # Abra Terminal 2 novo:
   cd C:\Users\Vinicius\Desktop\ERPPharmacy
   python -m http.server 5500 --directory ./API
   
   # Espere 2 segundos
   # Abra navegador e vá para http://localhost:5500
   ```

2. **Se ainda não funcionar:**
   - Tire um screenshot do erro
   - Copie o erro exato da Terminal 1 ou DevTools
   - Compare com a seção "Problemas Comuns" acima

---

## 📞 Resumo Rápido

| Erro | Solução |
|------|---------|
| CORS Error | API não está rodando |
| 404 Not Found | Endpoint errado ou API down |
| Cannot GET / | Terminal 2 não está rodando |
| Address already in use | Porta em uso, use outra |
| 500 Internal Server Error | Erro no código Python |
| Dados não aparecem | updateKPIWithData() não funciona |
| Gráfico não aparece | Chart.js não carregou |

---

## 🆘 Se Nada Funcionou

1. **Verifique o Requirements.txt:**
   ```powershell
   cat Requirements.txt
   
   # Deve ter:
   fastapi
   uvicorn
   pydantic
   ```

2. **Reinstale dependências:**
   ```powershell
   pip install -r Requirements.txt --upgrade
   ```

3. **Recrie o ambiente virtual:**
   ```powershell
   # Desative
   deactivate
   
   # Delete a pasta .venv
   rmdir -r .venv
   
   # Recrie:
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r Requirements.txt
   ```

4. **Se ainda não funcionar:**
   - Reinstale Python 3.9+
   - Atualize pip: `pip install --upgrade pip`
   - Tente novamente

---

**Boa sorte! 🍀**
