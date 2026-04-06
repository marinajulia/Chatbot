from openai import OpenAI

class IAresponse:
    def __init__(self, api_key:str, ia_model:str, system_prompt:str, resume_lead:str = ""):
        self.api_key = api_key
        self.ai_model = self._normalize_model_name(ia_model)
        self.system_prompt = system_prompt

        if resume_lead:
            print("Resumo localizado", flush=True)
            self.system_prompt += (
                "\n\nResumo de todas as interacoes anteriores com este lead:\n"
                f"{resume_lead}"
            )

        if not self.ai_model:
            self.ai_model = "gpt-4o-mini"

    @staticmethod
    def _normalize_model_name(model_name: str) -> str:
        normalized = (model_name or "").strip().replace("=", "-")
        return "-".join(part for part in normalized.split("-") if part)

    def generate_response(self, message_lead: str, history_message: list = None) -> str:
        try:
            if history_message is None:
                history_message = []

            messages = [{"role": "system", "content": self.system_prompt}]

            for msg in history_message[-20:]:
                role = (msg.get("role") or "").strip().lower()
                content = msg.get("content", "")
                if role in {"user", "assistant", "system"} and content:
                    messages.append({"role": role, "content": content})

            messages.append({"role": "user", "content": message_lead})

            print("Total de interações:", len(history_message), flush=True)

            client = OpenAI(api_key=self.api_key)
            result = client.chat.completions.create(model=self.ai_model, messages=messages)
            resposta = result.choices[0].message.content or ""

            print("Resposta gerada pela IA:", resposta, flush=True)

            return resposta

        except Exception as ex:
            print(f"Erro ao processar a resposta: {ex}", flush=True)
            return ""

    def generate_resume(self, history_message: list = []) -> str:
        try:
            system_prompt = (
                "Você é um assistente especializado em resumir conversas com leads. Seu objetivo é identificar, "
                "extrair e armazenar de forma clara todos os pontos-chave e informações importantes discutidas "
                "durante a conversa. Ao elaborar o resumo, siga estas diretrizes:\n\n"
                "1. **Identificação dos Pontos-Chave:** Extraia os tópicos principais da conversa, incluindo "
                "necessidades, interesses, objeções e próximos passos do lead.\n"
                "2. **Organização das Informações:** Estruture o resumo de maneira clara e organizada, "
                "facilitando a visualização dos dados mais relevantes.\n"
                "3. **Foco nas Informações Relevantes:** Certifique-se de que nenhuma informação importante "
                "seja omitida. Dados como informações de contato, dúvidas específicas e requisitos do lead "
                "devem ser destacados.\n"
                "4. **Clareza e Concisão:** O resumo deve ser conciso, mas detalhado o suficiente para "
                "fornecer um panorama completo da conversa.\n"
                "5. **Privacidade e Segurança:** Garanta que todas as informações sensíveis sejam tratadas "
                "com a devida confidencialidade."
            )

            messages = [{"role": "system", "content": system_prompt}]

            for msg in history_message:
                role = (msg.get("role") or "").strip().lower()
                content = msg.get("content", "")
                if role in {"user", "assistant"} and content:
                    messages.append({"role": role, "content": content})

            messages.append({"role": "user", "content": "Gere um resumo detalhado dessa conversa"})

            print(f"Total de {len(history_message)} interações", flush=True)

            client = OpenAI(api_key=self.api_key)
            result = client.chat.completions.create(model=self.ai_model, messages=messages)
            resposta = result.choices[0].message.content or ""

            print(f"Resposta da IA   : {resposta}", flush=True)

            return resposta
        except Exception as ex:
            print(f"❌ Erro ao processar resposta: {ex}", flush=True)
            return None
