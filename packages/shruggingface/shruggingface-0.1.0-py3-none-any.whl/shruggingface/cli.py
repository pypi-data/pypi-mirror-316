import os
import click

from . import env
from . import pack
from . import push


@click.group()
def cli():
    """
    ¯\\_(ツ)_/¯
    
    1. Create an environment and set it up:

        $(shruggingface init)

    2. Run your code to download models.

    3. Export and publish them:

        shruggingface publish

    4. Paste the code from the previous step into your program.

    5. There is no step 5.
    """
    pass

@cli.command()
def info():
    """Print some details"""

    click.echo(f"Project name: {env.name()}")

    env_exists = env.exists()
    exists = "exists" if env_exists else "missing"
    click.echo(f"HF_HOME: {env.get()} ({exists})")

    if env_exists:
        click.echo(f"Size: {pack.get_size()}")


@cli.command()
@click.argument("output_file", type=click.Path())
def save(output_file):
    """
    Export the cache directory as a tar.gz file.
    """
    
    if not env.exists():
        click.echo(f"HF_HOME isn't set up properly.", err=True)
        raise click.Abort()

    try:
        pack.pack(output_file)
    except Exception as e:
        click.echo(f"Error during export: {e}", err=True)
        raise click.Abort()

@cli.command()
@click.argument("input_file", type=click.Path())
def load(input_file):
    """
    Load the given tar.gz file into the cache.
    """
    if not env.exists():
        click.echo(f"HF_HOME isn't set up properly.", err=True)
        raise click.Abort()

    try:
        pack.unpack(input_file)
    except Exception as e:
        click.echo(f"Error during import: {e}", err=True)
        raise click.Abort()


@cli.command()
@click.option("--cache_dir", default=f"~/.cache/shruggingface/{env.name()}", type=click.Path(file_okay=False))
def init(cache_dir):
    """
    Creates the cache
    """
    cache_dir = os.path.abspath(os.path.expanduser(cache_dir))

    env.set(cache_dir)
    env.create()

    click.echo(f'export HF_HOME={cache_dir}')


@cli.command()
@click.option("--name", prompt="Project name", default=env.name())
def publish(name):
    """
    Publish the current cache to Internet Archive
    """
    if not env.exists():
        click.echo("HF_HOME isn't set up properly.", err=True)
        raise click.Abort()

    # Pack the cache directory
    tgz_file = f"{name}.tar.gz"
    try:
        pack.pack(tgz_file)
    except Exception as e:
        click.echo(f"Error during packing: {e}", err=True)
        raise click.Abort()

    # Upload to Internet Archive
    try:
        push.check_login()
        metadata = push.metadata(name)
        url = push.upload(tgz_file, name, metadata)
        click.echo(f"Upload successful! Archive URL: {url}")
    except Exception as e:
        click.echo(f"Error during upload: {e}", err=True)
        raise click.Abort()
    finally:
        os.unlink(tgz_file)

    # Provide code snippet
    click.echo("\nInclude the following code in your program to preload the models:")
    click.echo(f"import shruggingface; shruggingface.init('{name}', '{url}/{tgz_file}')")

    

if __name__ == "__main__":
    cli()

