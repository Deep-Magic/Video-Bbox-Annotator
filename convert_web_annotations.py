import glob
import csv
import numpy as np
from PIL import Image

textdata = []
classes = dict()

with open('classes.txt', 'r') as f:
	for i, c in [x.strip().split(',') for x in f.readlines()]:
		classes[i]=c

for f in glob.glob('./*/labels.txt'):
	with open(f, 'r') as g:
		textdata.extend([(f.split('/')[-2]+'/'+x).strip().split(',') for x in g.readlines()])

for i in range(len(textdata)):
	textdata[i][1] = classes[textdata[i][1]]

with open('annotations_full.csv', 'w') as f:
	writer = csv.writer(f)
	for x in textdata:
		img = Image.open(x[0])
		w, h = img.size
		writer.writerow([x[0], int(h-float(x[3])), int(float(x[2])), int(h-float(x[5])), int(float(x[4])), x[1]])

with open('classes.csv', 'r') as f:
	with open('index.txt', 'w') as g:
                for h in f.readlines():
                        g.write(h.strip().split(',')[1]+'\n')

with open('classes.csv', 'w') as f:
	w = csv.writer(f)
	for i, (k,v) in enumerate(classes.iteritems()):
		w.writerow([v,i])
