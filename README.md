This is a simple widget to effectively annotate videos in the context of single object tracking via bounding boxes. Once a video is loaded, you can click `n` key to move from one frame to the other. Any frame on which you press `n` on will save the particular rectangle persistent in that image. If there's no rectangle on screen, no annotations are saved.

### USAGE:

```
python annotate.py -v <VIDEO_FILE> -c <CLASS_FILE> -r <ROTATION_ANGLE> 
```
