import click
from tqdm import tqdm
from pathlib import Path
from PIL import Image

from tailors.compressor import Comporess as ComporessManager


@click.command()
@click.argument("images-dir")
@click.argument("zip-filename")
def cli(images_dir, zip_filename):
    images = list(Path(images_dir).glob("*.jpg"))

    compress_manager = ComporessManager()

    for img_file in tqdm(images):
        basename = img_file.name[:-len(img_file.suffix)]
        compress_manager.add(basename, Image.open(img_file))

    compress_manager.save(zip_filename)


if __name__ == "__main__":
    cli()
