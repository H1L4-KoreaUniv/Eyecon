# Headpose Detection
---
### Referenced Code
* https://www.learnopencv.com/head-pose-estimation-using-opencv-and-dlib
* https://www.pyimagesearch.com/2017/04/03/facial-landmarks-dlib-opencv-python
* https://github.com/lincolnhard/head-pose-estimation

### Requirements
* Python 3.7
  * dlib
  * opencv-python
  * numpy

* Please check `Dockerfile` for more information.

### Setup
* `./setup.sh`

### Usage
* Headpose detection for images
  * `python3.7 headpose.py -i [input_dir] -o [output_dir]`
* Headpose detection for videos
  * `python3.7 headpose_video.py -i [input_video] -o [output_file]`
* Headpose detection for webcam
  * `python3.7 headpose_video.py`

### Demo
[![](https://i.imgur.com/sdOM88J.png)](https://youtu.be/MMCbQCBtch8)

# Gaze Tracking
---
### Referenced Code
* https://github.com/antoinelame/GazeTracking

### Requirements
* numpy == 1.16.1
* opencv_python == 3.4.5.20
* dlib == 19.16.0

### Licensing
This project is released by Antoine Lamé under the terms of the MIT Open Source License. View LICENSE for more information.

### Demo
[![](https://camo.githubusercontent.com/b2701b19d2b251ada6aeff2f2bb10783c5d2a930/68747470733a2f2f692e696d6775722e636f6d2f574e7167516b4f2e676966)]
