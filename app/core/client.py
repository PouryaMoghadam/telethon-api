from dotenv import dotenv_values
from telethon import TelegramClient, functions

client_info = dotenv_values('.env')
client_dict = dict(client_info)
api_id = client_dict['TELEGRAM_API_ID']
api_hash = client_dict['TELEGRAM_API_HASH']
phone = client_dict['TELEGRAM_API_PHONE']
username = client_dict['TELEGRAM_API_USERNAME']


async def create_client():
    return TelegramClient(username, api_id, api_hash)


async def check_client_authorized():
    client = await create_client()
    await client.connect()
    return await client.is_user_authorized()


def display_url_as_qr(url):
    print(url)
    pass


async def login_with_qr():
    client = await create_client()
    await client.connect()
    qr_login = await client.qr_login()
    display_url_as_qr(qr_login.url)


async def send_code_request():
    client = await create_client()
    await client.connect()
    return await client.send_code_request(phone=phone)


async def client_sign_in(user_code):
    print(user_code)
    client = await create_client()
    await client.connect()
    result = await client.sign_in(phone=phone, code=user_code)
    return result
