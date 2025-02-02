from fastapi import Cookie, Depends, HTTPException, status
from app.backend.db_depends import get_db
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models import User
from typing import Annotated

COOKIE_SESSION_ID_KEY = 'web-app-session-id'

def session_user(
        db: Annotated[Session, Depends(get_db)],
        session_id: str = Cookie(alias=COOKIE_SESSION_ID_KEY, default=None)
):
    exept_redirect = HTTPException(
        status_code=status.HTTP_307_TEMPORARY_REDIRECT,
        headers={'Location': '/login'}
    )
    if session_id == None:
        raise exept_redirect
    dt = session_id.split('-')
    if len(dt) != 2:
        raise exept_redirect
    if len(dt[0]) < 1:
        raise exept_redirect
    if len(dt[1]) < 1:
        raise exept_redirect
    user = db.scalar(select(User).where(User.id == dt[0]))
    if user is None:
        raise exept_redirect
    if dt[1] != user.access_token:
        raise exept_redirect
    return user
