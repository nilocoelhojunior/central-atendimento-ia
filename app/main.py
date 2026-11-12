from pathlib import Path
import json

from fastapi import FastAPI, Query
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.triage import classify

ROOT = Path(__file__).resolve().parents[1]
app = FastAPI(title="Central de Atendimento: baseline de triagem", version="0.1.0")


class TicketInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    subject: str = Field(min_length=3, max_length=200)
    body: str = Field(default="", max_length=5000)

    @field_validator("subject", "body", mode="before")
    @classmethod
    def strip_text(cls, value):
        return value.strip() if isinstance(value, str) else value


class TriageOutput(BaseModel):
    category: str
    route: str
    evidence: dict[str, list[str]]
    reason: str
    method: str


@app.get("/api/health")
def health():
    return {"status": "ok", "version": "0.1.0", "mode": "rules-only"}


@app.get("/api/samples")
def samples(split: str = Query(default="dev", pattern="^(dev|holdout)$")):
    rows = json.loads((ROOT / "data/tickets.json").read_text())
    return [row for row in rows if row["split"] == split]


@app.post("/api/triage", response_model=TriageOutput)
def triage(ticket: TicketInput):
    return classify(ticket.subject, ticket.body).to_dict()


if (ROOT / "frontend/dist").is_dir():
    app.mount("/", StaticFiles(directory=ROOT / "frontend/dist", html=True), name="frontend")
