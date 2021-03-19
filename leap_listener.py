import Leap
# 'lib' folder contains
# - Leap.dll (original file from LeapMotion v.3 sdk)
# - Leap.py (generated... see *)
# - LeapPython.dll (generated... see *)
# - LeapPython.pyd (generated... see *)
# *Generating a Python 3.x Wrapper with SWIG (in my case Python 3.7 with Swig 2.0.9):
# https://support.leapmotion.com/hc/en-us/articles/360004362237-Generating-a-Python-3-3-0-Wrapper-with-SWIG-2-0-9
# my visual studio project: C:\Users\Monica Gruosso\source\repos\leap_python37 (Release x64)

import cv2, math, ctypes
import numpy as np

class LeapEventListener(Leap.Listener):
    '''
    Subclass of Leap.Listener implementing the callback functions for some interesting events
    '''
    
    def on_init(self, controller):
        maps_initialized = False
        print("Controller initialized")
        
    def on_connect(self, controller):
        maps_initialized = False
        print("Controller connected")

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print("Controller disconnected")
    
    def on_exit(self, controller):
        print("Exited")
        
    # def on_frame(self, controller):
        # print("Frame available")
        # frame = controller.frame()
        #print("images from frame is valid: ", frame.images[0].is_valid)
        #Process frame data... 
    
    def on_device_change(self, controller):
        maps_initialized = False
        print("Device changed")
    
    def on_images(self, controller):
        #print("Images available")
        images = controller.images
        left_image = images[0]
        right_image = images[1]
        # you can correct the distortion here...
        
