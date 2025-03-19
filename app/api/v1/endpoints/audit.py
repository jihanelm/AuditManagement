from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
import shutil
import os
from app.core.database import get_db
from app.models.audit import Audit
from app.schemas.audit import AuditResponse

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/request", response_model=AuditResponse)
def create_audit_request(
        user_id: int = Form(...),
        type_audit: str = Form(...),
        demandeur_nom: str = Form(...),
        demandeur_prenom: str = Form(...),
        demandeur_email: str = Form(...),
        demandeur_phone: str = Form(...),
        demandeur_departement: str = Form(...),
        description: str = Form(...),
        objectif: str = Form(...),
        urgence: str = Form(...),
        fichier_attache: Optional[UploadFile] = File(None),
        db: Session = Depends(get_db),
):
    file_path = None
    if fichier_attache:
        file_path = os.path.join(UPLOAD_DIR, fichier_attache.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(fichier_attache.file, buffer)

    audit = Audit(
        user_id=user_id,
        type_audit=type_audit,
        demandeur_nom=demandeur_nom,
        demandeur_prenom=demandeur_prenom,
        demandeur_email=demandeur_email,
        demandeur_phone=demandeur_phone,
        demandeur_departement=demandeur_departement,
        description=description,
        objectif=objectif,
        urgence=urgence,
        fichier_attache=file_path
    )
    db.add(audit)
    db.commit()
    db.refresh(audit)
    return audit


@router.get("/", response_model=List[AuditResponse])
def get_audits(db: Session = Depends(get_db)):
    return db.query(Audit).all()


@router.get("/{audit_id}", response_model=AuditResponse)
def get_audit(audit_id: int, db: Session = Depends(get_db)):
    audit = db.query(Audit).filter(Audit.id == audit_id).first()
    if not audit:
        raise HTTPException(status_code=404, detail="Audit not found")
    return audit
