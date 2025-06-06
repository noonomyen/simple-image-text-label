from enum import Enum
from typing import NamedTuple, TypedDict, Optional

class ImageStatus(Enum):
    QUEUE = 0
    PASS = 1
    DROP = 2
    FIX = 3

class Item(NamedTuple):
    id: int
    text: Optional[str]
    images: list[tuple[str, bytes]]
    file: str
    size: str
    status: ImageStatus

class Stats(TypedDict):
    number: int
    queue: int
    pass_: int
    drop: int
    fix: int

class SITLHandler:
    name: str

    def __init__(self): ...
    def __len__(self) -> int: ...

    def next_queue(self) -> Optional[int]: ...
    def get(self, id: int) -> Optional[Item]: ...
    def set(self, id: int, text: str, status: ImageStatus) -> bool: ...
    def stats(self) -> Stats: ...
    def save(self) -> bool: ...
