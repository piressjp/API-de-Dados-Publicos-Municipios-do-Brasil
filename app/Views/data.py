from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import deps
from app.Data.Repo import municipio_repo
from typing import List, Optional
from app.schemas import MunicipioRead
from app.Models.municipio import Municipio
import requests
import pandas as pd
import io
import os

router = APIRouter(prefix="/data", tags=["data"])

@router.get("/municipios/", response_model=List[MunicipioRead])
def list_municipios(
    skip: int = 0,
    limit: int = 100,
    uf: Optional[str] = None,
    db: Session = Depends(deps.get_db),
    current_user=Depends(deps.get_current_user)
):
    return municipio_repo.list_municipios(db, skip=skip, limit=limit, uf=uf)

@router.post("/municipios/sync", dependencies=[Depends(deps.require_admin)])
def sync_municipios_from_csv(db: Session = Depends(deps.get_db)):
    """
    Baixa o CSV do portal (configurado via env DATASET_CSV_URL) e popula a tabela.
    Só para admin.
    """
    csv_url = os.getenv("DATASET_CSV_URL", "https://www.gov.br/receitafederal/dados/municipios.csv")
    if not csv_url:
        raise HTTPException(status_code=400, detail="DATASET_CSV_URL não configurado")
    r = requests.get(csv_url)
    if r.status_code != 200:
        raise HTTPException(status_code=400, detail="Não foi possível baixar CSV")
    # tenta ler com pandas
    df = pd.read_csv(io.StringIO(r.text), sep=";|,", engine="python")
    # Normalizar colunas de acordo com seu CSV — aqui supondo colunas conhecidas: adapt to actual file
    # Encontrar colunas (imprime se quiser)
    mapping = {}
    # tenta mapeamento automático comum
    for c in df.columns:
        lc = c.upper()
        if "CÓDIGO DO MUNICÍPIO - TOM" in lc:
            mapping["codigo_tom"] = c
        if "CÓDIGO DO MUNICÍPIO - IBGE" in lc:
            mapping["codigo_ibge"] = c
        if "MUNICÍPIO - TOM" in lc:
            mapping["municipio_tom"] = c
        if "MUNICÍPIO - IBGE" in lc:
            mapping["municipio_ibge"] = c
        if "UF" in lc:
            mapping["uf"] = c

    db.query(Municipio).delete()
    db.commit()

    inserted = 0
    for _, row in df.iterrows():
        obj = {
            "codigo_tom": row.get(mapping.get("codigo_tom")),
            "codigo_ibge": row.get(mapping.get("codigo_ibge")),
            "municipio_tom": row.get(mapping.get("municipio_tom")),
            "municipio_ibge": row.get(mapping.get("municipio_ibge")),
            "uf": row.get(mapping.get("uf"))
        }
        municipio_repo.create_municipio(db, obj)
        inserted += 1

    return {"inserted": inserted}
