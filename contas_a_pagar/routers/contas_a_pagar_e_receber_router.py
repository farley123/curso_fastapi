from decimal import Decimal
from typing import List, Dict
from fastapi import APIRouter
from pydantic import BaseModel


router = APIRouter(prefix="/contas-a-pagar-e-receber")


class ContaPagarReceberResponse(BaseModel):
    id: int
    descricao: str
    valor: float
    tipo: str


class ContaPagarReceberRequest(BaseModel):
    descricao: str
    valor: float
    tipo: str


@router.get("/", response_model=List[ContaPagarReceberResponse])
def listar_contas():
    return [
        ContaPagarReceberResponse(
            id=1, descricao="Aluguel", valor=1000.5, tipo="Pagar"
        ),
        ContaPagarReceberResponse(
            id=2, descricao="salario", valor=5000.0, tipo="Receber"
        ),
    ]


@router.post("/", response_model=ContaPagarReceberResponse, status_code=201)
def criar_conta(conta: ContaPagarReceberRequest):
    return ContaPagarReceberResponse(
        id=3, descricao=conta.descricao, valor=conta.valor, tipo=conta.tipo
    )
