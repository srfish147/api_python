from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from tempfile import NamedTemporaryFile
import shutil
import os
#from convert_doc import adicionar_cabecalho_com_logo_e_numero_pagina
from insert_header import adicionar_cabecalho_com_logo

app = FastAPI()

# Habilita CORS para permitir requisições do Bubble
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Ou especifique: ["https://info-57154.bubbleapps.io"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/generate-docx/")
async def generate_docx(
    contract_name: str = Form(...),
    logo_url: str = Form(...),
    doc: UploadFile = File(...),
):
    # Salva o arquivo enviado em um arquivo temporário
    with NamedTemporaryFile(delete=False, suffix=".docx") as tmp_input:
        shutil.copyfileobj(doc.file, tmp_input)
        input_path = tmp_input.name

    # Define o caminho do arquivo de saída
    output_path = input_path.replace(".docx", f"_{contract_name}.docx")

    # Chama a função de conversão passando os parâmetros
    #adicionar_cabecalho_com_logo_e_numero_pagina(input_path, output_path, logo_url)
    adicionar_cabecalho_com_logo(input_path, output_path, logo_url)


    # Remove o arquivo temporário de entrada
    os.remove(input_path)

    # Retorna o novo arquivo como resposta
    return FileResponse(
        output_path,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        filename=f"{contract_name}.docx"
    )

@app.get("/")
def read_root():
    return {"message": "API DOCX is running"}
