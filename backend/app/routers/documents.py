from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session

from app.middleware.deps import get_db, require_role
from app.models.user import User
from app.schemas.document import DocumentOut
from app.services.activity_service import log_activity
from app.services.documents_service import save_document, list_documents, delete_document

router = APIRouter(prefix="/documents", tags=["documents"])


@router.post("", response_model=DocumentOut)
def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("Admin")),
):
    doc = save_document(db, file, current_user.id)
    log_activity(db, current_user.id, "document_upload", f"document_id={doc.id}")
    return doc


@router.get("", response_model=list[DocumentOut])
def list_documents_endpoint(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("Admin")),
):
    return list_documents(db)


@router.delete("/{document_id}")
def delete_document_endpoint(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("Admin")),
):
    delete_document(db, document_id)
    log_activity(db, current_user.id, "document_delete", f"document_id={document_id}")
    return {"ok": True}
