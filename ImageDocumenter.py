from PIL import Image
from PIL.ExifTags import TAGS
import os

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