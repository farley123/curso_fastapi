from fastapi import FastAPI
import uvicorn
from shared.database import engine, Base

from contas_a_pagar.routers import contas_a_pagar_e_receber_router
from contas_a_pagar.models.conta_a_pagar_receber_model import ContaPagarReceber

# Base.metadata.drop_all(bind=engine)
# Base.metadata.create_all(bind=engine)
app = FastAPI()


@app.get("/")
def hello_world() -> str:
    return "Hello World FastApi!!!"


app.include_router(contas_a_pagar_e_receber_router.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
