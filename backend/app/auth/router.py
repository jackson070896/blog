from fastapi import APIRouter, HTTPException, status

from app.auth.dao import UsersDAO
from app.auth.schemas import UserLogin, UserRegister, UserResponse
from app.auth.utils import create_access_token, hash_password, verify_password
from app.dependencies import CurrentUser, DBSession
from app.exceptions import IncorrectEmailOrPassword

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(data: UserRegister, session: DBSession):
    if await UsersDAO.find_one_or_none(session, username=data.username):
        raise HTTPException(status_code=409, detail="Это имя уже занято")
    if await UsersDAO.find_one_or_none(session, email=data.email):
        raise HTTPException(status_code=409, detail="Этот email уже занят")
    user = await UsersDAO.add(
        session,
        username=data.username,
        email=data.email,
        password=hash_password(data.password),
    )
    return user


@router.post("/login")
async def login(data: UserLogin, session: DBSession):
    user = await UsersDAO.find_one_or_none(session, username=data.username)
    if not user or not verify_password(data.password, user.password):
        raise IncorrectEmailOrPassword
    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}


@router.post("/logout")
async def logout():
    return {"detail": "Выход выполнен"}


@router.get("/me", response_model=UserResponse)
async def me(user: CurrentUser):
    return user
