from fastapi import FastAPI
import uvicorn
from contas_a_pagar.routers import contas_a_pagar_e_receber_router
from shared.exception_handler import not_found_handler
from shared.exceptions import NotFound


app = FastAPI()

 


@app.get("/")
def hello_world() -> str:
    return "Hello World FastApi!!!"


app.include_router(contas_a_pagar_e_receber_router.router)
app.add_exception_handler(NotFound,not_found_handler)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
