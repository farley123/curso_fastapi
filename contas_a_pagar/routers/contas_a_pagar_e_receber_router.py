from typing import List, Dict
from fastapi import APIRouter


router = APIRouter(prefix="/contas-a-pagar-e-receber")


@router.get("/")
def listar_contas() -> List[Dict]:
    return [{"contas1": "contas1"}, {"contas2": "contas2"}]
