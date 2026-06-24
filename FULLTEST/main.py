from fastapi import FastAPI,Depends,HTTPException
from FULLTEST.log_sql_config import SET_LOGGER, create_db_and_tables, get_session
from pathlib import Path
from sqlmodel import SQLModel,Field,Session,select
from contextlib import asynccontextmanager
from typing import Annotated



@asynccontextmanager
async def lifespan(app:FastAPI):
    create_db_and_tables()
    yield

LOG_FILE = Path(__file__).resolve().parents[0] / "test_logs.log"
logger = SET_LOGGER("小测试用",LOG_FILE)
SessionDep = Annotated[Session, Depends(get_session)]
app = FastAPI(title="FASTapi和SOLmodel的回顾",lifespan=lifespan)

class ARequest(SQLModel):
    age: int
    description:str

class AData(SQLModel,table=True):
    id:int|None =Field(default=None,primary_key=True)
    age: int
    description:str

class AResponse(SQLModel):
    id:int
    age: int
    description:str
    message:str = "RESPONSE OK"

class AUpdate(SQLModel):
    age: int|None = None
    description:str|None = None


@app.post(
        "/create",
        description="增加数据",
        response_model=AResponse)
def create(input:ARequest,session:SessionDep)->AResponse:
    data = AData(
        age=input.age,
        description=input.description
    )
    session.add(data)
    session.commit()
    session.refresh(data)
    return AResponse(id=data.id,age=data.age,description=data.description)

@app.get(
    "/check",
    description="查找数据",
    response_model=AResponse
)
def check(session:SessionDep,id:int|None = None,key:str|None = None)->AResponse:
    
    if key:
        statement = select(AData).where(AData.description == key)
        result = session.exec(statement).first()
    if id:
        result = session.get(AData,id)
    if not result:
        raise HTTPException(status_code=404,detail="此数据不存在")
    return AResponse(id=result.id,age=result.age,description=result.description,message="查找结束")

@app.patch(
    "/update",
    description="修改数据",
    response_model=AResponse
)
def modify(session:SessionDep,data_up:AUpdate,id:int)->AResponse:
    db_data = session.get(AData,id)
    update = data_up.model_dump(exclude_unset=True)
    for key,value in update.items():
        setattr(db_data,key,value)
    session.add(db_data)
    session.commit()
    session.refresh(db_data)
    return AResponse(
        id=db_data.id,
        age=db_data.age,
        description=db_data.description,
        message="修改结束"
    )
    

@app.delete(
    "/delete",
    description="修改数据"
)
def delete(session:SessionDep,id:int):
    db_data = session.get(AData,id)
    session.delete(db_data)
    session.commit()
    if not session.get(AData,id):
        return {
        "id": id,
        "message": f"ID:{id}的数据已删除"
    }
    