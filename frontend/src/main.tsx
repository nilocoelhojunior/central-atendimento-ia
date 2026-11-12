import { useState, type FormEvent } from "react";
import { createRoot } from "react-dom/client";
import "./style.css";

type Result = {
  category: string;
  route: string;
  reason: string;
  evidence: Record<string, string[]>;
  method: string;
};
const labels: Record<string, string> = {
  billing: "Financeiro",
  access: "Acesso",
  bug: "Problema técnico",
  feature: "Melhoria",
  unknown: "Sem evidência",
  ambiguous: "Revisão necessária",
  human_review: "Revisão humana",
};
const examples = [
  "Preciso da segunda via do boleto",
  "Esqueci minha senha",
  "A página não carrega",
  "Erro no boleto",
  "Obrigado pelo atendimento",
];

function App() {
  const [subject, setSubject] = useState(examples[0]);
  const [body, setBody] = useState(
    "O documento do mês passado não aparece no meu histórico.",
  );
  const [result, setResult] = useState<Result | null>(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [stale, setStale] = useState(false);
  async function submit(event: FormEvent) {
    event.preventDefault();
    setBusy(true);
    setError("");
    setResult(null);
    setStale(false);
    try {
      const response = await fetch("/api/triage", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ subject, body }),
      });
      if (!response.ok)
        throw new Error(
          response.status === 422
            ? "Revise o assunto e a descrição antes de tentar novamente."
            : "Não foi possível classificar. Tente novamente.",
        );
      setResult(await response.json());
    } catch (err) {
      setError(
        err instanceof TypeError
          ? "Não foi possível conectar à API. Verifique o serviço e tente novamente."
          : (err as Error).message,
      );
    } finally {
      setBusy(false);
    }
  }
  return (
    <main>
      <header>
        <a className="brand" href="/">
          Central de Atendimento
        </a>
        <span className="version">Primeira entrega · v0.1</span>
      </header>
      <section className="intro">
        <p className="kicker">Laboratório público de engenharia</p>
        <h1>
          Uma decisão de triagem.
          <br />
          Com evidências à vista.
        </h1>
        <p>
          Experimente um chamado e veja os termos que sustentam o
          encaminhamento. Quando as regras não bastam, a decisão fica com uma
          pessoa.
        </p>
      </section>
      <div className="workspace">
        <section className="input">
          <h2>Descreva o chamado</h2>
          <p className="hint">
            Use um exemplo fictício. Esta demonstração não salva os textos.
          </p>
          <form onSubmit={submit}>
            <label htmlFor="subject">Assunto</label>
            <input
              id="subject"
              value={subject}
              required
              minLength={3}
              maxLength={200}
              disabled={busy}
              onChange={(e) => {
                setSubject(e.target.value);
                setStale(true);
              }}
            />
            <label htmlFor="body">
              Descrição <span>(opcional)</span>
            </label>
            <textarea
              id="body"
              rows={5}
              maxLength={5000}
              disabled={busy}
              value={body}
              onChange={(e) => {
                setBody(e.target.value);
                setStale(true);
              }}
            />
            <button
              className="primary"
              disabled={busy || subject.trim().length < 3}
            >
              {busy ? "Classificando…" : "Classificar chamado"}
            </button>
          </form>
          <h3>Experimente também</h3>
          <div className="examples">
            {examples.map((example) => (
              <button
                key={example}
                disabled={busy}
                onClick={() => {
                  setSubject(example);
                  setBody("");
                  setResult(null);
                  setError("");
                }}
              >
                {example}
              </button>
            ))}
          </div>
        </section>
        <section className="output" aria-live="polite">
          <h2>Por que este encaminhamento?</h2>
          {error && (
            <p role="alert" className="error">
              {error}
            </p>
          )}
          {result ? (
            <>
              <span className="result-label">{labels[result.category]}</span>
              <p className="reason">{result.reason}</p>
              <dl>
                <dt>Encaminhar para</dt>
                <dd>{labels[result.route]}</dd>
                <dt>Evidências encontradas</dt>
                <dd>
                  {Object.keys(result.evidence).length
                    ? Object.entries(result.evidence).map(
                        ([category, terms]) => (
                          <p key={category}>
                            <strong>{labels[category]}:</strong>{" "}
                            {terms.join(", ")}
                          </p>
                        ),
                      )
                    : "Nenhum termo reconhecido."}
                </dd>
              </dl>
              {stale && (
                <p className="notice">
                  O chamado foi alterado. Classifique novamente para atualizar o
                  resultado.
                </p>
              )}
            </>
          ) : (
            <p className="empty">
              Classifique o chamado para inspecionar o resultado e as
              evidências.
            </p>
          )}
          <aside>
            <h3>O que esta versão faz</h3>
            <p>
              Usa regras lexicais, sem modelo de IA. Empates e ausência de
              termos pedem revisão humana. Ela ainda não compreende negações ou
              contexto.
            </p>
            <p>Este baseline será comparado com LLMs nas próximas entregas.</p>
            <a href="/docs" target="_blank" rel="noreferrer">
              Explorar contrato da API
            </a>
          </aside>
        </section>
      </div>
      <footer>
        Projeto de Nilo Coelho · Dados de demonstração sintéticos · Sem chamadas
        a serviços pagos
      </footer>
    </main>
  );
}
createRoot(document.getElementById("root")!).render(<App />);
