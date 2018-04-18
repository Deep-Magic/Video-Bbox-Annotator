import csv
import argparse
import os
from tempfile import NamedTemporaryFile
import shutil
import csv

if __name__=='__main__':
    
    ap = argparse.ArgumentParser()
    ap.add_argument('-a', '--annotation_csv', required=True, help='Path to annotation file')
    args = ap.parse_args()
    
    tempfile = NamedTemporaryFile(delete=False)

    with open(args.annotation_csv, 'rb') as csvFile, tempfile:
        reader = csv.reader(csvFile)
        writer = csv.writer(tempfile)

        for line in reader:
            new_csv = line
            splits = line[0].split('/')
            new_csv[0] = os.path.join(os.path.abspath('.'), splits[-2]+'/'+splits[-1])
            writer.writerow(new_csv)
            
    shutil.move(tempfile.name, args.annotation_csv)
