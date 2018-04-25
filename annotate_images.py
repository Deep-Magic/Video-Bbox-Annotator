from matplotlib.widgets import RectangleSelector, Button, RadioButtons
import matplotlib.patches as patches
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

    def __init__(self, fig, ax, img_paths, classes):
    
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
        self.axradio = plt.axes([0.0, 0.0, 0.2, 1])
        self.radio = RadioButtons(self.axradio, classes)
        self.zoom_scale = 1.2
        self.img_paths = img_paths
        self.zoom_id = fig.canvas.mpl_connect('scroll_event', self.zoom)
        self.axsubmit = plt.axes([0.81, 0.05, 0.1, 0.05])
        self.b_submit = Button(self.axsubmit, 'Submit')
        self.b_submit.on_clicked(self.submit)
        
        self.index = 0
        img = plt.imread(self.img_paths[self.index])
        self.ax.imshow(img, aspect='auto')
    
    def line_select_callback(self, eclick, erelease):
        'eclick and erelease are the press and release events'
        x1, y1 = eclick.xdata, eclick.ydata
        x2, y2 = erelease.xdata, erelease.ydata
    
    def persist_rectangle(self, event):
        if self.RS.active:
            self.RS.update()
        
    def zoom(self, event):
        
        if not event.inaxes:
            return
        cur_xlim = self.ax.get_xlim()
        cur_ylim = self.ax.get_ylim()

        xdata = event.xdata # get event x location
        ydata = event.ydata # get event y location

        if event.button == 'down':
            # deal with zoom in
            scale_factor = 1 / self.zoom_scale
        elif event.button == 'up':
            # deal with zoom out
            scale_factor = self.zoom_scale
        else:
            # deal with something that should never happen
            scale_factor = 1
            print (event.button)

        new_width = (cur_xlim[1] - cur_xlim[0]) * scale_factor
        new_height = (cur_ylim[1] - cur_ylim[0]) * scale_factor

        relx = (cur_xlim[1] - xdata)/(cur_xlim[1] - cur_xlim[0])
        rely = (cur_ylim[1] - ydata)/(cur_ylim[1] - cur_ylim[0])

        self.ax.set_xlim([xdata - new_width * (1-relx), xdata + new_width * (relx)])
        self.ax.set_ylim([ydata - new_height * (1-rely), ydata + new_height * (rely)])
        self.ax.figure.canvas.draw()

    
    def submit(self, event):
        if not self.is_empty():
            bbox = self.RS.extents
            with open('annotations.csv','a') as f: 
                csv_writer = csv.writer(f, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                csv_writer.writerow([os.path.abspath(self.img_paths[self.index]), int(bbox[0]), int(bbox[2]), int(bbox[1]), int(bbox[3]), self.radio.value_selected])
            rect = patches.Rectangle((bbox[0],bbox[2]),bbox[1]-bbox[0],bbox[3]-bbox[2],linewidth=1,edgecolor='g',facecolor='g', alpha=0.4)
            self.ax.add_patch(rect)
            self.RS.to_draw.set_visible(False)
            self.fig.canvas.draw()
            
    def toggle_selector(self, event):
        if event.key in ['N', 'n']:
            self.ax.clear()
            self.index+=1
            img = plt.imread(self.img_paths[self.index])
            self.ax.imshow(img)
            self.ax.set_yticklabels([])
            self.ax.set_xticklabels([])
            self.fig.canvas.draw()
            
        if event.key in ['q','Q']:
            exit()
        
    def is_empty(self):
        return self.RS._rect_bbox==(0,0,0,1)

if __name__=='__main__':

    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--img_dir", required=True, help="Path to the directory of images to annotate")
    ap.add_argument('-f', '--class_file', required=True, help="Path to class file to create classes' list")
    args = ap.parse_args()
    
    with open(args.class_file, 'r') as f:
        classes = [x.strip() for x in f.readlines() if x is not None]
    if not os.path.exists('classes.csv'):
        with open('classes.csv', 'w') as f:
            filewriter = csv.writer(f, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for i, c in enumerate(classes):
                filewriter.writerow([c, str(i)])
    
    fig, ax = plt.figure(), plt.gca() 
    ax.set_position([0.22,0.1,0.7,0.8])      
    img_paths = glob.glob(os.path.join(args.img_dir, '*'))
    
    # drawtype is 'box' or 'line' or 'none'
    rect_bbox = Video_Bbox(fig, ax, img_paths, classes)
    
    plt.show()
