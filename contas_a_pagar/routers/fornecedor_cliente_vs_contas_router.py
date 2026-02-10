from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from shared.dependencies import get_db
from contas_a_pagar.routers.contas_a_pagar_e_receber_router import ContaPagarReceberResponse
from contas_a_pagar.models.conta_a_pagar_receber_model import ContaPagarReceber

router = APIRouter(prefix="/fornecedor-cliente")

@router.get("/{id_do_fornecedor_cliente/contas_a_pagar_e_recber", response_model=List[ContaPagarReceberResponse])
def obter_contas_a_pagar_e_receber_de_um_fornecedor_cliente_por_id(id_do_fornecedor_cliente: int,
                                                                   db: Session = Depends(get_db)) -> List[
    ContaPagarReceberResponse]:
    return db.query(ContaPagarReceber).filter(ContaPagarReceber.fornecedor_cliente_id==id_do_fornecedor_cliente).all()