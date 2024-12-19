from typing import Any, Dict

import aiohttp

from ..clients.vk import VKClient


class VKService:
    def __init__(self, token: str):
        self.token = token
        self.session = lambda: aiohttp.ClientSession()

    async def get_user_info(self, user_id: str) -> Dict[str, Any]:
        async with self.session() as session:
            vk_client = VKClient(session, self.token)
            result = await vk_client.get_account_info(user_id)
            return result

    async def get_groups(
        self,
        filter: str,
        fields: str,
        count: int = 1000,
        offset: int = 0,
        extended: int = 1,
    ) -> Dict[str, Any]:
        async with self.session() as session:
            vk_client = VKClient(session, self.token)
            result = await vk_client.get_resources(
                filter, fields, count, offset, extended
            )
            return result

    async def upload_clip(
        self,
        path: str,
        group_id: str,
        description: str,
        wallpost: bool = True,
    ) -> Dict[str, Any]:
        async with self.session() as session:
            vk_client = VKClient(session, self.token)
            result = await vk_client.upload_video(
                path,
                "shortVideo.create",
                group_id,
                "",
                description,
                1 if wallpost else 0,
            )
            return result

    async def upload_video(
        self,
        path: str,
        group_id: str,
        name: str,
        description: str,
        wallpost: bool = True,
    ) -> Dict[str, Any]:
        async with self.session() as session:
            vk_client = VKClient(session, self.token)
            result = await vk_client.upload_video(
                path,
                "video.save",
                group_id,
                name,
                description,
                1 if wallpost else 0,
            )
            return result
