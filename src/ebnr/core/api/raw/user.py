
import httpx

from ebnr.core.cryto.weapi import make_weapi_form
from ebnr.core.utils import make_client


async def get_user_info(
    *,
    client: httpx.AsyncClient | None = None,
    cookies: dict[str, str] | None = None,
) -> dict:
    request_url = "https://music.163.com/weapi/nuser/account/get"
    form = make_weapi_form("{}")
    async with client or make_client() as client:
        response = await client.post(request_url, data=form, cookies=cookies)
    return response.json()
