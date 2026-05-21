from typing import TYPE_CHECKING # CARALHO EU ODEIO TYPE_CHECKING AAAAAAAAAAAAAAAAAAAA

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from Infrastructure.database import init_db

from API.controllers.medicamentos_routes import router as medicamentos_router
from API.controllers.alertas_routes import router as alertas_router
from API.controllers.lotes_routes import router as lotes_router
from API.controllers.compras_routes import router as compras_router
from API.controllers.relatorios_routes import router as relatorios_router

from Domain.Fornecedor import Fornecedor

app = FastAPI(
    title="PharmacyERP API",
    description="API para gestão de suprimentos de farmácias",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  #TODO: Mudar para o domínio http://localhost:5500 quando em produção
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    init_db()

app.include_router(medicamentos_router)
app.include_router(alertas_router)
app.include_router(lotes_router)
app.include_router(compras_router)
app.include_router(relatorios_router)

@app.get("/")
def root():
    return {"status": "ok", "mensagem": "PharmacyERP API rodando com sucesso!"}

# Bloco para permitir execução direta via Python
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("API.main:app", host="0.0.0.0", port=8000, reload=True)