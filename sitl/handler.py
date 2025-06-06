from enum import Enum
from typing import NamedTuple, TypedDict, Optional

class ImageStatus(Enum):
    """
    Enum representing the status of an image.

    Attributes:
        QUEUE (int): Image is in the queue and awaiting processing.
        PASS (int): Image has passed validation or review.
        DROP (int): Image has been dropped or rejected.
        FIX (int): Image requires fixing or further action.
    """
    QUEUE = 0
    PASS = 1
    DROP = 2
    FIX = 3

class Item(NamedTuple):
    """
    Represents an item containing image and text data.

    Attributes:
        id (int): Unique identifier for the item.
        text (Optional[str]): Associated text label or description.
        images (list[tuple[str, bytes]]): List of image data as (filename, bytes) tuples.
        file (str): File path or name associated with the item.
        size (str): Size descriptor of the item or image.
        status (ImageStatus): Current status of the image.
    """
    id: int
    text: Optional[str]
    images: list[tuple[str, bytes]]
    file: str
    size: str
    status: ImageStatus

class Stats(TypedDict):
    """
    Dictionary representing statistics of image processing.

    Attributes:
        number (int): Total number of items.
        queue (int): Number of items in the queue.
        passed (int): Number of items that have passed.
        dropped (int): Number of items that have been dropped.
        fixing (int): Number of items that require fixing.
    """
    number: int
    queue: int
    passed: int
    dropped: int
    fixing: int

class SITLHandler:
    """
    Handler class for Simple Image Text Label (SITL) operations.

    Attributes:
        name (str): Name of the handler.

    Methods:
        __init__(): Initializes the handler.
        __len__() -> int: Returns the number of items managed by the handler.
        next_queue() -> Optional[int]: Returns the ID of the next item in the queue, if any.
        get(id: int) -> Optional[Item]: Retrieves an item by its ID.
        set(id: int, text: str, status: ImageStatus) -> bool: Updates the text and status of an item.
        stats() -> Stats: Returns statistics about the items.
        save() -> bool: Persists the current state of the handler.
    """

    name: str

    def __init__(self): ...
    def __len__(self) -> int: ...

    def next_queue(self) -> Optional[int]: ...
    def get(self, id: int) -> Optional[Item]: ...
    def set(self, id: int, text: str, status: ImageStatus) -> bool: ...
    def stats(self) -> Stats: ...
    def save(self) -> bool: ...
