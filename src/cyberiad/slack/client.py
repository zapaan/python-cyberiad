from typing import Iterable, Tuple

import httpx

from .block_kit import Block, Divider, SectionBlock


def get_client(token: str):
    token = os.environ["SLACK_TOKEN"]
    return httpx.Client(
        base_url="https://slack.com/api/", headers={"Authorization": f"Bearer {token}"}
    )


def find_channel_id(channame: str, /, *, client=client) -> Tuple[str, bool]:
    res = client.get("conversations.list")
    if not res.json()["ok"]:
        print(res.json())
        return
    return next(
        (chan["id"], chan["is_member"])
        for chan in res.json()["channels"]
        if chan["name"] == channame
    )


def join_channel(chanid: str, /, *, client=client) -> None:
    r = client.post("conversations.join", data={"channel": chanid})
    if not r.json()["ok"]:
        print(r.json())


def send_message(
    chanid: str,
    /,
    blocks: Iterable[Block] = (),
    text: str = "",
    *,
    intro=True,
    client=client,
) -> None:
    if intro:
        blocks = [SectionBlock(text="Upgrade is compulsory."), Divider(), *blocks]
    r = client.post(
        "chat.postMessage",
        data={
            "channel": chanid,
            "blocks": [prep_block(b) for b in blocks],
            "text": text,
        },
    )
    if not r.json()["ok"]:
        print(r.json())
