from langchain_classic.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI
from langchain_classic.chains import ConversationChain
from langchain_core.prompts import PromptTemplate

class IAresponse:
    def __init__(self, api_key:str, ia_model:str, system_prompt:str, resume_lead:str = ""):
        self.api_key = api_key
        self.ai_model = self.ai_model
        self.system_prompt = system_prompt

        if resume_lead:
            print("Resumo localizado",flush=True)
            response_prompt = """
            historico da convers: {history}

            usuario: {input}
            """

            resume_lead += f"\nresumo de todas as interações que houve com esse lead: {resume_lead}"

        else:
            response_prompt = """
            historico da conversa:
            {history}

            usuario: {input}
            """

        self.system_prompt += response_prompt

        if not self.ai_model:
            self.ai_model = "gpt-4o-mini"

    def generate_response(self, message_lead:str, history_message:list=[]) -> str:
        try:
            chat = ChatOpenAI(model=self.ai_model, api_key=self.api_key)

            
        except Exception as ex:
            print(f"Erro ao processar a resposta: {ex}")
            return ""

    def generate_resume(self, history_message:list=[]) -> str:
        ...
