"""
Utils for MadMeme
"""

from urllib.request import Request, urlopen

import cv2
import numpy as np


def url_to_image(url: str, readFlag: int = cv2.IMREAD_COLOR) -> np.ndarray:
    """Get image data via url, convert to cv2 and switch to RBG format"""
    req = Request(
        url=url, headers={"User-Agent": "Mozilla/6.0"}
    )  # trick: https://stackoverflow.com/questions/16627227/problem-http-error-403-in-python-3-web-scraping
    resp = urlopen(req).read()
    img = np.asarray(bytearray(resp), dtype="uint8")
    img = cv2.imdecode(img, readFlag)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    return img


if __name__ == "__main__":
    # test utils
    url = "https://api.memegen.link/images/buzz/memes/memes_everywhere.png"
    img = url_to_image(url, readFlag=cv2.IMREAD_COLOR)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    cv2.imshow("test image", img)
    cv2.waitKey(2000)
    print("\nutils.py ran successfully.\n")
