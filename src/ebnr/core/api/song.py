import asyncio
from itertools import chain

import httpx

from ebnr.core.api import raw
from ebnr.core.parser import (
    parse_album_json,
    parse_audio_json,
    parse_lyric_json,
    parse_playlist_json,
    parse_song_json,
)
from ebnr.core.types import Encoding, Quality, SongInfo
from ebnr.core.utils import extract_playlist_tracks, make_client, remap_result


async def get_audio(
    ids: list[int],
    quality: Quality = Quality.STANDARD,
    encoding: Encoding = Encoding.FLAC,
    *,
    http_client: httpx.AsyncClient | None = None,
    cookies: dict[str, str] | None = None,
):
    # 2000 一批都没问题, 但大了容易超时
    batches = [ids[i : i + 1000] for i in range(0, len(ids), 1000)]

    async def get_audio_batch(current_ids: list[int]):
        audios_data = await raw.song.get_audio(
            current_ids, quality, encoding, http_client=client, cookies=cookies
        )
        return [parse_audio_json(audio_data) for audio_data in audios_data["data"]]

    with http_client or make_client(http2=True) as client:
        tasks = [get_audio_batch(current_ids) for current_ids in batches]
        results = await asyncio.gather(*tasks)

    return remap_result(ids, chain(*results))


async def get_song_info(
    ids: list[int],
    *,
    http_client: httpx.AsyncClient | None = None,
    cookies: dict[str, str] | None = None,
):
    batches = [ids[i : i + 1000] for i in range(0, len(ids), 1000)]

    async def get_song_batch(current_ids: list[int]):
        songs_info_data = await raw.song.get_song_info(
            current_ids, http_client=client, cookies=cookies
        )
        return [parse_song_json(info) for info in songs_info_data["songs"]]

    with http_client or make_client(http2=True) as client:
        tasks = [get_song_batch(current_ids) for current_ids in batches]
        results = await asyncio.gather(*tasks)

    return remap_result(ids, chain(*results))


async def get_lyric(
    id: int,
    *,
    http_client: httpx.AsyncClient | None = None,
    cookies: dict[str, str] | None = None,
):
    if (
        lyric_data := await raw.song.get_lyric(
            id, http_client=http_client, cookies=cookies
        )
    ) is None:
        return None
    return parse_lyric_json(lyric_data)


async def search(
    keyword: str,
    limit: int = 10,
    *,
    http_client: httpx.AsyncClient | None = None,
    cookies: dict[str, str] | None = None,
):
    search_data = await raw.song.search(
        keyword, limit, http_client=http_client, cookies=cookies
    )
    return [parse_song_json(song_data) for song_data in search_data["result"]["songs"]]


async def get_playlist(
    id: int,
    *,
    http_client: httpx.AsyncClient | None = None,
    cookies: dict[str, str] | None = None,
):
    playlist_data = await raw.song.get_playlist(
        id, http_client=http_client, cookies=cookies
    )
    if playlist_data is None:
        return None
    return parse_playlist_json(playlist_data["playlist"])


async def get_tracks(
    id: int,
    limit: int = 1000,
    page: int = 0,
    *,
    http_client: httpx.AsyncClient | None = None,
    cookies: dict[str, str] | None = None,
) -> list[SongInfo | None] | None:
    data = await get_playlist(id, http_client=http_client, cookies=cookies)
    if data is None:
        return None
    extracted = extract_playlist_tracks(data.track_ids, data.tracks, limit, page)
    return extracted.known + (await get_song_info(extracted.unknown, cookies=cookies))


async def get_album(
    id: int,
    *,
    http_client: httpx.AsyncClient | None = None,
    cookies: dict[str, str] | None = None,
):
    album_data = await raw.song.get_album(id, http_client=http_client, cookies=cookies)
    if album_data is None:
        return None
    return parse_album_json(album_data)
