from fastapi import FastAPI,Request,HTTPException,Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from pydantic import BaseModel
import models
from database import engine,SessionLocal
from sqlalchemy.orm import Session


models.Base.metadata.create_all(bind=engine)
app = FastAPI()
def get_db():
    try:
        db=SessionLocal()
        yield db
    finally:
        db.close()    


class Voters(BaseModel):
    # id:Optional[int]=None
    username:str
    password:str

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def show_users(db:Session=Depends(get_db)):
    return db.query(models.User).all()

@app.post("/api/login/")
def login(username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == username, models.User.password == password).first()
    if user:
        return {"message": "Success"}
    else:
        return {"message": "Invalid username or password"}

@app.post("/api/register/")
def register(username: str, password: str, db: Session = Depends(get_db)):
    user = models.User(username=username, password=password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "Success"}

# @app.get('/voters')
# def get_all_voters():
#     return voters

# @app.get('/voter/{v_id}')
# def get_voters(v_id:int):
#     voter =[v for v in voters if v['id']==v_id]
#     return voter[0] if len(voter)>0 else {}

# @app.post('/voter')
# async def voted(request: Request):
#     json_data = await request.json()
#     v_id = json_data['id']
#     for v in voters:
#         if v['id']==v_id:
#             v['voted']=True
#     return JSONResponse(content={"msg":"updated successfully"})




    