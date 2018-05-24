from PIL import Image
from PIL.ExifTags import TAGS
import glob
import argparse
import os

if __name__=='__main__':

    ap = argparse.ArgumentParser()
    ap.add_argument('-d', '--dir', required=True, help='Directory of images to strip EXIF data and save original EXIF-independent rotated image in-place in the same directory')
    args = ap.parse_args()

    for f in glob.glob(os.path.join(args.dir, '*')):
        img = Image.open(f)
        for k, v in img._getexif().items():
            if TAGS.get(k, k)=='Orientation' and v==6:
                img = img.transpose(Image.ROTATE_270)
                img.save(f)
