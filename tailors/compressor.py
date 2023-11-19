from io import BytesIO
from zipfile import ZipFile, ZIP_BZIP2
from rembg import new_session, remove


class Comporess:
    def __init__(self):
        self.size_limit = 3_000_000
        self.files = {}
        self.session = new_session("isnet-general-use.onnx")

    def save(self, outfile):
        with ZipFile(outfile, "w", ZIP_BZIP2) as myzip:
            for filename, data in sorted(self.files.items()):
                myzip.writestr(filename, data)

    def merge(self, basename, bg, img, size, center):
        w, h = size
        x, y = center
        left = int(x - w / 2)
        upper = int(y - h / 2)

        output = bg.copy()
        item = remove(img, session=self.session, post_process_mask=True)
        fg = item.resize((w, h))
        output.paste(fg, (left, upper), fg)

        buffer = BytesIO()
        output.save(buffer, "PNG", optimize=True)

        self.files[f"{basename}.png"] = buffer.getbuffer()
        return output

    def reduce(self, basename, img, quality=100):
        buffer = BytesIO()
        img.save(
            buffer,
            "JPEG",
            quality="keep" if quality > 95 else quality,
            optimize=True
        )

        if len(buffer.getbuffer()) < self.size_limit:
            self.files[f"{basename}.jpeg"] = buffer.getbuffer()
            return buffer
        else:
            return self.reduce(basename, img, quality - 5)
