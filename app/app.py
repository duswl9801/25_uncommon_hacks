from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from database import engineconn
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from pydantic import BaseModel
from typing import Optional, List
from fastapi.staticfiles import StaticFiles
import os
from models import User, UserGame, Guide, GameSession, Base, Emotion
from datetime import timedelta


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


# Front template
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
def main_page(request: Request):
    return templates.TemplateResponse("main.html", {"request": request})


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard_page(request: Request, db: Session = Depends(get_db)):
    # Fetch Emotion and GameSession data
    emotions = db.query(Emotion).order_by(Emotion.created_at).all()
    sessions = db.query(GameSession).all()

    # Prepare chart data
    mapping = {"negative": -1, "neutral": 0, "positive": 1}
    chart_labels = [em.created_at.strftime("%H:%M") for em in emotions]
    chart_data = [mapping.get(em.emotion_label.lower(), 0) for em in emotions]

    # Calculate total play time from sessions
    total_duration = timedelta()
    for s in sessions:
        if s.started_time and s.created_at:
            total_duration += s.started_time - s.created_at

    total_minutes = int(total_duration.total_seconds() // 60)
    total_hours = total_minutes // 60
    remaining_minutes = total_minutes % 60
    total_time_str = f"{total_hours:02}:{remaining_minutes:02}"

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "chart_labels": chart_labels,
        "chart_data": chart_data,
        "total_play_time": total_time_str
    })

# -----------------------------------------------------
# USER Endpoints
# -----------------------------------------------------

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


@app.get("/signup", response_class=HTMLResponse)
def signup_page(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})


# 회원가입 처리 (POST): 폼 데이터와 게임 경로를 받아 사용자 등록 및 UserGame 테이블에 저장
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
        return templates.TemplateResponse("signup.html", {"request": request, "error": "이미 존재하는 사용자입니다."})

    # 비밀번호 해싱 후 사용자 생성
    hashed_password = get_password_hash(password)
    new_user = User(name=name, pw=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # 회원가입 성공 후 /usergame 페이지로 리다이렉트 (user_id 전달)
    return RedirectResponse(url=f"/usergame?user_id={new_user.id}", status_code=303)


@app.get("/usergame", response_class=HTMLResponse)
def usergame_page(request: Request, user_id: int):
    # user_id를 이용해 필요한 정보를 조회할 수도 있습니다.
    return templates.TemplateResponse("user_game.html", {"request": request, "user_id": user_id})


# 유저 게임 정보 저장 처리 (POST)
@app.post("/usergame")
def post_usergame(
        request: Request,
        user_id: int = Form(...),
        game_path: str = Form(...),
        db: Session = Depends(get_db)
):
    # 입력된 게임 경로에서 파일명(마지막 경로 부분) 추출
    game_name = os.path.basename(game_path)

    # UserGame 레코드 생성 (guide 정보는 아직 없으므로 None 사용)
    new_user_game = UserGame(
        user_id=user_id,
        game_path=game_path,
        game_name=game_name,
        guide_id=None  # guide 정보는 나중에 운영자가 입력
    )
    db.add(new_user_game)
    db.commit()

    # 저장 후 대시보드 등 다른 페이지로 리다이렉트 (여기서는 대시보드로)
    return RedirectResponse(url="/dashboard", status_code=303)



@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


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
    return RedirectResponse(url="/dashboard", status_code=303)


# -----------------------------------------------------
# Run the application
# -----------------------------------------------------
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
