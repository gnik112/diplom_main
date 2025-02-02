import uuid
from fastapi import APIRouter, Depends, status, HTTPException, Request, Form, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from app.backend.db_depends import get_db
from typing import Annotated
from app.auth_cookies import session_user, COOKIE_SESSION_ID_KEY
from app.models import *
from sqlalchemy import insert, select, update, delete

from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="templates")


#from slugify import slugify

router = APIRouter(prefix="", tags=["user"])




def make_new_token(user_id):
    token = uuid.uuid4().hex
    cookie_token = str(user_id) + '-' + token
    return token, cookie_token



@router.get("/login")
async def login_get(request: Request):
    return templates.TemplateResponse('login.html', {'request': request, 'user_is_auth': False})


@router.post("/login")
async def login_post(
        request: Request,
        db: Annotated[Session, Depends(get_db)],
        username: Annotated[str, Form()],
        password: Annotated[str, Form()]
):
    #print('username=' + username, 'password=' + password)
    user_check = db.scalar(select(User).where(User.username == username))
    #print('user_check=' + str(user_check.username), 'user_check_pass=' + str(user_check.password))
    if user_check is None or user_check.password != password:
        return templates.TemplateResponse('login.html', {'request': request, 'user_is_auth': False})
    # Создание токена соединения
    token, cookie_token = make_new_token(user_check.id)
    # Запись токена в БД
    db.execute(update(User).where(User.username == username).values(access_token=token))
    db.commit()
    #print('cookie_token=', cookie_token)
    # Переход с отправкой куки
    red_resp = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    red_resp.set_cookie(key=COOKIE_SESSION_ID_KEY, value=cookie_token)
    return red_resp


@router.get("/register")
async def register_get(request: Request):
    return templates.TemplateResponse('register.html', {'request': request})


@router.post("/register")
async def register_post(
        request: Request,
        db: Annotated[Session, Depends(get_db)],
        username: Annotated[str, Form()],
        password1: Annotated[str, Form()],
        password2: Annotated[str, Form()]
):
    print('username=' + username, 'password1=' + password1, 'password2=' + password2)
    # Проверка пароля и имени пользователя
    if len(password1) > 7 and password1 == password2 and len(username) > 4:
        # Проверка уникальности имени пользователя
        user = db.scalar(select(User).where(User.username == username))
        if user is None:
            # Создание нового пользователя в бд
            db.execute(insert(User).values(username=username, password=password1, access_token=''))
            db.commit()
            user_new = db.scalar(select(User).where(User.username == username))
            # Создание токена соединения и запись в БД
            token, cookie_token = make_new_token(user_new.id)
            db.execute(update(User).where(User.username == username).values(access_token=token))
            db.commit()
            # Переход с отправкой куки
            red_resp = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
            red_resp.set_cookie(key=COOKIE_SESSION_ID_KEY, value=cookie_token)
            return red_resp
    #return RedirectResponse('/register')
    return templates.TemplateResponse('register.html', {'request': request})


@router.get("/logout")
async def login_out(
        db: Annotated[Session, Depends(get_db)],
        usr: User = Depends(session_user)
):
    # Стирание токена в БД
    db.execute(update(User).where(User.id == usr.id).values(access_token='111111'))
    db.commit()
    # Переход на вход
    return RedirectResponse('/login')

