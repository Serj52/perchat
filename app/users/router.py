from fastapi import APIRouter, Response

from app.dependencies import DataBaseDep
from app.exceptions import UserAlreadyExistsException, IncorrectEmailOrPasswordException, \
    PasswordMismatchException
from app.users.auth import get_password_hash, authenticate_user, create_access_token

from app.users.crud import get_user_by_mail, create_user
from app.users.shemas import UserAuth, UserRegister

router = APIRouter(prefix='/auth', tags=['Auth'])


@router.post("/register")
async def register_user(user_data: UserRegister, session=DataBaseDep) -> dict:
    user = await get_user_by_mail(email=user_data.email, session=session)
    if user:
        raise UserAlreadyExistsException

    if user_data.password != user_data.password_check:
        raise PasswordMismatchException("Пароли не совпадают")
    hashed_password = get_password_hash(user_data.password)

    await create_user(
        name=user_data.name,
        email=user_data.email,
        hashed_password=hashed_password,
        session=session
    )

    return {'message': 'Вы успешно зарегистрированы!'}


@router.post("/login")
async def auth_user(response: Response, user_data: UserAuth, session=DataBaseDep):
    check = await authenticate_user(email=user_data.email, password=user_data.password,
                                    session=session)
    if check is None:
        raise IncorrectEmailOrPasswordException
    access_token = create_access_token({"sub": str(check.id)})
    response.set_cookie(key="users_access_token", value=access_token, httponly=True)
    return {'ok': True, 'access_token': access_token, 'refresh_token': None,
            'message': 'Авторизация успешна!'}


@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie(key="users_access_token")
    return {'message': 'Пользователь успешно вышел из системы'}
