import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.triage import classify

client = TestClient(app)


@pytest.mark.parametrize(("text", "category"), [
    ("Segunda via de BOLETO", "billing"),
    ("Esqueci minha senha", "access"),
    ("A página não carrega", "bug"),
    ("Sugestão de exportação", "feature"),
    ("Obrigado pela ajuda", "unknown"),
    ("Erro no boleto", "ambiguous"),
    ("O relatório de ferro chegou", "unknown"),
])
def test_routing_and_abstention(text, category):
    assert classify(text).category == category


def test_repeated_keyword_does_not_inflate_evidence():
    assert classify("boleto boleto boleto senha").category == "ambiguous"


def test_api_explains_evidence():
    response = client.post("/api/triage", json={"subject": "Preciso de reembolso"})
    assert response.status_code == 200
    assert response.json()["evidence"] == {"billing": ["reembolso"]}


@pytest.mark.parametrize("payload", [
    {"subject": "   "}, {"subject": "ok"}, {"subject": "x" * 201},
    {"subject": "Chamado", "body": "x" * 5001},
    {"subject": "Chamado", "role": "admin"}, {"subject": 42},
])
def test_api_rejects_invalid_payload(payload):
    assert client.post("/api/triage", json=payload).status_code == 422


def test_dataset_contract_and_split_integrity():
    dev = client.get("/api/samples?split=dev").json()
    holdout = client.get("/api/samples?split=holdout").json()
    assert dev and holdout
    assert not ({row["id"] for row in dev} & {row["id"] for row in holdout})
    assert not ({row["subject"] for row in dev} & {row["subject"] for row in holdout})
    assert client.get("/api/samples?split=invalid").status_code == 422
