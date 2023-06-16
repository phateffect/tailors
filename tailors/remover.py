import rembg

from PIL import Image


def remove_background(fp, bgcolor=None):
    img = Image.open(fp)
    session = rembg.new_session("isnet-general-use")
    return rembg.remove(img, session=session, bgcolor=bgcolor)
