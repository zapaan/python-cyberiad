from dataclasses import dataclass
from typing import Dict, Iterable, Tuple, Union


@dataclass(frozen=True)
class SectionBlock:
    text: str


@dataclass(frozen=True)
class ContextBlock:
    elements: Iterable[TextObj]


class Divider:
    pass


@dataclass(frozen=True)
class TextObj:
    text: str


Block = Union[SectionBlock, ContextBlock, Divider]
CompObj = TextObj


def prep_block(block: Block, /) -> Dict:
    if isinstance(block, SectionBlock):
        return {"type": "section", "text": {"type": "mrkdwn", "text": block.text}}
    elif isinstance(block, ContextBlock):
        return {"type": "context", "elements": [prep_obj(o) for o in block.elements]}
    elif isinstance(block, Divider):
        return {"type": "divider"}

    return {}


def prep_obj(obj: CompObj, /) -> Dict:
    if isinstance(obj, TextObj):
        return {"type": "mrkdwn", "text": obj.text}

    return {}
