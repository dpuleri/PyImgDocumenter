import argparse
from PIL import Image
from PIL.ExifTags import TAGS
import os
import sys

def img_documenter(origin_direc, dest_direc):
    DateTakenValue = 0x9003
    pre_file_name = "test.jpg"
    img = Image.open(pre_file_name)
    img.close()
    exif = img._getexif()
    # decode exif using TAGS
    full_date = exif[DateTakenValue].split(sep=" ")
    date = full_date[0]
    time = full_date[1]
    date = date.replace(":", "")
    time = time.replace(":", "")
    new_file_name = date + "-" + time + ".jpg"
    if not os.path.isfile(new_file_name):
        os.rename(pre_file_name, new_file_name)
    elif new_file_name == pre_file_name:
        print(pre_file_name + " already has the right name!")
    else:
        filetype_loc = new_file_name.find(".")
        new_file_name = new_file_name[:filetype_loc] + "-1" + \
                        new_file_name[filetype_loc:]
        os.rename(pre_file_name, new_file_name)

    print(date)
    print(time)

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
    parser = argparse.ArgumentParser(description="Gather input directories and"\
                                                 "initials")
    parser.add_argument("-v", "--verbose", help="increase output verbosity",
                    action="store_true")
    parser.add_argument("-i", "--initials", default="",
                    help="initials to append to the filename")
    parser.add_argument("filenames", nargs='*',
                    help=
"""please provide a directory to read the images from
 and a directory to output the files to
 Unless, you would like to read and write to the current dir""")
    args = parser.parse_args()
    verboseprint = print if args.verbose else lambda *a, **k: None
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
    print(origin_direc)
    print(dest_direc)
    print(args.verbose)
    print(initials)

if __name__ == '__main__':
    main()