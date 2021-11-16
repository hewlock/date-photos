import click
import os
import re
import src.constants as c
import sys

@click.command()
@click.argument('source')
@click.argument('destination')
@click.option('--verbose/--quiet', '-v/-q', default=False)
@click.option('--dry-run/--execute', '-d/-e', default=False)
def main(source, destination, verbose, dry_run):
    """Add date EXIF metadata to images based on directory path.

SOURCE file paths must start with YYYY-MM-DD. YYYY MM and DD can be any
combination of directory or filename characters. For example,
"2020/01-01/photo.jpg" or "2020-01-01 photo.jpg" are fine.

Affected images will be moved to DESTINATION/YYYY and will be renamed to include
the YYYY-MM-DD date in the filename."""
    print(f"src: {source}")
    print(f"dst: {destination}")
    print(f"v: {verbose}")
    print(f"d: {dry_run}")


def old():
    if len(sys.argv) < 2:
        sys.exit("missing path argument")

    root_path = sys.argv[1]

    if not os.path.exists(root_path):
        sys.exit("path does not exist: " + root_path)

    regex = re.compile(r'[0-9]{4}-[0-9]{2}-[0-9]{2}')
    prefix_length = len(root_path) if root_path.endswith("/") else len(root_path) + 1

    def handle(path):
        match = regex.match(path[prefix_length:].replace("/", "-"))
        if match:
            print(f"{path} {match.group()}")
        else:
            print(f"{c.color.ERROR}Error!{c.color.CLEAR} {path}")

    for root, dirs, files in os.walk(root_path):
        for file in files:
            handle(os.path.join(root, file))
