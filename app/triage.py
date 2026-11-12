"""Explainable lexical baseline. Scores are evidence counts, not probabilities."""

from dataclasses import asdict, dataclass
import re
import unicodedata


RULES = {
    "billing": ("boleto", "fatura", "cobranca", "reembolso", "pagamento", "estorno"),
    "access": ("senha", "login", "autenticacao", "acesso bloqueado", "entrar na conta", "2fa"),
    "bug": ("erro", "falha", "travando", "nao carrega", "tela branca", "indisponivel"),
    "feature": ("sugestao", "adicionar", "nova funcionalidade", "integracao", "gostaria que", "melhoria"),
}


def normalize(text: str) -> str:
    text = unicodedata.normalize("NFKD", text.casefold())
    text = "".join(char for char in text if not unicodedata.combining(char))
    return " ".join(re.findall(r"\w+", text))


@dataclass(frozen=True)
class Triage:
    category: str
    route: str
    evidence: dict[str, list[str]]
    reason: str
    method: str = "lexical-v1"

    def to_dict(self) -> dict:
        return asdict(self)


def classify(subject: str, body: str = "") -> Triage:
    # Boundaries prevent matching 'erro' inside unrelated words such as 'ferro'.
    text = f" {normalize(subject + ' ' + body)} "
    evidence = {
        category: [term for term in terms if f" {term} " in text]
        for category, terms in RULES.items()
    }
    evidence = {key: terms for key, terms in evidence.items() if terms}
    if not evidence:
        return Triage("unknown", "human_review", {}, "Nenhuma regra encontrou evidência suficiente.")
    best = max(len(terms) for terms in evidence.values())
    winners = [key for key, terms in evidence.items() if len(terms) == best]
    if len(winners) != 1:
        return Triage("ambiguous", "human_review", evidence, "Empate entre categorias; revisar o chamado.")
    category = winners[0]
    return Triage(category, category, evidence, "Categoria com mais termos distintos encontrados.")
