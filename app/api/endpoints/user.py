from fastapi import APIRouter
from pydantic import BaseModel
from core.client import create_client, send_code_request, client_sign_in, login_with_qr

router = APIRouter()


class SignIn(BaseModel):
    code: str
    phone_hash_code: str


@router.get('/private/profile')
async def get_user_profile():
    client = await create_client()
    await client.connect()
    profile = await client.get_me()
    await client.disconnect()
    return profile


@router.get('/send-qr-code')
async def send_login_rq_code():
    result = await login_with_qr()
    # https: // www.qrcode - monkey.com /
    return result


@router.get('/send-code')
async def send_sign_in_code():
    result = await send_code_request()
    return result


@router.post('/sign-in')
async def user_sign_in(sign_in: SignIn):
    data = dict(sign_in)
    return await client_sign_in(user_code=data['code'], hash_code=data['phone_hash_code'])
