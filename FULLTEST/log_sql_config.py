import logging
from pathlib import Path
from collections.abc import Generator
from sqlmodel import SQLModel, Session, create_engine


BASE_DIR = Path(__file__).resolve().parents[0]
DB_PATH = BASE_DIR / "app.db"
DATABASE_URL = f"sqlite:///{DB_PATH}"
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread":False},
    echo=False
)
def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)

def get_session()-> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

def SET_LOGGER(name:str, log_path:Path|str)-> logging.Logger:
    log_path = Path(log_path)
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.handlers.clear()
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )
    file_handler = logging.FileHandler(log_path,encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger