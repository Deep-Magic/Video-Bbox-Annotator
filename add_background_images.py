import argparse
import csv
import os
import glob

ap = argparse.ArgumentParser()
ap.add_argument('-c', '--csv_file', help="CSV file to add background images to", required=True)
ap.add_argument('-b', '--bg_dir', help="Directory with the background images", required=True)
args = ap.parse_args()

if __name__=='__main__':
	
	with open(args.csv_file, 'a') as f:
	
		writer = csv.writer(f, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
		bg_imgs = glob.glob(os.path.join(os.path.abspath(args.bg_dir), '*'))
		
		for img in bg_imgs:
			writer.writerow([img,'','','','',''])
