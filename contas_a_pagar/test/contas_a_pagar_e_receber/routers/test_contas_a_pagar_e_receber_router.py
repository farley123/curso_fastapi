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

