from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import xml.etree.ElementTree as ET
import configparser

# Lê o config.ini
config = configparser.ConfigParser()
config.read('config.ini')
ARQUIVO = config['DEFAULT'].get('arquivo')

app = FastAPI()

class Aparelho(BaseModel):
    id: int
    nome: str
    marca: str
    preco: float
    categoria: str
    deposito: str

def carregar_aparelhos_xml():
    try:
        tree = ET.parse(ARQUIVO)
        root = tree.getroot()
        aparelhos = []

        for aparelho in root.findall("aparelho"):
            aparelhos.append({
                "id": int(aparelho.find("id").text),
                "nome": aparelho.find("nome").text,
                "marca": aparelho.find("marca").text,
                "preco": float(aparelho.find("preco").text),
                "categoria": aparelho.find("categoria").text,
                "deposito": aparelho.find("deposito").text,
            })

        return aparelhos

    except FileNotFoundError:
        root = ET.Element("estoque")
        tree = ET.ElementTree(root)
        tree.write(ARQUIVO, encoding="utf-8", xml_declaration=True)
        return []

def salvar_aparelhos_xml(aparelhos):
    root = ET.Element("estoque")

    for a in aparelhos:
        ap = ET.SubElement(root, "aparelho")
        ET.SubElement(ap, "id").text = str(a["id"])
        ET.SubElement(ap, "nome").text = a["nome"]
        ET.SubElement(ap, "marca").text = a["marca"]
        ET.SubElement(ap, "preco").text = str(a["preco"])
        ET.SubElement(ap, "categoria").text = a["categoria"]
        ET.SubElement(ap, "deposito").text = a["deposito"]

    tree = ET.ElementTree(root)
    tree.write(ARQUIVO, encoding="utf-8", xml_declaration=True)

@app.post("/aparelhos", status_code=201)
def adicionar(aparelho: Aparelho):
    aparelhos = carregar_aparelhos_xml()

    if any(a["id"] == aparelho.id for a in aparelhos):
        raise HTTPException(status_code=400, detail="ID já existe")

    aparelhos.append(aparelho.dict())
    salvar_aparelhos_xml(aparelhos)
    return {"message": "Aparelho adicionado"}

@app.get("/aparelhos")
def listar():
    return carregar_aparelhos_xml()

@app.get("/aparelhos/{id}")
def buscar(id: int):
    for a in carregar_aparelhos_xml():
        if a["id"] == id:
            return a
    raise HTTPException(status_code=404, detail="Não encontrado")

@app.put("/aparelhos/{id}")
def atualizar(id: int, aparelho: Aparelho):
    aparelhos = carregar_aparelhos_xml()

    for a in aparelhos:
        if a["id"] == id:
            a.update(aparelho.dict())
            salvar_aparelhos_xml(aparelhos)
            return {"message": "Atualizado"}

    raise HTTPException(status_code=404, detail="Não encontrado")

@app.delete("/aparelhos/{id}")
def deletar(id: int):
    aparelhos = carregar_aparelhos_xml()
    novos = [a for a in aparelhos if a["id"] != id]

    if len(aparelhos) == len(novos):
        raise HTTPException(status_code=404, detail="Não encontrado")

    salvar_aparelhos_xml(novos)
    return {"message": "Removido"}

@app.put("/aparelhos/{id}/transferir/{novo_deposito}")
def transferir(id: int, novo_deposito: str):
    aparelhos = carregar_aparelhos_xml()

    for a in aparelhos:
        if a["id"] == id:
            a["deposito"] = novo_deposito
            salvar_aparelhos_xml(aparelhos)
            return {"message": "Transferido"}

    raise HTTPException(status_code=404, detail="Não encontrado")
