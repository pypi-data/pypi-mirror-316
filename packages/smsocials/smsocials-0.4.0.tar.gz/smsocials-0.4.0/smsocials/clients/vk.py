import json
from genericpath import getsize
from typing import Any, Dict, Literal, Tuple

import aiofiles
import aiohttp

from .base import BaseClient


class VKClient(BaseClient):
    def __init__(self, session: aiohttp.ClientSession, token: str):
        self.session = session
        self.token = token
        self.api_url = "https://api.vk.com/method/"
        self.api_version = "5.131"

    async def request(
        self, method: str, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        try:
            data["access_token"] = self.token
            data["v"] = self.api_version
            async with self.session.get(
                f"{self.api_url}{method}", params=data
            ) as response:
                response_data = await response.json()
                return response_data

        except aiohttp.ClientError as e:
            return {"error": "Client error", "details": str(e)}

        except Exception as e:
            return {"error": "Unexpected error", "details": str(e)}

    async def get_account_info(
        self, account_id: str, **data: Any
    ) -> Dict[str, Any]:
        data["user_ids"] = account_id
        response = await self.request("users.get", data)
        if "error" in response:
            return response
        response_data = response.get("response", {})
        return response_data

    async def create_resource(self, name: str, **data: Any) -> Dict[str, Any]:
        return {"": ""}

    async def create_post(self, **data: Any) -> Dict[str, Any]:
        return {"": ""}

    async def get_resources(
        self,
        filter: str,
        fields: str,
        count: int = 1000,
        offset: int = 0,
        extended: int = 1,
    ) -> Dict[str, Any]:
        data = {
            "extended": extended,
            "count": count,
            "offset": offset,
            "fields": fields,
            "filter": filter,
        }
        response = await self.request("groups.get", data)
        if "error" in response:
            return response
        response_data = response.get("response", {})
        return response_data

    async def upload_video(
        self,
        path: str,
        method: Literal["video.save", "shortVideo.create"],
        group_id: str,
        name: str,
        description: str,
        wallpost: int = 1,
    ) -> Tuple[bool, Dict[str, Any]]:
        try:
            data = {
                "group_id": group_id,
                "wallpost": wallpost,
                "file_size": getsize(path),
                "description": description,
                "name": name,
            }

            response_data = await self.request(method, data)

            if "error" in response_data:
                return False, response_data

            upload_url = response_data.get("response", {}).get("upload_url")
            if not upload_url:
                return False, {
                    "error": "Not upload url",
                    "responce": response_data,
                }

            async with aiofiles.open(path, "rb") as file:
                file_data = await file.read()

            form_data = aiohttp.FormData()
            form_data.add_field(
                "file",
                file_data,
                filename="vkvideo.mp4",
                content_type="video/mp4",
            )

            async with self.session.post(
                upload_url,
                data=form_data,
            ) as response:
                response_data = await response.text()

            if (
                method == "shortVideo.create"
                and response.status == 200
                and "<retval>1</retval>" in response_data
            ):
                return True, {
                    "success": "Clip upload complete!",
                    "response": response_data,
                }
            elif method == "video.save" and response.status == 200:
                try:
                    response_data_json = json.loads(response_data)
                except json.JSONDecodeError:
                    response_data_json = response_data

                return True, {
                    "success": "Video upload complete!",
                    "response": response_data_json,
                }
            else:
                return (
                    False,
                    {
                        "error": "Unexpected error",
                        "details": f"""Error upload video {path} in public
                    {group_id}: {response_data}""",
                    },
                )
        except Exception as e:
            return False, {"error": "Unexpected error", "details": str(e)}
