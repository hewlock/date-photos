import click
import os
import re
import sys

from datetime import datetime
from exif import Image, DATETIME_STR_FORMAT

def find_files(params):
    results = []
    for root, dirs, files in os.walk(params['source']):
        for file in files:
            results.append({
                'file_path': os.path.join(root, file),
                'file_name': file,
                'file_ext': file[file.rfind('.'):],
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
            date = match.group()
            result['date'] = date
            result['year'] = date[0:4]
            result['month'] = date[5:7]
            result['day'] = date[8:10]
        else:
            result['valid'] = False
            result['reason'] = 'Invalid Date'

def to_exif_date(result):
    year = int(result['year'])
    month = int(result['month'])
    day = int(result['day'])
    exif_date = datetime(year=year, month=month, day=day, hour=12, minute=0, second=0)
    return exif_date.strftime(DATETIME_STR_FORMAT)

def set_exif_date(params, results):
    dst = params['destination']
    if not dst.endswith('/'):
        dst = f'{dst}/'

    count = 0;
    for result in results:
        if not result['valid']:
            continue

        with open(result['file_path'], 'rb') as image_file:
            image = Image(image_file)

        if not image.has_exif:
            result['valid'] = False
            result['reason'] = 'Invalid Photo'
            continue

        count += 1
        exif_date = to_exif_date(result)
        image.datetime_original = exif_date
        image.datetime = exif_date

        dir = f"{dst}{result['year']}/{result['month']}/{result['day']}"
        name = f"{result['date']}-photo-{count}{result['file_ext']}"
        full = f"{dir}/{name}"
        result['output_path'] = full

        if params['dry_run']:
            continue

        try:
            os.makedirs(dir, exist_ok=True)
            with open(full, 'wb') as image_file:
                image_file.write(image.get_file())
        except Exception as e:
            result['valid'] = False
            result['reason'] = e

def print_results(params, results):
    errors = [r for r in results if not r['valid']]
    success = [r for r in results if r['valid']]
    error_count = len(errors)
    success_count = len(results) - error_count

    if params['verbose']:
        if len(success) > 0:
            print('\nSuccess:')
            for s in success:
                print(f"  {s['file_path']} -> {s['output_path']} ({s['date']})")
        if len(errors) > 0:
            print('\nErrors:')
            for e in errors:
                print(f"  {e['file_path']}: {e['reason']}")

    print('\nComplete!')
    print(f'  {len(success)} success')
    print(f'  {len(errors)} errors\n')


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
