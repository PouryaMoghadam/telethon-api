import datetime
from fastapi import APIRouter
from core.config import settings

router = APIRouter()


@router.get('/')
async def system_info():
    return {
        'server': 'running',
        'data-time': datetime.datetime.now(),
        'documentation': 'http://localhost:' + str(settings.SERVER_PORT) + '/docs'
    }
