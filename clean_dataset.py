import glob
import os
import csv

if __name__=='__main__':
    dirs = []
    img_paths = []
    ann_paths = []

    with open('annotations.csv', 'r') as f:
        reader = csv.reader(f)
        for line in reader:
            if os.path.dirname(line[0]) not in dirs:
                dirs.append(os.path.dirname(line[0]))
                img_paths.extend(glob.glob(os.path.abspath(os.path.join(os.path.dirname(line[0]), '*'))))
            if (line[0] not in ann_paths):
                ann_paths.append(line[0])
       
        print ('Number of image files in dataset: ', len(img_paths))
        print ('Number of annotations in dataset:', len(ann_paths))
        
        for ann in ann_paths:
            del img_paths[img_paths.index(ann)]
        
        for img in img_paths:
            os.remove(img)
            print ("Removing: ", img)

        print ('Number of image files in dataset: ', len(img_paths))
        print ('Number of annotations in dataset:', len(ann_paths))

        for ann in ann_paths:
            del img_paths[img_paths.index(ann)]

        for img in img_paths:
            os.remove(img)
            print ("Removing: ", img)
