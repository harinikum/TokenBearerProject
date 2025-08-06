from fastapi import FastAPI, HTTPException, Header, status
from fastapi.middleware.cors import CORSMiddleware
import mysql.connector
from pydantic import BaseModel
import uuid

app=FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
def get_db_connection():
    return mysql.connector.connect(
        host="zwoz6x.h.filess.io",
        user="TokenBearerProject_arrangetax",
        password="cda7b56d760bfa6cff1942999f5e7be70e245e07",
        database="TokenBearerProject_arrangetax",
        port=3307
    )
valid_token=set()

class Logindata(BaseModel):
    username : str
    password : str
@app.post('/login')
def user_login(data:Logindata,authorization :str = Header(None)):
    token = authorization.split(" ")[1]
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    if authorization == f"Bearer {token}":
        cursor.execute(f"select username,password from users where username='{data.username}' and password='{data.password}'")
        return {"Message":"Login Successfully"}
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid token",
        headers={"WWW-Authentication": "bearer"}
    )
class Update(BaseModel):
    username:str
    password:str
    mail:str
    phoneno:int
@app.post("/insert")
def user_register(data:Update):
    token = str(uuid.uuid4())
    valid_token.add(token)
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute(f"INSERT INTO users ( username, password, email, phoneno, token) VALUES ('{data.username}', '{data.password}', '{data.mail}', '{data.phoneno}','{token}')")
    db.commit()
    db.close()
    return {"Message":"user access to insert data","token":token}

class Delete(BaseModel):
    id:int
@app.post("/delete")
def user_delete(data:Delete,authorization:str = Header(None)):
    token = authorization.split(" ")[1]
    if authorization == f"Bearer {token}":
      db = get_db_connection()
      cursor = db.cursor()
      cursor.execute(f"delete from users where id='{data.id}'")
      db.commit()
      db.close()
      return{"Message":"Delete"}
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid token",
        headers={"WWW-Authentication": "bearer"}
    )
class UpdateUsername(BaseModel):
    id: int
    new_username: str
@app.post("/update")
def update_username(data: UpdateUsername,authorization:str = Header(None)):
    token = authorization.split(" ")[1]
    db = get_db_connection()
    cursor = db.cursor()
    if authorization == f"Bearer {token}":
        cursor.execute(f"UPDATE users SET username = '{data.new_username}' WHERE id = '{data.id}'")
        db.commit()
        db.close()
        return {"Message": "updated"}
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid token",
        headers={"WWW-Authentication": "bearer"}
    )
@app.get("/select")
def select_users():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    cursor.close()
    db.close()
    return {"user": users}