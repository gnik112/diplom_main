import uuid
from fastapi import APIRouter, Depends, status, HTTPException, Request, Form, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from app.backend.db_depends import get_db
from typing import Annotated

from app.auth_cookies import session_user
from app.models import *
# from app.schemas import CreateUser, UpdateUser, LoginUser
from sqlalchemy import insert, select, update, delete

from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

# from slugify import slugify

router = APIRouter(prefix="", tags=["room"])


@router.get("/rooms")
async def room_list(
        request: Request,
        db: Annotated[Session, Depends(get_db)],
        usr: User = Depends(session_user)
):
    print(f'user_id={usr.id}, username={usr.username}')
    rooms = db.scalars(select(Room)).all()
    return templates.TemplateResponse('rooms.html',
                                      {'request': request, 'user_is_auth': True, 'username': usr.username,
                                       'rooms': rooms})


@router.get("/room_edit/")
async def room_edit(
        request: Request,
        db: Annotated[Session, Depends(get_db)],
        id: str = '',
        usr: User = Depends(session_user)
):
    print('get id=', id)
    if id == '':
        content = {'caption': 'создание нового помещения', 'key_title': 'Создать'}
    else:
        room = db.scalar(select(Room).where(Room.id == id))
        if room is None:
            content = {'caption': 'создание нового помещения', 'key_title': 'Создать'}
        else:
            content = {
                'caption': 'изменение данных',
                'roomname': room.name,
                'people_count': room.people_count,
                'cost': room.cost,
                'key_title': 'Изменить'
            }
    return templates.TemplateResponse('room_edit.html',
                                      {'request': request, 'user_is_auth': True, 'username': usr.username,
                                       'fdata': content})

@router.post("/room_edit/")
async def room_edit(
        request: Request,
        db: Annotated[Session, Depends(get_db)],
        roomname: Annotated[str, Form()],
        people_count: Annotated[str, Form()],
        cost: Annotated[str, Form()],
        id: str = '',
        usr: User = Depends(session_user)
):
    print('get id=', id)

    return templates.TemplateResponse('room_edit.html',
                                      {'request': request, 'user_is_auth': True, 'username': usr.username,
                                       'fdata': content})


@router.get("/room_busy/")
async def room_busy(
        request: Request,
        db: Annotated[Session, Depends(get_db)],
        id: str = '',
        usr: User = Depends(session_user)
):
    content = {
        'caption': 'изменение данных',
        'busy_list': [],
        'people_count': '',
        'cost': '',
        'key_title': 'Изменить'
    }
    return templates.TemplateResponse('room_busy.html',
                                      {'request': request, 'user_is_auth': True, 'username': usr.username,
                                       'fdata': content})
