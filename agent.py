import pandas as pd
from langchain_community.chat_models import ChatOpenAI
from langchain_experimental.agents import create_pandas_dataframe_agent

class CSVAnalysisAgent:
    def __init__(self, api_key: str):
        self.current_file = None
        self.df = None
        self.agent = None

        # Inicializando ChatOpenAI para Groq
        self.llm = ChatOpenAI(
            model="llama-3.3-70b-versatile",                    # modelo Groq
            temperature=0,
            openai_api_key=api_key,
            base_url="https://api.groq.com/openai/v1"
        )

    def load_file(self, file_path: str):
        import pandas as pd
        try:
            self.df = pd.read_csv(file_path)
            self.current_file = file_path

            # ⚠️ df primeiro, llm segundo, sem nomear
            self.agent = create_pandas_dataframe_agent(
                df=self.df,
                llm=self.llm,
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
