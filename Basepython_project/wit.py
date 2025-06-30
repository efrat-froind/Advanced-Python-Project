import os
import click
import Repository as re

@click.group()
def wit():
    """CLI for version control similar to git."""
    pass

@wit.command()
@click.option('--path', default=os.getcwd(), help="The path of the project directory.")
def init(path):
    """Initialize a new version control repository."""
    # print(f"Initializing repository in: {path}")
    re.init(path, "")

@wit.command()
@click.argument('files', nargs=-1)
@click.option('--path', default=os.getcwd(), help="The path of the project directory.")
def add(path, files):
    """Add files to the staging area."""
    re.add(path, list(files))

@wit.command()
@click.option('-m', '--message', required=True, help="The commit message.")
@click.option('--path', default=os.getcwd(), help="The path of the project directory.")
def commit(path, message):
    """Commit changes to the repository."""
    re.commit(path, "", message)
    print("The version was executed successfully")


@wit.command()
@click.option('--path', default=os.getcwd(), help="The path of the project directory.")
def log(path):
    """Show the commit log."""
    re.log(path)

@wit.command()
@click.argument('commit_id')
@click.option('--path', default=os.getcwd(), help="The path of the project directory.")
def checkout(path, commit_id):
    """Checkout a specific commit."""
    re.checkout(path, commit_id)

@wit.command()
@click.option('--path', default=os.getcwd(), help="The path of the project directory.")
def status(path):
    """Show the repository status."""
    re.status(path)


@wit.command()
@click.option('--path', default=os.getcwd(), help="The path of the project directory.")
@click.option('--server', default="http://127.0.0.1:8000", help="The URL of the FastAPI server.")
def push(path, server):
    """Push files to server and get alerts and analysis."""
    re.push(path, server)

if __name__ == "__main__":
    wit()









