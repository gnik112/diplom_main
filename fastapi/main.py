import uuid
from fastapi import FastAPI
from app.routers import rout_user, rout_room, rout_book
from fastapi.templating import Jinja2Templates
from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException, Request, Form, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from app.backend.db_depends import get_db
from app.models import *

from app.auth_cookies import session_user
from sqlalchemy import insert, select, update, delete

from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")


app = FastAPI()



@app.get("/")
def root(
        response: Response,
        usr: User = Depends(session_user)
):
    # redirect_url = request.url_for('signin') + '?x-error=Invalid+credentials'
    # return RedirectResponse(redirect_url, status_code=status.HTTP_302_FOUND, headers={"x-error": "Invalid credentials"})
    #return RedirectResponse('/login')
    #if usr is None:
    #    return RedirectResponse("/login")
    print('user активен:', usr.id)
    return RedirectResponse("/rooms")
    #return {"message": "Welcome"}

# @app.get("/protected")
# async def protected_route(username: str = Depends(get_current_user)):
#     return {"message": f"Hello, {username}! This is a protected resource."}


app.include_router(rout_user.router)
app.include_router(rout_room.router)
app.include_router(rout_book.router)
