from decimal import Decimal
from typing import List, Dict
from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from enum import Enum
from sqlalchemy.orm import Session

from contas_a_pagar.models import conta_a_pagar_receber_model
from contas_a_pagar.models.conta_a_pagar_receber_model import ContaPagarReceber
from shared.dependencies import get_db


router = APIRouter(prefix="/contas-a-pagar-e-receber")


class ContaPagarReceberResponse(BaseModel):
    id: int
    descricao: str
    valor: float
    tipo: str

class ContaPagarReceberTipoEnum(str,Enum):
    PAGAR = 'PAGAR'
    RECEBER = 'RECEBER'

class ContaPagarReceberRequest(BaseModel):
    descricao: str = Field(min_length=3,max_length=30)
    valor: float = Field(gt=0.0)
    tipo: ContaPagarReceberTipoEnum


@router.get("/", response_model=List[ContaPagarReceberResponse])
def listar_contas(db: Session = Depends(get_db)):
    return db.query(ContaPagarReceber).all()


@router.post("/", response_model=ContaPagarReceberResponse, status_code=201)
def criar_conta(conta: ContaPagarReceberRequest, db: Session = Depends(get_db)):
    conta_a_pagar_receber = ContaPagarReceber(
        descricao=conta.descricao, valor=conta.valor, tipo=conta.tipo
    )
    db.add(conta_a_pagar_receber)
    db.commit()
    db.refresh(conta_a_pagar_receber)
    return ContaPagarReceberResponse(**conta_a_pagar_receber.__dict__)
