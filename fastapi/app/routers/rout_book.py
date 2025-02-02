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

router = APIRouter(prefix="", tags=["booking"])


@router.get("/booking")
async def booking(
        request: Request,
        db: Annotated[Session, Depends(get_db)],
        usr: User = Depends(session_user)
):
    print(f'user_id={usr.id}, username={usr.username}')
    books = db.scalars(select(Booking)).all()
    return templates.TemplateResponse('book_list.html',
                                      {'request': request, 'user_is_auth': True, 'username': usr.username,
                                       'books': books})


@router.get("/booklist/")
async def booklist(
        request: Request,
        db: Annotated[Session, Depends(get_db)],
        id: str = '',
        usr: User = Depends(session_user)
):
    books = db.scalars(select(Booking)).all()
    return templates.TemplateResponse('book_list.html',
                                      {'request': request, 'user_is_auth': True, 'username': usr.username,
                                       'books': books})



@router.post("/bookedit/")
async def book_edit(
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
                                       'fdata': ''})


