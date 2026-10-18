import { CheckCircle2, MessageSquareText, Send } from "lucide-react";
import { useState, type FormEvent } from "react";
import { submitFeedback, type FeedbackPayload } from "../api/feedback";
import { Card } from "../components/Card";
import { Field, Select, TextArea } from "../components/ui/FormControls";

type FeedbackFormState = Omit<FeedbackPayload, "enjoyment"> & {
  enjoyment: FeedbackPayload["enjoyment"] | "";
};

const initialFeedback: FeedbackFormState = {
  enjoyment: "",
  comments: "",
  suggestions: "",
};

export default function FeedbackScreen() {
  const [feedback, setFeedback] = useState<FeedbackFormState>(initialFeedback);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [sent, setSent] = useState(false);

  const submit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!feedback.enjoyment) {
      setError("Selecione uma opção sobre sua experiência.");
      return;
    }
    setSubmitting(true);
    setError(null);

    try {
      await submitFeedback({
        ...feedback,
        enjoyment: feedback.enjoyment,
      });
      setFeedback(initialFeedback);
      setSent(true);
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Não foi possível enviar seu feedback.",
      );
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="mx-auto max-w-3xl p-5 sm:p-8">
      <div className="mb-6 flex items-start gap-3">
        <div className="rounded-xl bg-emerald-100 p-3 text-[#1D6A4A]">
          <MessageSquareText size={22} />
        </div>
        <div>
          <h1 className="text-2xl font-semibold text-neutral-800">
            Queremos ouvir você
          </h1>
          <p className="mt-1 text-sm text-neutral-500">
            Estamos preparando o Melitrack para um teste com meliponicultores.
            Conte como está sendo sua experiência e o que podemos melhorar.
          </p>
        </div>
      </div>

      {sent ? (
        <Card className="p-6 sm:p-8">
          <div className="flex items-start gap-3">
            <CheckCircle2 className="mt-0.5 shrink-0 text-[#1D6A4A]" size={22} />
            <div>
              <h2 className="font-semibold text-neutral-800">Feedback enviado. Obrigado!</h2>
              <p className="mt-1 text-sm text-neutral-600">
                Sua resposta foi salva e vai ajudar a orientar as próximas melhorias.
              </p>
              <button
                type="button"
                onClick={() => setSent(false)}
                className="mt-4 text-sm font-medium text-[#1D6A4A] hover:underline"
              >
                Enviar outro feedback
              </button>
            </div>
          </div>
        </Card>
      ) : (
        <Card className="p-5 sm:p-7">
          <form onSubmit={submit} className="space-y-5">
            <Field label="Você está gostando de usar o Melitrack?">
              <Select
                value={feedback.enjoyment}
                onChange={(enjoyment) =>
                  setFeedback((current) => ({
                    ...current,
                    enjoyment: enjoyment as FeedbackFormState["enjoyment"],
                  }))
                }
                className="w-full"
                required
              >
                <option value="" disabled>
                  Selecione uma opção
                </option>
                <option value="gostando">Sim, estou gostando</option>
                <option value="neutro">Mais ou menos</option>
                <option value="nao_gostando">Ainda não estou gostando</option>
              </Select>
            </Field>

            <Field label="O que achou do Melitrack até agora?">
              <TextArea
                value={feedback.comments}
                onChange={(event) =>
                  setFeedback((current) => ({
                    ...current,
                    comments: event.target.value,
                  }))
                }
                placeholder="Conte o que foi útil, o que chamou sua atenção ou o que não ficou claro."
                maxLength={3000}
                required
              />
            </Field>

            <Field label="Que sugestões ou melhorias você gostaria de ver? (opcional)">
              <TextArea
                value={feedback.suggestions}
                onChange={(event) =>
                  setFeedback((current) => ({
                    ...current,
                    suggestions: event.target.value,
                  }))
                }
                placeholder="Compartilhe ideias para deixar o Melitrack melhor para o seu trabalho."
                maxLength={3000}
              />
            </Field>

            <p className="text-xs text-neutral-500">
              Seu feedback será associado à sua conta para podermos organizar as respostas.
            </p>
            {error && <p className="text-sm text-red-600">{error}</p>}

            <div className="flex justify-end border-t border-[#f0ece4] pt-4">
              <button
                type="submit"
                disabled={submitting}
                className="inline-flex items-center gap-2 rounded-lg bg-[#1D6A4A] px-4 py-2.5 text-sm font-medium text-white transition-colors hover:bg-[#155438] disabled:cursor-not-allowed disabled:opacity-60"
              >
                <Send size={15} />
                {submitting ? "Enviando..." : "Enviar feedback"}
              </button>
            </div>
          </form>
        </Card>
      )}
    </div>
  );
}
