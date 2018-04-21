from matplotlib.widgets import RectangleSelector
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import argparse
import cv2
import imutils
import os
import glob
import csv

class Video_Bbox(object):

    def __init__(self, fig, ax, args):
    
        self.RS = RectangleSelector(ax, self.line_select_callback,
                                       drawtype='box', useblit=True,
                                       button=[1, 3],  # don't use middle button
                                       minspanx=5, minspany=5,
                                       spancoords='pixels',
                                       interactive=True) 
                                       
        fig.canvas.mpl_connect('key_press_event', self.toggle_selector)
        fig.canvas.mpl_connect('draw_event', self.persist_rectangle)  
        ax.set_yticklabels([])
        ax.set_xticklabels([])
        
        self.ax = ax
        self.fig = fig
        self.cls_name = args.class_name
        self.img_paths = sorted(glob.glob(os.path.join(os.path.basename(args.video_file), '*')), key=lambda x: int(os.path.basename(x[:-4])))
        
        self.index = 0
        img = plt.imread(self.img_paths[self.index])
        self.ax.imshow(img)
    
    def persist_rectangle(self, event):
        if self.RS.active:
            self.RS.update()
    
    def line_select_callback(self, eclick, erelease):
        'eclick and erelease are the press and release events'
        x1, y1 = eclick.xdata, eclick.ydata
        x2, y2 = erelease.xdata, erelease.ydata

    def toggle_selector(self, event):
        if event.key in ['N', 'n']:
            
            if not self.is_empty():
                bbox = self.RS.extents
                
                with open('annotations.csv','a') as f: 
                    csv_writer = csv.writer(f, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                    csv_writer.writerow([os.path.abspath(self.img_paths[self.index]), int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3]), self.cls_name])
                print('Frame %d/%d'%(self.index+1, len(self.img_paths)))
            self.ax.clear()
            self.index+=1
            img = plt.imread(self.img_paths[self.index])
            self.ax.imshow(img)
            self.RS.to_draw.set_visible(True)
            self.ax.set_yticklabels([])
            self.ax.set_xticklabels([])
            self.fig.canvas.draw()
            
        if event.key in ['q','Q']:
            exit()
        
    def is_empty(self):
        return self.RS._rect_bbox==(0,0,0,1)

if __name__=='__main__':

    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--video_file", required=True, help="Path to the video file to annotate one object")
    ap.add_argument('-r', '--rotation', required=True, help="Rotation angle for frames")
    ap.add_argument('-c', '--class_name', required=True, help="Name of object's class")
    ap.add_argument('-f', '--class_file', required=False, help="Path to class file to create classes' list")
    args = ap.parse_args()
    
    classes = []
    if args.class_file is not None and not os.path.exists('classes.csv'):
        
        with open(args.class_file, 'r') as f:
            classes = [x.strip() for x in f.readlines() if x is not None]
        
        with open('classes.csv', 'w') as f:
            filewriter = csv.writer(f, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for i, c in enumerate(classes):
                filewriter.writerow([c, str(i)])
    
    fig, ax = plt.subplots()        
    if not os.path.isdir(os.path.basename(args.video_file)):
        os.mkdir(os.path.basename(args.video_file))
    
    vidcap = cv2.VideoCapture(args.video_file)
    success,image = vidcap.read()
    count, video_paths = 0, []
    if int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT)) == len(glob.glob(os.path.join(os.path.basename(args.video_file), '*'))):
        print ("Using cached video frames!!")
    else:
        print ("Creating frame image files!!")
        while success:
            if not os.path.exists('%s/%d.jpg'%(os.path.basename(args.video_file), count)):
                image = imutils.rotate_bound(image, int(args.rotation))
                cv2.imwrite('%s/%d.jpg'%(os.path.basename(args.video_file), count), image, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
            count = count + 1
            success,image = vidcap.read()
    
    # drawtype is 'box' or 'line' or 'none'
    rect_bbox = Video_Bbox(fig, ax, args)
    
    plt.show()
