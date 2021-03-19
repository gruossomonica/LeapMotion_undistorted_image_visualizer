# LeapMotion Undistorted Infrared Image Visualizer

This repo contains the source code of a visualizer built with Python 3.7.0 and OpenCV on Window 10. It is useful for displaying undistorted IR images captured by a Leap Motion device. A simple viewer for RGB images captured by a webcam is also provided.

![GUI](images/gui1.png)

## Requirements

- Wrapper of the Leap Motion SDK v3 for Python 3.7 (Windows), since it is available only for Python 2. The wrapper is available in the `lib` folder. If you need your wrapper for another version of Python or other OS, please follow [this guide](https://support.leapmotion.com/hc/en-us/articles/360004362237-Generating-a-Python-3-3-0-Wrapper-with-SWIG-2-0-9)
- Python 3.7.0
- OpenCV (suggested 4.x)
- NumPy
- math
- os
- ctypes
- threading
