import cv2
import imutils
import os
import argparse
import glob

if __name__=='__main__':

    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--video_dir", required=True, help="Directory to the video file to annotate one object")
    ap.add_argument('-r', '--rotation', required=True, help="Rotation angle for frames")
    args = ap.parse_args()
    
    for vid in glob.glob(os.path.join(args.video_dir, '*')):
        if not os.path.isdir(os.path.basename(vid)):
            os.mkdir(os.path.basename(vid))
        
        vidcap = cv2.VideoCapture(vid)
        success,image = vidcap.read()
        count = 0
        if int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT)) == len(glob.glob(os.path.join(os.path.basename(vid), '*'))):
            print ("Using cached video frames!!")
        else:
            print ("Creating frame image files!!")
            while success:
                if not os.path.exists('%s/%d.jpg'%(os.path.basename(vid), count)):
                    image = imutils.rotate_bound(image, int(args.rotation))
                    cv2.imwrite('%s/%d.jpg'%(os.path.basename(vid), count), image, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
                count = count + 1
                success,image = vidcap.read()
