from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from app.exceptions import NotAuthenticateUser as NotAuthenticated


from app.auth.dao import UsersDAO
from app.auth.models import Users
from app.config import settings
from app.database import get_db

http_bearer = HTTPBearer(auto_error=False)

DBSession = Annotated[AsyncSession, Depends(get_db)]


async def get_current_user(
    db: DBSession,
    credentials: HTTPAuthorizationCredentials | None = Depends(http_bearer),
) -> Users:
    token = credentials.credentials if credentials else None
    if not token:
        raise NotAuthenticated
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        user_id = payload.get("sub")
    except JWTError:
        raise NotAuthenticated
    user = await UsersDAO.find_one_or_none_by_id(db, int(user_id))
    if not user or not user.is_active:
        raise NotAuthenticated
    return user


CurrentUser = Annotated[Users, Depends(get_current_user)]
