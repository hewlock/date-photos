import click
import exif
import os
import re
import src.constants as c
import sys

def find_files(params):
    results = []
    for root, dirs, files in os.walk(params['source']):
        for file in files:
            results.append({
                'file_path': os.path.join(root, file),
                'file_name': file,
                'valid': True,
            })
    return results

def add_date(params, results):
    regex = re.compile(r'[0-9]{4}-[0-9]{2}-[0-9]{2}')
    source = params['source']
    prefix_length = len(source) if source.endswith('/') else len(source) + 1

    for result in results:
        date_path = result['file_path'][prefix_length:];
        match = regex.match(date_path.replace('/', '-'))
        if match:
            result['date'] = match.group()
        else:
            result['valid'] = False
            result['reason'] = 'Invalid Date'

def set_exif_date(params, results):
    for result in results:
        if not result['valid']:
            continue

        with open(result['file_path'], 'rb') as image_file:
            image = exif.Image(image_file)

        if image.has_exif:
            print('\n')
            print(result['file_path'])
            for prop in image.list_all():
                try:
                    print(f'{prop}: {image[prop]}')
                except:
                    print(f'{prop}: {c.color.ERROR}Error!{c.color.CLEAR}')
        else:
            result['valid'] = False
            result['reason'] = 'Invalid Photo'

def print_results(params, results):
    print(params)
    for result in results:
        if (result['valid']):
            print(result)
        else:
            print(f'{c.color.ERROR}{result}{c.color.CLEAR}')

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

    if not os.path.exists(source):
        sys.exit('Source does not exist: ' + source)
    if not os.path.exists(destination):
        sys.exit('Destination does not exist: ' + destination)

    params = {
        'source': source,
        'destination': destination,
        'verbose': verbose,
        'dry_run': dry_run,
    }

    results = find_files(params)
    add_date(params, results)
    set_exif_date(params, results)
    print_results(params, results)
