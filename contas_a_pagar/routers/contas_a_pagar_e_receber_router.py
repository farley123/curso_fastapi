
from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from enum import Enum
from sqlalchemy.orm import Session
from contas_a_pagar.models.conta_a_pagar_receber_model import ContaPagarReceber
from contas_a_pagar.models.fornecedor_cliente_model import FornecedorCliente
from contas_a_pagar.routers.fornecedor_cliente_router import FornecedorClienteResponse
from shared.dependencies import get_db
from shared.exceptions import NotFound


router = APIRouter(prefix="/contas-a-pagar-e-receber")


class ContaPagarReceberResponse(BaseModel):
    id: int
    descricao: str
    valor: float
    tipo: str
    fornecedor:FornecedorClienteResponse|None =None


class ContaPagarReceberTipoEnum(str, Enum):
    PAGAR = "PAGAR"
    RECEBER = "RECEBER"


class ContaPagarReceberRequest(BaseModel):
    descricao: str = Field(min_length=3, max_length=30)
    valor: float = Field(gt=0.0)
    tipo: ContaPagarReceberTipoEnum
    fornecedor_cliente_id:int | None=None


@router.get("/", response_model=List[ContaPagarReceberResponse])
def listar_contas(db: Session = Depends(get_db)):
    return db.query(ContaPagarReceber).all()


@router.get("/{id_conta}", response_model=ContaPagarReceberResponse)
def obter_conta(id_conta: int, db: Session = Depends(get_db)):
    contasAPagarEReceber= busca_conta_por_id(id_conta,db)
    return contasAPagarEReceber


@router.post("/", response_model=ContaPagarReceberResponse, status_code=201)
def criar_conta(conta: ContaPagarReceberRequest, db: Session = Depends(get_db)):
    conta_a_pagar_receber = ContaPagarReceber(
        descricao=conta.descricao, valor=conta.valor, tipo=conta.tipo,fornecedor_cliente_id=conta.fornecedor_cliente_id
    )
    valida_fornecedor(conta.fornecedor_cliente_id, db)

    db.add(conta_a_pagar_receber)
    db.commit()
    db.refresh(conta_a_pagar_receber)
    return ContaPagarReceberResponse(**conta_a_pagar_receber.__dict__)


def valida_fornecedor(fornecedor_cliente_id, db: Session) -> Any | None:
    if fornecedor_cliente_id is not None:
        conta_a_pagar_receber = db.query(FornecedorCliente).get(fornecedor_cliente_id)
        if conta_a_pagar_receber is None:
            raise HTTPException(status_code=422, detail="esse fornecedor nao existe no banco de dados")



@router.put("/{id_conta}", response_model=ContaPagarReceberResponse, status_code=200)
def criar_conta(
    id_conta: int, conta: ContaPagarReceberRequest, db: Session = Depends(get_db)
):
    valida_fornecedor(conta.fornecedor_cliente_id, db)
    conta_a_pagar_receber = busca_conta_por_id(id_conta,db)
    conta_a_pagar_receber.tipo = conta.tipo
    conta_a_pagar_receber.descricao = conta.descricao
    conta_a_pagar_receber.valor = conta.valor
    conta_a_pagar_receber.fornecedor_cliente_id = conta.fornecedor_cliente_id
    db.add(conta_a_pagar_receber)
    db.commit()
    db.refresh(conta_a_pagar_receber)
    return conta_a_pagar_receber


@router.delete("/{id_conta}", status_code=200)
def criar_conta(id_conta: int, db: Session = Depends(get_db)):
    conta =busca_conta_por_id(id_conta,db)
    db.delete(conta)
    db.commit()


def busca_conta_por_id(id:int,db:Session):
    conta= db.get(ContaPagarReceber,id)
    if conta is None:
        raise NotFound('Conta a pagar e receber')
    return conta    
