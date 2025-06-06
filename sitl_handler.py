# This is example code for a SITL handler that reads from a CSV file.

from sitl import SITLHandler, ImageStatus, Item, Stats
from os import path
from io import BytesIO
from typing import Optional
from pandas import read_csv
from PIL import Image

class Handler(SITLHandler):
    def __init__(self):
        self.name = "Demo"
        self.dir = "./data"
        self.df = read_csv(path.join(self.dir, "labels.csv"))
        self.df.rename(columns={"filename": "file", "text": "text"}, inplace=True)

        if "status" not in self.df.columns:
            self.df["status"] = ImageStatus.QUEUE.name

    def __len__(self) -> int:
        return len(self.df)

    def next_queue(self) -> Optional[int]:
        queue_rows = self.df[self.df["status"] == ImageStatus.QUEUE.name]
        if not queue_rows.empty:
            return queue_rows.index[0]
        return None

    def get(self, id: int) -> Optional[Item]:
        if id < 0 or id >= len(self.df):
            return None

        row = self.df.iloc[id]
        processed = open(path.join(self.dir, "processed", row["file"]), "rb").read()
        processed_image = Image.open(BytesIO(processed))

        return Item(
            id = id,
            images=[
                ("Boxes", open(path.join(self.dir, "boxes", row["file"].replace(".bmp", ".jpg")), "rb").read()),
                ("Processed", processed),
                ("Binary", open(path.join(self.dir, "binary", row["file"]), "rb").read()),
                ("Heatmap", open(path.join(self.dir, "heatmap", row["file"]), "rb").read())
            ],
            size=f"{processed_image.width}x{processed_image.height}",
            file=row["file"],
            status=ImageStatus[row["status"]],
            text=row["text"]
        )

    def set(self, id: int, text: str, status: ImageStatus) -> bool:
        if id < 0 or id >= len(self.df):
            return False

        self.df.loc[id, "status"] = status.name
        self.df.loc[id, "text"] = text

        return True

    def stats(self) -> Stats:
        return Stats(
            number=len(self.df),
            queue=(self.df["status"] == ImageStatus.QUEUE.name).sum(),
            pass_=(self.df["status"] == ImageStatus.PASS.name).sum(),
            drop=(self.df["status"] == ImageStatus.DROP.name).sum(),
            fix=(self.df["status"] == ImageStatus.FIX.name).sum()
        )

    def save(self) -> bool:
        try:
            self.df.to_csv(path.join(self.dir, "labels.csv"), index=False)
            return True
        except Exception:
            return False

handler = Handler()
