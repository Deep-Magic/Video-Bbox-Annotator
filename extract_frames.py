import numpy as np
import cv2
import glob
import argparse
import imutils
import os

if __name__=='__main__':

    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--videos_dir", required=True, help="Path to the dir of videos") 
    ap.add_argument("-o", "--frames_dir", required=True, help="Path to the output dir")
    ap.add_argument("-n", "--num_images", required=False, help="Number of images per video to sample")
    ap.add_argument("-r", "--rotation", required=False, action='store_true', help="Angle of rotation") 
    args = ap.parse_args()

    if not os.path.isdir(args.frames_dir):
        os.mkdir(args.frames_dir)

    for f in glob.glob(os.path.join(args.videos_dir, '*')):

        print (f)
        cap = cv2.VideoCapture(f)
        sample_rate = 1 if args.num_images is None else int(cap.get(cv2.CAP_PROP_FRAME_COUNT))/int(args.num_images)
        if not os.path.isdir(os.path.join(args.frames_dir, f.split('/')[-1][:-4])):
            os.mkdir(os.path.join(args.frames_dir, f.split('/')[-1][:-4]))
        
        for i in range(0, int(cap.get(cv2.CAP_PROP_FRAME_COUNT)), sample_rate):
            
            cap.set(1,i);
            ret, frame = cap.read()
            if ret:
                if args.rotation:
                    if '.1' in f:
                        frame = imutils.rotate_bound(frame, 90)
                    else:
                        frame = imutils.rotate_bound(frame, 270)     
                
                if os.path.exists(os.path.join(*[args.frames_dir, f.split('/')[-1][:-4], f.split('/')[-1][:-4]+'_%d.jpg'%(i)])):
                    continue
                else:
                    cv2.imwrite(os.path.join(*[args.frames_dir, f.split('/')[-1][:-4], f.split('/')[-1][:-4]+'_%d.jpg'%(i)]), frame)
            
        cap.release()
