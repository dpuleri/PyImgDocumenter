PyImgDocumenter
================

usage: ImageDocumenter.py [-h] [-v] [-i INITIALS] [-c] [-vid] [filenames [filenames ...]]

This is a helpful tool for one to be able to batch rename and move photo
files. It will either rename or copy the files based on whether ot not "-c" is used. Files are renamed to the general format of YYYYMMDD-
HHMMSS[-initials].filename -- note initials are optional. Please see below for the different arguments that can be provided.

- positional arguments:
  + filenames             please provide a path to read the images from and a
  + path to output the files to Unless, you would like to read and write to the current dir

- optional arguments:
  + h, --help            show this help message and exit
  + v, --verbose         increase output verbosity
  + i INITIALS, --initials INITIALS initials to append to the filename
  + c, --copy            if enabled, instead of renaming the files it will make a copy with the correct name
  + vid, --videos        if enabled, videos will also be renamed based on metadata information available in the file


good usage would be:

```
python ImageDocumenter.py -i "initials" "path to source" "path to destination"
```