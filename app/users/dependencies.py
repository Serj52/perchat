from fastapi import Request, HTTPException, status, Depends
from jose import jwt, JWTError
from datetime import datetime, timezone

from app.config import AUTH_SETTINGS
from app.dependencies import DataBaseDep
from app.exceptions import TokenExpiredException, NoJwtException, NoUserIdException, TokenNoFoundException
from app.users.crud import get_user_by_id


def get_token(request: Request):
    token = request.cookies.get('users_access_token')
    if not token:
        raise TokenNoFoundException
    return token


async def get_current_user(token: str = Depends(get_token), session=DataBaseDep):
    try:
        payload = jwt.decode(token, AUTH_SETTINGS['SECRET_KEY'], algorithms=AUTH_SETTINGS['ALGORITHM'])
    except JWTError:
        raise NoJwtException

    expire: str = payload.get('exp')
    expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
    if (not expire) or (expire_time < datetime.now(timezone.utc)):
        raise TokenExpiredException

    user_id: str = payload.get('sub')
    if not user_id:
        raise NoUserIdException

    user = await get_user_by_id(int(user_id), session)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found')
    return user
