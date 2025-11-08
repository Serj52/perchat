from fastapi import Depends

from app.database import get_db_session

DataBaseDep = Depends(get_db_session)