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
# -----------------------------------------------------
# GUIDE Endpoints
# -----------------------------------------------------

class GuideCreate(BaseModel):
    game_guide: str
    screenshot: Optional[bytes] = None

class GuideOut(BaseModel):
    id: int
    game_guide: str

    class Config:
        orm_mode = True

@app.post("/guides/", response_model=GuideOut)
def create_guide(guide: GuideCreate, db: Session = Depends(get_db)):
    db_guide = Guide(game_guide=guide.game_guide, screenshot=guide.screenshot)
    db.add(db_guide)
    db.commit()
    db.refresh(db_guide)
    return db_guide

@app.get("/guides/", response_model=List[GuideOut])
def read_guides(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    guides = db.query(Guide).offset(skip).limit(limit).all()
    return guides

@app.get("/guides/{guide_id}", response_model=GuideOut)
def read_guide(guide_id: int, db: Session = Depends(get_db)):
    guide = db.query(Guide).filter(Guide.id == guide_id).first()
    if not guide:
        raise HTTPException(status_code=404, detail="Guide not found")
    return guide

@app.put("/guides/{guide_id}", response_model=GuideOut)
def update_guide(guide_id: int, guide_update: GuideCreate, db: Session = Depends(get_db)):
    guide = db.query(Guide).filter(Guide.id == guide_id).first()
    if not guide:
        raise HTTPException(status_code=404, detail="Guide not found")
    guide.game_guide = guide_update.game_guide
    if guide_update.screenshot is not None:
        guide.screenshot = guide_update.screenshot
    db.commit()
    db.refresh(guide)
    return guide

@app.delete("/guides/{guide_id}")
def delete_guide(guide_id: int, db: Session = Depends(get_db)):
    guide = db.query(Guide).filter(Guide.id == guide_id).first()
    if not guide:
        raise HTTPException(status_code=404, detail="Guide not found")
    db.delete(guide)
    db.commit()
    return {"detail": "Guide deleted"}

# -----------------------------------------------------
# USERGAME Endpoints
# -----------------------------------------------------

class UserGameCreate(BaseModel):
    user_id: int
    game_path: str
    game_name: str
    guide_id: int

class UserGameOut(BaseModel):
    id: int
    user_id: int
    game_path: str
    game_name: str
    guide_id: int

    class Config:
        orm_mode = True

@app.post("/usergames/", response_model=UserGameOut)
def create_usergame(usergame: UserGameCreate, db: Session = Depends(get_db)):
    db_usergame = UserGame(**usergame.dict())
    db.add(db_usergame)
    db.commit()
    db.refresh(db_usergame)
    return db_usergame

@app.get("/usergames/", response_model=List[UserGameOut])
def read_usergames(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    usergames = db.query(UserGame).offset(skip).limit(limit).all()
    return usergames

@app.get("/usergames/{usergame_id}", response_model=UserGameOut)
def read_usergame(usergame_id: int, db: Session = Depends(get_db)):
    usergame = db.query(UserGame).filter(UserGame.id == usergame_id).first()
    if not usergame:
        raise HTTPException(status_code=404, detail="UserGame not found")
    return usergame

@app.put("/usergames/{usergame_id}", response_model=UserGameOut)
def update_usergame(usergame_id: int, usergame_update: UserGameCreate, db: Session = Depends(get_db)):
    usergame = db.query(UserGame).filter(UserGame.id == usergame_id).first()
    if not usergame:
        raise HTTPException(status_code=404, detail="UserGame not found")
    for key, value in usergame_update.dict().items():
        setattr(usergame, key, value)
    db.commit()
    db.refresh(usergame)
    return usergame

@app.delete("/usergames/{usergame_id}")
def delete_usergame(usergame_id: int, db: Session = Depends(get_db)):
    usergame = db.query(UserGame).filter(UserGame.id == usergame_id).first()
    if not usergame:
        raise HTTPException(status_code=404, detail="UserGame not found")
    db.delete(usergame)
    db.commit()
    return {"detail": "UserGame deleted"}

# -----------------------------------------------------
# GAMESESSION Endpoints
# -----------------------------------------------------

class GameSessionCreate(BaseModel):
    user_id: int
    guide_id: int
    finished_time: Optional[str] = None  # Expecting an ISO datetime string

class GameSessionOut(BaseModel):
    id: int
    user_id: int
    guide_id: int
    finished_time: Optional[str] = None

    class Config:
        orm_mode = True

@app.post("/gamesessions/", response_model=GameSessionOut)
def create_gamesession(gamesession: GameSessionCreate, db: Session = Depends(get_db)):
    db_gamesession = GameSession(
        user_id=gamesession.user_id,
        guide_id=gamesession.guide_id,
        finished_time=gamesession.finished_time
    )
    db.add(db_gamesession)
    db.commit()
    db.refresh(db_gamesession)
    return db_gamesession

@app.get("/gamesessions/", response_model=List[GameSessionOut])
def read_gamesessions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    gamesessions = db.query(GameSession).offset(skip).limit(limit).all()
    return gamesessions

@app.get("/gamesessions/{gamesession_id}", response_model=GameSessionOut)
def read_gamesession(gamesession_id: int, db: Session = Depends(get_db)):
    gamesession = db.query(GameSession).filter(GameSession.id == gamesession_id).first()
    if not gamesession:
        raise HTTPException(status_code=404, detail="GameSession not found")
    return gamesession

@app.put("/gamesessions/{gamesession_id}", response_model=GameSessionOut)
def update_gamesession(gamesession_id: int, gamesession_update: GameSessionCreate, db: Session = Depends(get_db)):
    gamesession = db.query(GameSession).filter(GameSession.id == gamesession_id).first()
    if not gamesession:
        raise HTTPException(status_code=404, detail="GameSession not found")
    for key, value in gamesession_update.dict().items():
        setattr(gamesession, key, value)
    db.commit()
    db.refresh(gamesession)
    return gamesession

@app.delete("/gamesessions/{gamesession_id}")
def delete_gamesession(gamesession_id: int, db: Session = Depends(get_db)):
    gamesession = db.query(GameSession).filter(GameSession.id == gamesession_id).first()
    if not gamesession:
        raise HTTPException(status_code=404, detail="GameSession not found")
    db.delete(gamesession)
    db.commit()
    return {"detail": "GameSession deleted"}

# -----------------------------------------------------
# EMOTION Endpoints
# -----------------------------------------------------

class EmotionCreate(BaseModel):
    emotion_label: str
    screenshot: Optional[bytes] = None

class EmotionOut(BaseModel):
    id: int
    emotion_label: str

    class Config:
        orm_mode = True

@app.post("/emotions/", response_model=EmotionOut)
def create_emotion(emotion: EmotionCreate, db: Session = Depends(get_db)):
    db_emotion = Emotion(**emotion.dict())
    db.add(db_emotion)
    db.commit()
    db.refresh(db_emotion)
    return db_emotion

@app.get("/emotions/", response_model=List[EmotionOut])
def read_emotions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    emotions = db.query(Emotion).offset(skip).limit(limit).all()
    return emotions

@app.get("/emotions/{emotion_id}", response_model=EmotionOut)
def read_emotion(emotion_id: int, db: Session = Depends(get_db)):
    emotion = db.query(Emotion).filter(Emotion.id == emotion_id).first()
    if not emotion:
        raise HTTPException(status_code=404, detail="Emotion not found")
    return emotion

@app.put("/emotions/{emotion_id}", response_model=EmotionOut)
def update_emotion(emotion_id: int, emotion_update: EmotionCreate, db: Session = Depends(get_db)):
    emotion = db.query(Emotion).filter(Emotion.id == emotion_id).first()
    if not emotion:
        raise HTTPException(status_code=404, detail="Emotion not found")
    for key, value in emotion_update.dict().items():
        setattr(emotion, key, value)
    db.commit()
    db.refresh(emotion)
    return emotion

@app.delete("/emotions/{emotion_id}")
def delete_emotion(emotion_id: int, db: Session = Depends(get_db)):
    emotion = db.query(Emotion).filter(Emotion.id == emotion_id).first()
    if not emotion:
        raise HTTPException(status_code=404, detail="Emotion not found")
    db.delete(emotion)
    db.commit()
    return {"detail": "Emotion deleted"}

# -----------------------------------------------------
# Run the application
# -----------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
