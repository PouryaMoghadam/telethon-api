from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from telethon.tl.functions.messages import (GetHistoryRequest)
from app.core.client import create_client

router = APIRouter()


class ChannelBaseModel(BaseModel):
    id: int
    limit: Optional[int] = 0
    offset_id: Optional[int] = 0
    max_id: Optional[int] = 0
    min_id: Optional[int] = 0
    add_offset: Optional[int] = 0
    hash: Optional[int] = 0


@router.get('/private/user-channels')
async def get_user_channels_list():
    client = await create_client()
    await client.connect()
    channel_list = []
    async for dialog in client.iter_dialogs():
        if not dialog.is_group and dialog.is_channel:
            dialog_id = dialog.message.peer_id.channel_id
            channel = await client.get_entity(dialog_id)
            data = {
                'id': channel.id,
                'title': channel.title,
                'username': channel.username,
                'creator': channel.creator,
                'access_hash': channel.access_hash
            }
            channel_list.append(data)
    await client.disconnect()
    return channel_list


@router.post('/private/channel-info')
async def get_user_channel_info(channel: ChannelBaseModel):
    data = dict(channel)
    client = await create_client()
    await client.disconnect()
    await client.connect()
    async with client:
        try:
            my_channel = await client.get_entity(data['id'])
            messages = []
            posts = await client(GetHistoryRequest(
                peer=my_channel,
                limit=data['limit'],
                offset_date=None,
                offset_id=data['offset_id'],
                max_id=data['max_id'],
                min_id=data['min_id'],
                add_offset=data['add_offset'],
                hash=data['hash']))
            for msg in posts.messages:
                media = None
                if msg.media is not None:
                    if type(msg.media).__name__ == 'MessageMediaDocument':
                        media = {
                            'type': 'video',
                            'id': msg.media.document.id,
                            'access_hash': msg.media.document.access_hash
                        }
                    if type(msg.media).__name__ == 'MessageMediaPhoto':
                        media = {
                            'type': 'photo',
                            'id': msg.media.photo.id,
                            'access_hash': msg.media.photo.access_hash
                        }
                data = {
                    'id': msg.id,
                    'channel_id': msg.peer_id.channel_id,
                    'date': msg.date,
                    'message': msg.message,
                    'views': msg.views,
                    'forwards': msg.forwards,
                    'replies': msg.replies,
                    'media': media
                }
                messages.append(data)
            await client.disconnect()
            return messages
        except ValueError:
            await client.disconnect()
            return {
                'detail': 'Can not Find Channel With This ID'
            }
