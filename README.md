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

## Usage and Info

The main file is the `leap_camera_control-py`. 
Press `q` to stop execution and exit. 
Press `s` to save images in folders. The folder paths are defined [here](https://github.com/gruossomonica/LeapMotion_Undistorted_Image_Visualizer/blob/7f627de95ac4f857605f8243ef470872e0f050bd/leap_camera_control.py#L18-L19).

Two threads starts: one is related to the Leap Motion controller and IR images acquisition, the other manages the webcam execution flow. 
The theard definition is provided in `thread_definition.py`.
If you prefere to use listener to manage the Leap Motion controller, please follow the example provided in comments of the main file and in `leap_listener.py`.
There is an interesting discussion on using the listener in the [Leap Motion developer guide](https://developer-archive.leapmotion.com/documentation/python/devguide/Sample_Tutorial.html#id40).

A simple setting window is also defined using OpenCV. It can be used to change the gamma and contrast of the undistorted IR images.
You can change the code in the `ImageVisualizer` class defined in `image_utils.py` to add more parameters to the settings window.

The `image_utils.py` file contains the image processing code. The distortion of the data acquired by the Leap Motion was corrected using bilinear interpolation. Other useful information about distortion maps can be found in [Leap Motion API documentation](https://developer-archive.leapmotion.com/documentation/python/devguide/Leap_Images.html?proglang=python).


