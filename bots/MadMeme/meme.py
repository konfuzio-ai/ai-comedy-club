"""
API integration of Memegen (https://memegen.link/)
"""

import random
from pathlib import Path
from typing import Tuple

import requests


class MemeAPI:
    """Meme API interaction"""

    def __init__(self) -> None:
        self.headers = {"Accept": "application/json"}
        self.memes = self.get_memes()

    def get_memes(self) -> list:
        """Get all meme templates from API (https://api.memegen.link)"""
        # get memes
        memes = requests.get(
            "https://api.memegen.link/templates/", headers=self.headers
        ).json()
        # remove gif memes
        for m in memes:
            url = m["example"]["url"]
            if Path(url).suffix == ".gif":
                memes.remove(m)
        return memes

    def get_random(self) -> Tuple[str, str]:
        """Select random meme and extract name, url."""
        id = random.randint(0, len(self.memes))
        try:
            name = self.memes[id]["name"]
        except:
            # few memes without name
            name = None
        try:
            url = self.memes[id]["example"]["url"]
        except:
            # very few memes without url, so replace with default
            name = "Memes everywhere!"
            url = "https://api.memegen.link/images/buzz/memes/memes_everywhere.png"
        return name, url


if __name__ == "__main__":

    meme_api = MemeAPI()
    name, url = meme_api.get_random()
    print(f"\nMeme name: {name}\nMeme url: {url}\n")
    print("Meme API (meme.py) ran successfully\n")
