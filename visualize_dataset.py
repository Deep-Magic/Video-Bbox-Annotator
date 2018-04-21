import cv2
import csv

with open('annotations.csv', 'r') as f:
    reader = csv.reader(f)
    for line in reader:
        bbox = [int(x) for x in line[1:-1]]
        caption = line[-1]
        img = cv2.imread(line[0])
        cv2.rectangle(img, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (255,0,0), 2, cv2.LINE_AA)
        dy = 30
        x1, y1, x2, y2 = bbox
        size, base = cv2.getTextSize(caption, cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, 1)
        cv2.rectangle(img, (x1+20, y1+20-size[1]+dy), (x1+20+size[0], y1+20+base+dy), 0, -1)
        cv2.putText(img,caption, (x1+20,y1+20+dy), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255,255,255))
        img = cv2.resize(img, (0,0), fx=0.5, fy=0.5) 
        cv2.imshow('Rectangle-BBox', img)
        cv2.waitKey(1) 
