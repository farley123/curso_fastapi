from fastapi.testclient import TestClient
from main import app


client = TestClient(app=app)


def test_deve_listar_contas_a_pagar_e_receber():
    response = client.get("/contas-a-pagar-e-receber")
    assert response.status_code == 200

    assert response.json() == [
        {
            "id": 1,
            "descricao": "Aluguel",
            "valor": 1000.5,
            "tipo": "Pagar",
        },
        {
            "id": 2,
            "descricao": "salario",
            "valor": 5000.0,
            "tipo": "Receber",
        },
    ]


def test_deve_criar_contas_a_pagar_e_receber():
    nova_conta = {"descricao": "Curso python", "valor": 333, "tipo": "PAGAR"}
    nova_conta_copy = nova_conta.copy()
    nova_conta_copy["id"] = 3
    response = client.post(url="/contas-a-pagar-e-receber/", json=nova_conta)
    assert response.status_code == 201

    assert response.json() == {
        "id": 3,
        "descricao": "Curso python",
        "valor": 333.0,
        "tipo": "PAGAR",
    }
