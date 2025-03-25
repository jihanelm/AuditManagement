from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from typing import List
from app.models.affect import Affect
from app.models.auditeur import Auditeur
from app.models.prestataire import Prestataire
from app.models.ip import IP
from app.schemas.affect import AffectSchema
from app.schemas.auditeur import AuditeurSchema
from app.schemas.prestataire import PrestataireSchema
from app.schemas.ip import IPSchema
from app.services.audit11 import create_affect, get_affect, list_affects, create_auditeur, list_auditeurs

router = APIRouter()

@router.post("/affects/", response_model=AffectSchema)
def create_affectation(affect_data: AffectSchema, db: Session = Depends(get_db)):
    return create_affect(db, affect_data)

@router.get("/affects/{affect_id}", response_model=AffectSchema)
def read_affect(affect_id: int, db: Session = Depends(get_db)):
    affect = get_affect(db, affect_id)
    if not affect:
        raise HTTPException(status_code=404, detail="Affectation non trouvée")
    return affect

@router.get("/affects/", response_model=List[AffectSchema])
def read_affects(db: Session = Depends(get_db)):
    return list_affects(db)

# Endpoints pour la gestion des auditeurs
@router.post("/auditeurs/", response_model=AuditeurSchema)
def create_auditor(auditeur_data: AuditeurSchema, db: Session = Depends(get_db)):
    return create_auditeur(db, auditeur_data)

@router.get("/auditeurs/", response_model=List[AuditeurSchema])
def read_auditors(db: Session = Depends(get_db)):
    return list_auditeurs(db)

# Endpoints pour la gestion des prestataires
@router.get("/prestataires/", response_model=List[PrestataireSchema])
def read_prestataires(db: Session = Depends(get_db)):
    return db.query(Prestataire).all()

# Endpoints pour la gestion des IPs
@router.get("/ips/", response_model=List[IPSchema])
def read_ips(db: Session = Depends(get_db)):
    return db.query(IP).all()
