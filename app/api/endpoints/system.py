import datetime
from fastapi import APIRouter

router = APIRouter()


@router.get('/')
async def system_info():
    return {
        'server': 'running',
        'data-time': datetime.datetime.now(),
        'documentation': 'http://localhost:7000/docs'
    }
