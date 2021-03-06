import argparse
import datetime
from PIL import Image
from PIL.ExifTags import TAGS
import os
import shutil
import sys

PIC_SUFFIXES = (".jpg", "jpeg", ".png", ".gif", ".tif", ".tiff")
VID_SUFFIXES = (".mkv", ".mov", ".mp4")  # may add more later
DATE_TAKEN_KEY = 0x9003

def img_documenter(origin_direc, dest_direc, initials, verboseprint, fileop,
        vid):
    if not os.path.exists(path=origin_direc):
        print("The given origin path does not exist")
        print("Please provide a proper path next time")
        sys.exit()
    elif not os.path.exists(path=dest_direc):
        print("The given destination path does not exist")
        print("Please provide a proper path next time")
        sys.exit()
    origin_list = os.listdir(origin_direc)
    move_count = 0
    miss_count = 0

    # generators!
    if vid:
        suffixes = PIC_SUFFIXES +  VID_SUFFIXES
    else:
        suffixes = PIC_SUFFIXES
    gen = (file for file in origin_list if file.lower().endswith(suffixes))
    for file in gen:
        filetype_loc = file.find(".")
        filetype = file[filetype_loc:].lower() # index indo the last part to get filetype
        pre_file_name = file
        if filetype in PIC_SUFFIXES:  # this would break for a video
            img = Image.open(os.path.join(origin_direc, pre_file_name))
            if not hasattr(img, '_getexif'):
                img.close()
                verboseprint("{} does not have exif data so it was not dealt with"
                    .format(pre_file_name))
                verboseprint()
                miss_count += 1
                continue
            exif = img._getexif()
            img.close()
        # decode exif using TAGS
        if filetype in VID_SUFFIXES or DATE_TAKEN_KEY not in exif:
            # this takes care of weird jpg files without date taken stamp
            unix_time = os.path.getmtime(os.path.join(origin_direc, pre_file_name))
            full_date = datetime.datetime.fromtimestamp(
                unix_time
                ).strftime('%Y:%m:%d %H:%M:%S').split(sep=" ")
            verboseprint("{} did not have date taken EXIF data".format(pre_file_name))
            verboseprint("Date modified from file metadata will be used")
        else:
            full_date = exif[DATE_TAKEN_KEY].split(sep=" ")
        date = full_date[0]
        time = full_date[1]
        date = date.replace(":", "")
        time = time.replace(":", "")
        if not initials: # check if none given
            new_file_name = date + "-" + time + filetype
        else:
            new_file_name = date + "-" + time + "-" + initials + filetype

        # get vars once outside the if
        old_full_file = os.path.join(origin_direc, pre_file_name)
        new_full_file = os.path.join(dest_direc, new_file_name)
        # without the if statement below.. almost had a silent bug
        if (not os.path.isfile(os.path.join(origin_direc ,new_file_name)) and
            not os.path.isfile(new_full_file)):
            fileop(old_full_file, new_full_file)
            verboseprint("{} renamed to {}".format(pre_file_name, new_file_name))
            verboseprint("Moved from {} to {}".format(origin_direc, dest_direc))
        elif new_file_name == pre_file_name:
            verboseprint(pre_file_name + " already has the right name!")
            fileop(old_full_file, new_full_file)
            verboseprint("Moved from {} to {}".format(origin_direc, dest_direc))
        else:
            filetype_loc = new_file_name.find(".")
            new_file_name = new_file_name[:filetype_loc] + "-1" + \
                            new_file_name[filetype_loc:]
            # next line is repeated to get the new full file path
            new_full_file = os.path.join(dest_direc, new_file_name)
            fileop(old_full_file, new_full_file)
            verboseprint("Oh, there already exists a file with predicted name..")
            verboseprint("{} renamed to {}".format(pre_file_name, new_file_name))
            verboseprint("Moved from {} to {}".format(origin_direc, dest_direc))
        verboseprint() # extra newline
        move_count += 1

    verboseprint("All done!")
    verboseprint("{} file(s) were moved".format(move_count))
    verboseprint("{} file(s) were missed because of lack of EXIF data"
        .format(miss_count))

def are_you_sure():
    print("Please press 0 if this is okay and 1 is not")
    choice = input("Select your item: ")
    choice = choice.strip()
    if choice == "1":
        print("Please re-use the program")
        sys.exit()
    elif choice != "0":
        print("Uh oh, that was not one of the options")
        sys.exit()
    print()
    print()

def main():
    parser = argparse.ArgumentParser(description=
"""This is a helpful tool for one to be able to batch rename and move photo files.
It will either rename or copy the files based on whether ot not "-c" is used.
Files are renamed to the general format of
    YYYYMMDD-HHMMSS[-initials].filename -- note initials are optional.
Please see below for the different arguments that can be provided.""")
    parser.add_argument("-v", "--verbose", help="increase output verbosity",
                    action="store_true")
    parser.add_argument("-i", "--initials", default="",
                    help="initials to append to the filename")
    parser.add_argument("-c", "--copy", action="store_true",
                    help=
"""if enabled, instead of renaming the files it will make a copy with
 the correct name""")
    parser.add_argument("-vid", "--videos", action="store_true",
                    help=
"""if enabled, videos will also be renamed based on metadata
 information available in the file""")
    parser.add_argument("filenames", nargs='*',
                    help=
"""please provide a path to read the images from
 and a path to output the files to
 Unless, you would like to read and write to the current dir""")
    args = parser.parse_args()
    # below is lambda to print out stuff if verbose is enabled
    verboseprint = print if args.verbose else lambda *a, **k: None
    fileop = shutil.copy2 if args.copy else shutil.move
    if len(args.initials) > 0:
        initials = args.initials
    else:
        print("Are you sure that you do not want to append initials to the files?")
        are_you_sure()
        initials = ""
    if len(args.filenames) > 2:
        print("Please provide only two directories...")
    elif (len(args.filenames) == 2):
        origin_direc = args.filenames[0]
        dest_direc = args.filenames[1]
    elif (len(args.filenames) == 1):
        print("If the directory provided is the origin please type 0")
        print("If the directory provided is the destination please type 1")
        choice = input("Select your item: ")
        choice = choice.strip()
        if choice == "0":
            origin_direc = args.filenames[0]
            print("The destination directory has defaulted to the current directory")
            are_you_sure()
            dest_direc = "."
        elif choice == "1":
            dest_direc = args.filenames[0]
            print("The origin directory has defaulted to the current directory")
            are_you_sure()
            origin_direc = "."
        else:
            print("Uh oh, that was not one of the options")
            sys.exit()
    else:
        print("You did not provide any directories")
        print("We will default to using current directory for both the ")
        print("origin and destination directory")
        are_you_sure()
        origin_direc = "."
        dest_direc = "."

    img_documenter(origin_direc, dest_direc, initials, verboseprint, fileop,
        args.videos)

if __name__ == '__main__':
    main()