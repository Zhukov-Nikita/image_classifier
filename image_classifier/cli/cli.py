import click

from image_classifier.main_logic.api.api import API
from image_classifier.main_logic.local_files.local_files import LocalFiles


@click.group()
def cli():
    pass


@cli.command()
@click.argument('path', type=str)
@click.option('-c', '--color', is_flag=True)
def image(path, color):
    api = API()
    text = api.categorize_image(path, color)
    click.echo(text)


@cli.command()
@click.argument('src', type=click.Path(exists=True, dir_okay=True, file_okay=False))
@click.option('-d', '--dst', default='')
@click.option('-c', '--color', is_flag=True)
def folder(src, dst, color):
    lf = LocalFiles(src, dst, color)
    lf.move_files()


@cli.command()
def usage():
    api = API()
    text = api.usage()
    click.echo(text)


if __name__ == '__main__':
    cli()
