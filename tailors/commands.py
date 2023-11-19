import click

from pathlib import Path
from PIL import Image
from .compressor import Comporess as ComporessManager


@click.group()
def cli():
    pass


@cli.command()
@click.argument("images-dir", type=click.Path(file_okay=False, exists=True))
@click.argument("zip-filename", type=click.Path(dir_okay=False, writable=True))
def reduce(images_dir, zip_filename):
    """减小图片体积"""
    images = list(Path(images_dir).glob("*.jpg"))

    compress_manager = ComporessManager()

    with click.progressbar(images) as bar:
        for img_file in bar:
            basename = img_file.name[:-len(img_file.suffix)]
            compress_manager.reduce(basename, Image.open(img_file))

    compress_manager.save(zip_filename)


@cli.command()
@click.argument("background-image", type=click.File("rb"))
@click.argument("images-dir", type=click.Path(file_okay=False, exists=True))
@click.argument("zip-filename", type=click.Path(dir_okay=False, writable=True))
def merge(background_image, images_dir, zip_filename):
    """合并前后景图片"""
    bg = Image.open(background_image)
    images = list(Path(images_dir).glob("*.jpg"))

    compress_manager = ComporessManager()

    with click.progressbar(images) as bar:
        for img_file in bar:
            basename = img_file.name[:-len(img_file.suffix)]
            compress_manager.merge(
                basename,
                bg.copy(),
                Image.open(img_file),
                (600, 600), # 宽 高
                (400, 450), # 左 上
            )

    compress_manager.save(zip_filename)


if __name__ == "__main__":
    cli()
