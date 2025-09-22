
from dotenv import load_dotenv
import os
import shutil
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from agent import CSVAnalysisAgent

# Load environment variables from the .env file
load_dotenv()

# Criar pasta para arquivos se não existir
if not os.path.exists("files"):
    os.makedirs("files")

# Inicializar agente com Groq API Key
api_key = os.getenv('GROQ_API_KEY')

print("API key")
print(api_key)
agent = CSVAnalysisAgent(api_key=api_key)

app = FastAPI(title="CSV Analysis Agent API")

# Configuração CORS para permitir requests do React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # porta do React
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "API CSV Analysis Agent funcionando!"}

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    file_path = os.path.join("files", file.filename)
    print("Upload do arquivo")
    try:
        # Salvar arquivo
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        print("Carregar o arquivo")
        # Carregar CSV no agente
        if agent.load_file(file_path):
            return {"message": f"Arquivo '{file.filename}' carregado com sucesso!", "filename": file.filename}
        else:
            return JSONResponse(status_code=400, content={"message": "Erro ao carregar o arquivo."})
    except Exception as e:
        return JSONResponse(status_code=400, content={"message": f"Erro: {str(e)}"})

@app.post("/ask")
async def ask(pergunta: str = Form(...)):
    response = agent.analyze_csv(pergunta)
    return {"response": response}

@app.get("/current")
def current_file():
    if agent.current_file:
        return {"current_file": agent.current_file}
    return {"current_file": None, "message": "Nenhum arquivo carregado."}
