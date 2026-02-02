from typing import List
from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from starlette import status

from contas_a_pagar.models.fornecedor_cliente_model import FornecedorCliente
from shared.dependencies import get_db
from shared.exceptions import NotFound

router = APIRouter(prefix="/fornecedor-cliente")


class FornecedorClienteResponse(BaseModel):
    id: int
    nome: str




class FornecedorClienteRequest(BaseModel):
    nome: str = Field(min_length=3, max_length=255)


#########################rotas###################
@router.get("/", response_model=List[FornecedorClienteResponse])
def listar_fornecedor_cliente(db: Session = Depends(get_db)):
    return db.query(FornecedorCliente).all()


@router.get("/{id_do_fornecedor_cliente", response_model=List[FornecedorClienteResponse])
def obter_fornecedor_cliente_por_id(id_do_fornecedor_cliente: int, db: Session = Depends(get_db)) -> FornecedorCliente:
    return busca_fornecedor_cliente_por_id(id_do_fornecedor_cliente, db)


@router.post("/", response_model=FornecedorClienteResponse, status_code=status.HTTP_201_CREATED)
def criar_fornecedor_cliente(fornecedor_cliente_request: FornecedorClienteRequest,
                             db: Session = Depends(get_db)) -> FornecedorClienteResponse:
    fornecedor_cliente = FornecedorCliente(nome=fornecedor_cliente_request.nome)
    db.add(fornecedor_cliente)
    db.commit()
    db.refresh(fornecedor_cliente)
    return fornecedor_cliente


@router.put("/{id_do_fornecedor_cliente}", response_model=FornecedorClienteResponse, status_code=200)
def atualizar_fornecedor_cliente(id_do_fornecedor_cliente: int, fornecedorClienteRequest: FornecedorClienteRequest,
                                 db: Session = Depends(get_db)) -> FornecedorClienteResponse:
    fornecedor_cliente = busca_fornecedor_cliente_por_id(id_do_fornecedor_cliente, db)
    fornecedor_cliente.nome = fornecedorClienteRequest.nome
    db.add(fornecedor_cliente)
    db.commit()
    db.refresh(fornecedor_cliente)
    return fornecedor_cliente


@router.delete("/{id_do_fornecedor_cliente}", status_code=204)
def excluir_fornecedor_cliente(id_do_fornecedor_cliente: int, db: Session = Depends(get_db)) -> None:
    fornecedor_cliente = busca_fornecedor_cliente_por_id(id_do_fornecedor_cliente, db)
    db.delete(fornecedor_cliente)
    db.commit()


def busca_fornecedor_cliente_por_id(id: int, db: Session):
    conta = db.get(FornecedorCliente, id)
    if conta is None:
        raise NotFound('Conta a pagar e receber')
    return conta
