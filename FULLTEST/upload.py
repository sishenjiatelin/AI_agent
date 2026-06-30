from datetime import datetime, timezone
import uuid
from pathlib import Path
from fastapi import HTTPException, UploadFile
from sqlmodel import Session, select,Field, SQLModel, create_engine

BASE_DIR = Path(__file__).resolve().parents[0]
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
pdf_path = BASE_DIR / "dptest.pdf"
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///FULLTEST/{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)

class Document(SQLModel, table=True):
    __tablename__ = "documents"

    id: int | None = Field(default=None, primary_key=True)
    filename: str
    file_type: str
    storage_path: str
    size: int
    created_at: datetime = Field(
        default_factory=lambda: datetime.now()
    )
SQLModel.metadata.create_all(engine)

class DocumentRead(SQLModel):
    id: int
    filename: str
    file_type: str
    storage_path: str
    size: int
    created_at: datetime

def to_document_read(document: Document) -> DocumentRead:
    return DocumentRead(
        id=document.id,
        filename=document.filename,
        file_type=document.file_type,
        storage_path=document.storage_path,
        size=document.size,
        created_at=document.created_at,
    )

def save_uploaded_file(session: Session, file: UploadFile) -> DocumentRead:
    original_name = Path(file.filename or " ").name
    content = file.file.read()
    save_name = f"{uuid.uuid4().hex}_{original_name}"
    saved_path = UPLOAD_DIR / save_name
    saved_path.write_bytes(content)

    document = Document(
        filename=original_name,
        file_type=file.content_type or "application/pdf",
        storage_path=str(saved_path),
        size=len(content),
    )
    session.add(document)
    session.commit()
    session.refresh(document)
    return to_document_read(document)

with Session(engine) as session:
    with pdf_path.open("rb") as f:
        upload_file = UploadFile(
            filename = pdf_path.name,
            file = f
        )
        result = save_uploaded_file(
            session=session,
            file=upload_file,
        )
        print(result)