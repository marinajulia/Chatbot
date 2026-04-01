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
            print(f"Erro ao processar a resposta: {ex}")
            return ""

    def generate_resume(self, history_message:list=[]) -> str:
        
