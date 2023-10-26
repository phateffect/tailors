from io import BytesIO
from zipfile import ZipFile, ZIP_BZIP2


class Comporess:
    def __init__(self):
        self.size_limit = 3_000_000
        self.files = {}

    def save(self, outfile):
        with ZipFile(outfile, "w", ZIP_BZIP2) as myzip:
            for filename, data in sorted(self.files.items()):
                myzip.writestr(filename, data)

    def add(self, basename, img, quality=100):
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
            return self.add(basename, img, quality - 5)
