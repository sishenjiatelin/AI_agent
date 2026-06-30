import uuid
from pathlib import Path

from fastapi import HTTPException, UploadFile
from sqlmodel import Session, select

from app.models.document import Document, DocumentRead

BASE_DIR = Path(__file__).resolve().parents[2]
UPLOAD_DIR = BASE_DIR / "uploads"

ALLOWED_SUFFIXES = {".txt", ".md", ".pdf"}
MAX_FILE_SIZE = 2 * 1024 * 1024


def to_document_read(document: Document) -> DocumentRead:
    return DocumentRead(
        id=document.id,
        filename=document.filename,
        file_type=document.file_type,
        storage_path=document.storage_path,
        size=document.size,
        created_at=document.created_at,
    )


def validate_suffix(filename: str) -> str:
    suffix = Path(filename).suffix.lower()
    if suffix not in ALLOWED_SUFFIXES:
        raise HTTPException(
            status_code=400,
            detail=f"不支持的文件类型：{suffix}",
        )
    return suffix


def save_uploaded_document(
    session: Session,
    file: UploadFile,
) -> DocumentRead:
    original_name = Path(file.filename or "").name
    if not original_name:
        raise HTTPException(status_code=400, detail="文件名不能为空")

    suffix = validate_suffix(original_name)
    content = file.file.read()

    if not content:
        raise HTTPException(status_code=400, detail="文件内容不能为空")
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="文件不能超过 2MB")

    UPLOAD_DIR.mkdir(exist_ok=True)
    saved_name = f"{uuid.uuid4().hex}_{original_name}"
    saved_path = UPLOAD_DIR / saved_name
    saved_path.write_bytes(content)

    relative_path = f"uploads/{saved_name}"
    document = Document(
        filename=original_name,
        file_type=suffix,
        storage_path=relative_path,
        size=len(content),
    )

    session.add(document)
    session.commit()
    session.refresh(document)
    return to_document_read(document)


def list_documents(session: Session) -> list[DocumentRead]:
    statement = select(Document).order_by(Document.id)
    documents = session.exec(statement).all()
    return [to_document_read(item) for item in documents]


def get_document_or_404(
    session: Session,
    document_id: int,
) -> Document:
    document = session.get(Document, document_id)
    if document is None:
        raise HTTPException(status_code=404, detail="资料不存在")
    return document


def read_document_content(
    session: Session,
    document_id: int,
) -> dict[str, object]:
    document = get_document_or_404(session, document_id)
    file_path = BASE_DIR / document.storage_path

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="文件不存在")

    if document.file_type == ".pdf":
        content = "PDF 文件已保存，Day 13 暂不解析正文。"
    else:
        content = file_path.read_text(encoding="utf-8")

    return {
        "id": document.id,
        "filename": document.filename,
        "file_type": document.file_type,
        "content": content,
    }