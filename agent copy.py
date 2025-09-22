
import pandas as pd
from langchain_community.chat_models import ChatOpenAI
from langchain_experimental.agents import create_pandas_dataframe_agent

class CSVAnalysisAgent:
    def __init__(self):
        self.current_file = None
        self.df = None
        self.agent = None

        # Inicializando ChatOpenAI apontando para a API Groq
        self.llm = ChatOpenAI(
            model="grok-english",            # ou outro modelo Groq disponível
            temperature=0,
            openai_api_key="",
    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        base_url="https://api.groq.com/openai/v1"  # aqui você direciona para Groq
        )

    def load_file(self, file_path: str):
        try:
            self.df = pd.read_csv(file_path)
            self.current_file = file_path
            self.agent = create_pandas_dataframe_agent(
                self.df,
                self.llm,
                verbose=False,
                allow_dangerous_code=True
            )
            return True
        except Exception as e:
            print("Erro ao carregar CSV:", e)
            return False

    def analyze_csv(self, question: str):
        if not self.agent:
            return {"output": "Nenhum arquivo carregado."}
        try:
            result = self.agent.run(question)
            return {"output": result}
        except Exception as e:
            return {"output": f"Erro ao processar a pergunta: {str(e)}"}
