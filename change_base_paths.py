import csv
import argparse
import os
from tempfile import NamedTemporaryFile
import shutil
import csv

if __name__=='__main__':
    
    ap = argparse.ArgumentParser()
    ap.add_argument('-a', '--annotation_csv', required=True, help='Path to annotation file')
    ap.add_argument('-m', '--min_area', required=True, help='Min area of bbox')
    args = ap.parse_args()
    
    tempfile = NamedTemporaryFile(delete=False)

    with open(args.annotation_csv, 'rb') as csvFile, tempfile:
        reader = csv.reader(csvFile)
        writer = csv.writer(tempfile)

        for line in reader:
            new_csv = line
            x1, y1, x2, y2 = [int(x) for x in new_csv[1:-1]]
            if abs((y2-y1)*(x2-x1))<=int(args.min_area):
                continue
            splits = line[0].split('/')
            new_csv[0] = os.path.join(os.path.abspath('.'), splits[-2]+'/'+splits[-1])
            writer.writerow(new_csv)
            
    shutil.move(tempfile.name, args.annotation_csv)
