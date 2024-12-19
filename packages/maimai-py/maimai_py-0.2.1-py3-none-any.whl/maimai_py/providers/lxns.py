import json
from typing import TYPE_CHECKING

from httpx import AsyncClient, Response
from maimai_py.enums import FCType, FSType, LevelIndex, RateType, SongType
from maimai_py.exceptions import InvalidDeveloperTokenError, InvalidPlayerIdentifierError, PrivacyLimitationError
from maimai_py.providers.base import IAliasProvider, IPlayerProvider, IScoreProvider, ISongProvider
from maimai_py.models import (
    LXNSPlayer,
    Player,
    PlayerFrame,
    PlayerIcon,
    PlayerIdentifier,
    PlayerNamePlate,
    PlayerTrophy,
    Score,
    Song,
    SongAlias,
    SongDifficulties,
    SongDifficulty,
    SongDifficultyUtage,
)

if TYPE_CHECKING:
    from maimai_py.maimai import MaimaiClient


class LXNSProvider(ISongProvider, IPlayerProvider, IScoreProvider, IAliasProvider):
    """The provider that fetches data from the LXNS.

    LXNS: https://maimai.lxns.net/
    """

    developer_token: str | None
    """The developer token used to access the LXNS API."""
    base_url = "https://maimai.lxns.net/"
    """The base URL for the LXNS API."""

    @property
    def headers(self):
        """@private"""
        if not self.developer_token:
            raise InvalidDeveloperTokenError()
        return {"Authorization": self.developer_token}

    def __init__(self, developer_token: str | None = None):
        """Initializes the LXNSProvider.

        Args:
            developer_token: The developer token used to access the LXNS API.
        """
        self.developer_token = developer_token

    def _deser_score(score: dict) -> Score:
        return Score(
            id=score["id"],
            song_name=score["song_name"],
            level=score["level"],
            level_index=LevelIndex(score["level_index"]),
            achievements=score["achievements"] if "achievements" in score else None,
            fc=FCType[score["fc"].upper()] if score["fc"] else None,
            fs=FSType[score["fs"].upper()] if score["fs"] else None,
            dx_score=score["dx_score"] if "dx_score" in score else None,
            dx_rating=score["dx_rating"] if "dx_rating" in score else None,
            rate=RateType[score["rate"].upper()],
            type=SongType[score["type"].upper()],
        )

    def _ser_score(score: Score) -> dict:
        return {
            "id": score.id,
            "song_name": score.song_name,
            "level": score.level,
            "level_index": score.level_index.value,
            "achievements": score.achievements,
            "fc": score.fc.name.lower() if score.fc else None,
            "fs": score.fs.name.lower() if score.fs else None,
            "dx_score": score.dx_score,
            "dx_rating": score.dx_rating,
            "rate": score.rate.name.lower(),
            "type": score.type.name.lower(),
        }

    def _check_response_player(self, resp: Response) -> None:
        resp_json = resp.json()
        if not resp_json["success"]:
            if resp_json["code"] in [400, 404]:
                raise InvalidPlayerIdentifierError(resp_json["message"])
            elif resp_json["code"] in [403]:
                raise PrivacyLimitationError(resp_json["message"])
            elif resp_json["code"] in [401]:
                raise InvalidDeveloperTokenError(resp_json["message"])
        return resp_json

    async def get_songs(self, client: AsyncClient) -> list[Song]:
        resp = await client.get(self.base_url + "api/v0/maimai/song/list")
        resp.raise_for_status()
        resp_json = resp.json()
        return [
            Song(
                id=song["id"],
                title=song["title"],
                artist=song["artist"],
                genre=song["genre"],
                bpm=song["bpm"],
                aliases=None,
                map=song["map"] if "map" in song else None,
                version=song["version"],
                rights=song["rights"] if "rights" in song else None,
                disabled=song["disabled"] if "disabled" in song else False,
                difficulties=SongDifficulties(
                    standard=[
                        SongDifficulty(
                            type=SongType[difficulty["type"].upper()],
                            difficulty=LevelIndex(difficulty["difficulty"]),
                            level=difficulty["level"],
                            level_value=difficulty["level_value"],
                            note_designer=difficulty["note_designer"],
                            version=difficulty["version"],
                            tap_num=difficulty["notes"]["tap"] if "notes" in difficulty else 0,
                            hold_num=difficulty["notes"]["hold"] if "notes" in difficulty else 0,
                            slide_num=difficulty["notes"]["slide"] if "notes" in difficulty else 0,
                            touch_num=difficulty["notes"]["touch"] if "notes" in difficulty else 0,
                            break_num=difficulty["notes"]["break"] if "notes" in difficulty else 0,
                        )
                        for difficulty in song["difficulties"]["standard"]
                    ],
                    dx=[
                        SongDifficulty(
                            type=SongType[difficulty["type"].upper()],
                            difficulty=LevelIndex(difficulty["difficulty"]),
                            level=difficulty["level"],
                            level_value=difficulty["level_value"],
                            note_designer=difficulty["note_designer"],
                            version=difficulty["version"],
                            tap_num=difficulty["notes"]["tap"] if "notes" in difficulty else 0,
                            hold_num=difficulty["notes"]["hold"] if "notes" in difficulty else 0,
                            slide_num=difficulty["notes"]["slide"] if "notes" in difficulty else 0,
                            touch_num=difficulty["notes"]["touch"] if "notes" in difficulty else 0,
                            break_num=difficulty["notes"]["break"] if "notes" in difficulty else 0,
                        )
                        for difficulty in song["difficulties"]["dx"]
                    ],
                    utage=(
                        [
                            SongDifficultyUtage(
                                kanji=difficulty["kanji"],
                                description=difficulty["description"],
                                is_buddy=difficulty["is_buddy"],
                                tap_num=difficulty["notes"]["tap"] if "notes" in difficulty and "tap" in difficulty["notes"] else 0,
                                hold_num=difficulty["notes"]["hold"] if "notes" in difficulty and "hold" in difficulty["notes"] else 0,
                                slide_num=difficulty["notes"]["slide"] if "notes" in difficulty and "slide" in difficulty["notes"] else 0,
                                touch_num=difficulty["notes"]["touch"] if "notes" in difficulty and "touch" in difficulty["notes"] else 0,
                                break_num=difficulty["notes"]["break"] if "notes" in difficulty and "break" in difficulty["notes"] else 0,
                            )
                            for difficulty in song["difficulties"]["utage"]
                        ]
                        if "utage" in song["difficulties"]
                        else []
                    ),
                ),
            )
            for song in resp_json["songs"]
        ]

    async def get_player(self, identifier: PlayerIdentifier, client: AsyncClient) -> Player:
        resp = await client.get(self.base_url + f"api/v0/maimai/player/{identifier.as_lxns()}", headers=self.headers)
        self._check_response_player(resp)
        resp_json = resp.json()["data"]
        return LXNSPlayer(
            name=resp_json["name"],
            rating=resp_json["rating"],
            friend_code=resp_json["friend_code"],
            trophy=PlayerTrophy(id=resp_json["trophy"]["id"], name=resp_json["trophy"]["name"], color=resp_json["trophy"]["color"]),
            course_rank=resp_json["course_rank"],
            class_rank=resp_json["class_rank"],
            star=resp_json["star"],
            icon=(
                PlayerIcon(id=resp_json["icon"]["id"], name=resp_json["icon"]["name"], genre=resp_json["icon"]["genre"])
                if "icon" in resp_json
                else None
            ),
            name_plate=PlayerNamePlate(id=resp_json["name_plate"]["id"], name=resp_json["name_plate"]["name"]) if "name_plate" in resp_json else None,
            frame=PlayerFrame(id=resp_json["frame"]["id"], name=resp_json["frame"]["name"]) if "frame" in resp_json else None,
            upload_time=resp_json["upload_time"],
        )

    async def get_scores_best(self, identifier: PlayerIdentifier, client: AsyncClient) -> tuple[list[Score], list[Score]]:
        await identifier.ensure_friend_code(client, self)
        entrypoint = f"api/v0/maimai/player/{identifier.friend_code}/bests"
        resp = await client.get(self.base_url + entrypoint, headers=self.headers)
        self._check_response_player(resp)
        return (
            [LXNSProvider._deser_score(score) for score in resp.json()["data"]["standard"]],
            [LXNSProvider._deser_score(score) for score in resp.json()["data"]["dx"]],
        )

    async def get_scores_all(self, identifier: PlayerIdentifier, client: AsyncClient) -> list[Score]:
        await identifier.ensure_friend_code(client, self)
        entrypoint = f"api/v0/maimai/player/{identifier.friend_code}/scores"
        resp = await client.get(self.base_url + entrypoint, headers=self.headers)
        self._check_response_player(resp)
        return [LXNSProvider._deser_score(score) for score in resp.json()["data"]]

    async def update_scores(self, identifier: PlayerIdentifier, scores: list[Score], client: AsyncClient) -> None:
        await identifier.ensure_friend_code(client, self)
        entrypoint = f"api/v0/maimai/player/{identifier.friend_code}/scores"
        scores_dict = {"scores": [LXNSProvider._ser_score(score) for score in scores]}
        resp = await client.post(self.base_url + entrypoint, headers=self.headers, json=scores_dict)
        if not resp.json()["success"] and resp.json()["code"] == 400:
            raise ValueError(resp.json()["message"])
        self._check_response_player(resp)

    async def get_aliases(self, client: AsyncClient) -> list[SongAlias]:
        resp = await client.get(self.base_url + "api/v0/maimai/alias/list")
        resp.raise_for_status()
        return [SongAlias(song_id=item["song_id"], aliases=item["aliases"]) for item in resp.json()["aliases"]]
