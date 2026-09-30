import { BrainCircuit, ExternalLink, FileText, ShieldCheck, User, X } from "lucide-react";

interface TermsModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export function TermsModal({ isOpen, onClose }: TermsModalProps) {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm p-4 animate-in fade-in duration-200">
      <div className="relative flex max-h-[90vh] w-full max-w-2xl flex-col rounded-2xl bg-white shadow-2xl overflow-hidden border border-neutral-100">
        {/* Header */}
        <div className="flex items-center justify-between border-b border-neutral-100 bg-[#F7F5F0] px-6 py-4">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-[#1D6A4A] text-white shadow-sm">
              <FileText size={20} />
            </div>
            <div>
              <h2 className="text-lg font-bold text-neutral-800">Termos de Serviço</h2>
              <p className="text-xs text-neutral-500">Condições de uso e política de dados do Melitrack</p>
            </div>
          </div>
          <button
            type="button"
            onClick={onClose}
            className="rounded-lg p-2 text-neutral-400 transition-colors hover:bg-neutral-200/60 hover:text-neutral-700"
            aria-label="Fechar termos de serviço"
          >
            <X size={20} />
          </button>
        </div>

        {/* Content Body */}
        <div className="flex-1 overflow-y-auto px-6 py-5 space-y-6 text-sm text-neutral-600 leading-relaxed">
          {/* Developed By Section */}
          <section className="rounded-xl border border-emerald-100 bg-emerald-50/50 p-4">
            <div className="flex items-start gap-3">
              <div className="mt-0.5 flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-[#1D6A4A] text-white">
                <User size={16} />
              </div>
              <div className="space-y-1">
                <h3 className="font-semibold text-[#1D6A4A]">Desenvolvimento e Autoria</h3>
                <p className="text-xs text-neutral-600">
                  O <strong>Melitrack</strong> é uma plataforma inteligente voltada à gestão de meliponários,
                  monitoramento de abelhas sem ferrão (<em>Meliponini</em>), controle de produção e análises por IA.
                </p>
                <div className="pt-1 flex items-center gap-2 text-xs">
                  <span className="font-medium text-neutral-700">Desenvolvido por:</span>
                  <a
                    href="https://www.linkedin.com/in/lucas-blanger-4668a2210/"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center gap-1 font-semibold text-[#1D6A4A] hover:underline"
                  >
                    Lucas Blanger
                    <ExternalLink size={12} />
                  </a>
                </div>
              </div>
            </div>
          </section>

          {/* AI Model Training Clause - Highlighted */}
          <section className="rounded-xl border border-amber-200 bg-amber-50/60 p-4.5 space-y-2">
            <div className="flex items-center gap-2 text-[#9A6200] font-semibold text-sm">
              <BrainCircuit size={18} className="shrink-0 text-amber-600" />
              <h4>Uso de Imagens e Treinamento de Inteligência Artificial</h4>
            </div>
            <p className="text-xs text-amber-950 leading-relaxed">
              Ao utilizar a plataforma e enviar fotografias referentes a colmeias, caixas, discos de postura,
              inspeções de manejo ou amostras de abelhas, <strong>o usuário concorda e autoriza expressamente</strong> que
              tais imagens possam ser armazenadas, processadas e utilizadas pelo sistema <strong>Melitrack</strong> para o
              <strong> treinamento, aprimoramento, validação e calibração contínua de seus modelos de Inteligência Artificial e Visão Computacional</strong>.
            </p>
            <p className="text-[11px] text-amber-800 italic">
              Esta autorização permite melhorar a precisão na identificação automatizada de espécies e na avaliação de saúde das colônias para toda a comunidade de meliponicultores.
            </p>
          </section>

          {/* Core Terms */}
          <section className="space-y-3">
            <h4 className="font-bold text-neutral-800 text-sm flex items-center gap-2">
              <ShieldCheck size={16} className="text-[#1D6A4A]" />
              1. Aceite dos Termos e Cadastro
            </h4>
            <p className="text-xs">
              A criação de conta e o acesso às funcionalidades do Melitrack estão condicionados à leitura,
              compreensão e aceite destes Termos de Serviço. O cadastro exige informações verdadeiras e atualizadas.
            </p>

            <h4 className="font-bold text-neutral-800 text-sm pt-2">2. Responsabilidade sobre as Informações</h4>
            <p className="text-xs">
              O usuário é o único responsável pela guarda e confidencialidade de suas credenciais de acesso,
              bem como pelas informações de manejo, localização e registro de colheitas inseridas na aplicação.
            </p>

            <h4 className="font-bold text-neutral-800 text-sm pt-2">3. Caráter Informativo do Diagnóstico por IA</h4>
            <p className="text-xs">
              As análises fotográficas e relatórios de saúde gerados pelos algoritmos de Visão Computacional
              constituem uma ferramenta auxiliar de apoio ao manejo meliponícola e não substituem o acompanhamento
              técnico presencial especializado de agrônomos ou médicos veterinários.
            </p>

            <h4 className="font-bold text-neutral-800 text-sm pt-2">4. Privacidade e Segurança de Dados</h4>
            <p className="text-xs">
              O Melitrack adota práticas modernas de proteção de dados (autenticação segura via JWT, cookies HttpOnly
              e armazenamento isolado) para garantir a integridade das informações cadastradas pelos meliponicultores.
            </p>
          </section>
        </div>

        {/* Footer Action */}
        <div className="flex items-center justify-between border-t border-neutral-100 bg-neutral-50/80 px-6 py-4">
          <p className="text-xs text-neutral-400">
            Melitrack © {new Date().getFullYear()} • Todos os direitos reservados.
          </p>
          <button
            type="button"
            onClick={onClose}
            className="rounded-lg bg-[#1D6A4A] px-5 py-2 text-xs font-semibold text-white shadow-sm transition-colors hover:bg-[#155438]"
          >
            Entendi e Concordo
          </button>
        </div>
      </div>
    </div>
  );
}
