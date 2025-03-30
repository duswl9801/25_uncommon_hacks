from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from database import engineconn
from models import User, Base
from pydantic import BaseModel
from typing import Optional, List
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles


# Create the FastAPI app instance
app = FastAPI()

# Initialize engine and create tables if they don't exist
engine_instance = engineconn()
Base.metadata.create_all(bind=engine_instance.engine)

# Dependency for database session
def get_db():
    db = engine_instance.sessionmaker()
    try:
        yield db
    finally:
        db.close()

#Front template
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
def main_page(request: Request):
    return templates.TemplateResponse("main.html", {"request": request})

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard_page(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

# -----------------------------------------------------
# USER Endpoints
# -----------------------------------------------------

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

@app.get("/signup", response_class=HTMLResponse)
def signup_page(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})


# 회원가입 처리(POST): 폼 데이터를 받아 사용자 등록
@app.post("/signup")
def signup(
        request: Request,
        name: str = Form(...),
        password: str = Form(...),
        db: Session = Depends(get_db)
):
    # 동일한 이름의 유저가 존재하는지 확인
    existing_user = db.query(User).filter(User.name == name).first()
    if existing_user:
        # 에러 메시지를 포함하여 다시 폼 렌더링
        return templates.TemplateResponse("signup.html", {"request": request, "error": "이미 존재하는 사용자입니다."})

    # 비밀번호 해싱 후 사용자 생성
    hashed_password = get_password_hash(password)
    new_user = User(name=name, pw=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # 회원가입 성공 후 메인 페이지(또는 로그인 페이지)로 리다이렉트
    return RedirectResponse(url="/", status_code=303)


@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


# 로그인 처리 (POST) 예시
@app.post("/login")
def login(
        request: Request,
        name: str = Form(...),
        password: str = Form(...),
        db: Session = Depends(get_db)
):
    # 사용자 검증 로직 (예시)
    user = db.query(User).filter(User.name == name).first()
    if not user:
        return templates.TemplateResponse("login.html", {"request": request, "error": "존재하지 않는 사용자입니다."})

    if not pwd_context.verify(password, user.pw):
        return templates.TemplateResponse("login.html", {"request": request, "error": "비밀번호가 틀렸습니다."})

    # 로그인 성공 후 대시보드로 리다이렉트
    return RedirectResponse(url="/dashboard", status_code=303)


# -----------------------------------------------------
# Run the application
# -----------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
