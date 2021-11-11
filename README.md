# date-photos

Fix scanned photo metadata.

## Motivation

I have been scanning a large number of old family photos to add to my digital collection. The problem is they are all assigned dates based on when I scanned them. I have organized them into a directory structure based on the dates they were taken. This app will use the directory structure to assign the correct metadata dates to each photo. This will allow me to import the photos to a photo app and have them show up correctly in a timeline.

## Implementation

Add date metadata to scanned photos based on directory path. I plan to support `YYYY-MM-DD` where either `-` or a new directory (mix and match allowed).

For example, these photos would all receive metadata dates for 2020/10/31:

    my-scanned-photos/
      2020/
        10/
          31/
            photo1.jpg
        10-31/
          photo2.jpg
      2020-10/
        31/
          photo3.jpg
      2020-10-31/
        photo4.jpg
        photo5.jpg
