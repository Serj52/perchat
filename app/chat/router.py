from fastapi import Depends, APIRouter
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from app.config import PATH_SETTINGS
from app.dependencies import DataBaseDep
from app.models import User
from app.users.crud import get_users
from app.users.dependencies import get_current_user

router = APIRouter(prefix='/chat', tags=['Chat'])
templates = Jinja2Templates(directory=PATH_SETTINGS["TEMPLATES"])


@router.get("/", response_class=HTMLResponse, summary="Chat Page")
async def get_chat_page(request: Request, user_data: User = Depends(get_current_user),
                        session=DataBaseDep):
    users_all = await get_users(session)
    return templates.TemplateResponse("chat.html",
                                      {"request": request, "user": user_data,
                                       'users_all': users_all})
