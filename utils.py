import base64
from io import BytesIO

def check_size(width: int, height: int, max_width: int, max_height: int) -> bool:
    """
    Check if width and height are in the correct range.
    In place to avoid abuses by forged POST requests.
    """
    if width <= 0 or width > max_width or height <= 0 or height > max_height:
        return False
    return True

def wc_to_b64(wc: "WordCloud") -> str:
    """
    Convert a WordCloud object to a base64 string
    """
    wc_img=wc.to_image()
    buff=BytesIO ()
    wc_img.save (buff, format="PNG")
    img_b64=base64.b64encode (buff.getvalue()).decode("utf-8")
    return img_b64