from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from shared.dependencies import get_db
from shared.database import Base
from main import app


client = TestClient(app=app)

SQLALCHEMY_DATABASE_URL = "sqlite:///.test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


def test_deve_listar_contas_a_pagar_e_receber():

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    client.post(
        "/contas-a-pagar-e-receber",
        json={
            "descricao": "Aluguel",
            "valor": 1000.5,
            "tipo": "PAGAR",
        },
    )
    response = client.get("/contas-a-pagar-e-receber")
    assert response.status_code == 200

    assert response.json() == [
        {
            "id": 1,
            "descricao": "Aluguel",
            "valor": 1000.5,
            "tipo": "PAGAR",
            "fornecedor": None,
        },
    ]


def test_deve_criar_contas_a_pagar_e_receber():

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    nova_conta = {"descricao": "Curso python", "valor": 333, "tipo": "PAGAR"}
    nova_conta_copy = nova_conta.copy()
    nova_conta_copy["id"] = 1
    response = client.post(url="/contas-a-pagar-e-receber/", json=nova_conta)
    assert response.status_code == 201

    assert response.json() == {
        "id": 1,
        "descricao": "Curso python",
        "valor": 333.0,
        "tipo": "PAGAR",
        "fornecedor": None
    }


def test_deve_retornar_erro_quando_exceder_a_descricao():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    response = client.post(
        "/contas-a-pagar-e-receber",
        json={
            "descricao": "012345678901234567890012345678901234567890012345678901234567890",
            "valor": 1000.5,
            "tipo": "PAGAR",
        },
    )
    assert response.status_code == 422


def test_deve_retornar_erro_quando_o_valor_for_zero_ou_menor():
    response = client.post(
        "/contas-a-pagar-e-receber",
        json={
            "descricao": "01121",
            "valor": 0,
            "tipo": "PAGAR",
        },
    )
    assert response.status_code == 422

    response = client.post(
        "/contas-a-pagar-e-receber",
        json={
            "descricao": "01121",
            "valor": -1,
            "tipo": "PAGAR",
        },
    )
    assert response.status_code == 422


def test_deve_atualizar_contas_a_pagar_e_receber():

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    # cria uma nova conta
    response = client.post(
        url="/contas-a-pagar-e-receber/",
        json={"descricao": "Curso python", "valor": 333, "tipo": "PAGAR"},
    )
    id_conta = response.json()["id"]

    # atualiza uma nova conta
    response_put = client.put(
        f"/contas-a-pagar-e-receber/{id_conta}",
        json={"descricao": "Valor atualizado", "valor": 111, "tipo": "PAGAR"},
    )
    assert response_put.status_code == 200
    assert response_put.json()["valor"] == 111


def test_deve_remover_contas_a_pagar_e_receber():

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    # cria uma nova conta
    response = client.post(
        url="/contas-a-pagar-e-receber/",
        json={"descricao": "Curso python", "valor": 333, "tipo": "PAGAR"},
    )
    id_conta = response.json()["id"]

    # remove uma conta
    response_delete = client.delete(
        f"/contas-a-pagar-e-receber/{id_conta}",
    )
    assert response_delete.status_code == 200


def test_deve_retornar_nao_encontrado_para_id_nao_existente():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    response_get = client.get("/contas-a-pagar-e-receber/100")
    assert response_get.status_code == 404


