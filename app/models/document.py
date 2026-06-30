from datetime import datetime, timezone

from sqlmodel import Field, SQLModel


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


class DocumentRead(SQLModel):
    id: int
    filename: str
    file_type: str
    storage_path: str
    size: int
    created_at: datetime