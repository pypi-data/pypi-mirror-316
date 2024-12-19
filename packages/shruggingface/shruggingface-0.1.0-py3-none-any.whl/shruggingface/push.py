import click
import os

try:
    import internetarchive
    import internetarchive.exceptions
    import internetarchive.config
except ImportError:
    pass


def metadata(item_name):
    """
    Prepare metadata for the Internet Archive item.
    """
    metadata = {
        'title': item_name,
        'mediatype': 'data',
        'subject': 'machine learning, shruggingface',
        'tags': 'shruggingface',
        'description': 'Machine learning model archived by shruggingface',
        'creator': 'shruggingface',
    }
    return metadata


def upload(tgz_file, item_name, metadata):
    """
    Upload the file to the Internet Archive.
    """
    remote_filename = os.path.basename(tgz_file)
    files = {remote_filename: tgz_file}

    response_generator = internetarchive.upload(
        "shruggingface-" + item_name,
        files=files,
        metadata=metadata
    )

    success = True
    for response in response_generator:
        if response.status_code != 200:
            success = False
            click.echo(f"Failed to upload {response.url}: {response.text}", err=True)

    if success:
        url = f'https://archive.org/details/{item_name}'
        return url
    else:
        raise Exception("Upload failed.")


def check_login():
    """
    Set up the Internet Archive session.
    """

    session = internetarchive.get_session()

    # Check if the session is authenticated
    try:
        session.s3_is_overloaded()
        return
    except internetarchive.exceptions.AuthenticationError:
        # The user is not authenticated
        pass

    # Provide instructions and save the config
    click.echo("You need to authenticate with the Internet Archive.")
    click.echo("If you trust me, enter your keys from https://archive.org/account/s3.php")
    click.echo("Otherwise, press Ctrl+C and run `ia configure`.")
    access_key = click.prompt("Enter access key")
    secret_key = click.prompt("Enter secret key", hide_input=True)

    # Create and save the config
    config = internetarchive.config.get_config()
    config['s3'] = {
        'access': access_key,
        'secret': secret_key
    }
    internetarchive.config.write_config_file(config)

    click.echo("Configuration saved. Trying again...")

    # Create a new session with the updated config
    session = internetarchive.get_session()
    session.s3_is_overloaded() # test that it works

    return
