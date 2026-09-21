from dataclasses import dataclass
from datetime import datetime
from enum import IntEnum, StrEnum


class Quality(StrEnum):
    # 标准
    STANDARD = "standard"
    # 较高
    HIGHER = "higher"
    # 极高
    EXHIGH = "exhigh"
    # 无损
    LOSSLESS = "lossless"
    # Hi-Res
    HIRES = "hires"
    # 高清环绕声
    JYEFFECT = "jyeffect"
    # 沉浸环绕声
    SKY = "sky"
    # 超清母带
    JYMASTER = "jymaster"


class Encoding(StrEnum):
    # MP3编码
    MP3 = "mp3"
    # FLAC编码
    FLAC = "flac"


@dataclass
class AudioInfo:
    id: int
    url: str | None
    # 编码
    encoding: Encoding | None
    # 比特率
    bitrate: int
    # 文件大小
    size: int
    md5: str
    # 时长(毫秒)
    duration: int
    # 采样率
    sample_rate: int
    # 响度增益
    gain: float
    # 音频峰值
    peak: float
    # 是否已付费
    payed: bool
    # 是否付费
    fee: bool


@dataclass
class ArtistShort:
    id: int
    name: str
    translations: list[str] | None
    alias: list[str] | None


@dataclass
class AlbumShort:
    id: int
    name: str
    translations: list[str] | None
    cover_url: str | None


@dataclass
class QualityInfo:
    # 比特率
    bitrate: int
    # 文件大小
    size: int
    # 采样率
    sample_rate: int | None


@dataclass
class Qualities:
    # 标准音质(l)
    standard: QualityInfo | None
    # 高音质
    higher: QualityInfo | None
    # 极高音质(h)
    exhigh: QualityInfo | None
    # 无损音质(sq)
    lossless: QualityInfo | None
    # Hires音质(hr)
    hires: QualityInfo | None
    # 沉浸环绕声
    sky: QualityInfo | None
    # 高清环绕声
    jyeffect: QualityInfo | None
    # 超清母带()
    jymaster: QualityInfo | None


@dataclass
class SongInfo:
    id: int
    name: str
    main_title: str | None
    additional_title: str | None
    translations: list[str] | None
    alias: list[str] | None
    # 流行度(0-100)
    pop: float
    # 艺术家
    artists: list[ArtistShort]
    # 专辑
    album: AlbumShort | None
    # MV id
    music_video_id: int | None
    # 发布时间
    publish_time: datetime | None
    # 质量
    qualities: Qualities


@dataclass
class LyricContributor:
    id: int
    user_id: int
    nickname: str
    update_time: int


@dataclass
class LyricContent:
    version: int
    lyric: str


@dataclass
class LyricData:
    lyric_contributor: LyricContributor | None
    translation_contributor: LyricContributor | None

    original_lyric: LyricContent | None
    translated_lyric: LyricContent | None
    romaji_lyric: LyricContent | None
    karaoke_lyric: LyricContent | None
    word_by_word_lyric: LyricContent | None


@dataclass
class PlaylistCreator:
    user_id: int
    nickname: str
    signature: str
    avatar_url: str
    background_url: str
    city_code: int


@dataclass
class Playlist:
    id: int
    name: str
    description: str | None
    cover_url: str
    track_count: int
    play_count: int
    creator: PlaylistCreator | None
    track_ids: list[int]
    tracks: list[SongInfo]


@dataclass
class Artist(ArtistShort):
    picture_url: str


@dataclass
class Album(AlbumShort):
    alias: list[str] | None
    description: str | None
    artists: list[ArtistShort]
    songs: list[SongInfo]


@dataclass
class UserShort:
    nickname: str
    avatar_url: str


class QrcodeStatus(IntEnum):
    # 等待扫码
    WAITING = 801
    # 授权中
    AUTHORIZING = 802
    # 授权成功
    AUTHORIZED = 803
    # 需要验证码
    NEED_CAPTCHA = 8821
