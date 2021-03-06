# date-photos

## Motivation

I have been scanning a large number of old family photos to add to my digital collection. The problem is they are all assigned dates based on when I scanned them. I have organized them into a directory structure based on the dates they were taken. This app will use the directory structure to assign the correct metadata dates to each photo. This will allow me to import the photos to a photo app and have them show up correctly in a timeline.

## Note about existing exif data

I scanned all photos on a Mac and used Quick Look (space bar in finder) with
command+L and command+R to rotate some photos. Something about this clashed with
the exif python library corrupting those images after conversion. I had to run
the following command to strip existing exif data and then rotate them again
after dates were assigned. Definitely not ideal.

```
find . -name '*.jpg' -print0 | xargs -0 mogrify -strip
```

## Implementation

```
Usage: date-photos [OPTIONS] SOURCE DESTINATION

  Add date EXIF metadata to images based on directory path.

  SOURCE file paths must start with YYYY-MM-DD. YYYY MM and DD can be any
  combination of directory or filename characters. For example,
  "2020/01-01/photo.jpg" or "2020-01-01 photo.jpg" are fine.

  Affected images will be moved to DESTINATION/YYYY and will be renamed to
  include the YYYY-MM-DD date in the filename.

Options:
  -v, --verbose / -q, --quiet
  -d, --dry-run / -e, --execute
  --help                         Show this message and exit.
```
