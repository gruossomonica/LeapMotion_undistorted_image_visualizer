import sys
sys.path.append("lib") 
import Leap
# 'lib' folder contains
# - Leap.dll (original file from LeapMotion v.3 sdk)
# - Leap.py (generated... see *)
# - LeapPython.dll (generated... see *)
# - LeapPython.pyd (generated... see *)
# *Generating a Python 3.x Wrapper with SWIG (in my case Python 3.7 with Swig 2.0.9):
# https://support.leapmotion.com/hc/en-us/articles/360004362237-Generating-a-Python-3-3-0-Wrapper-with-SWIG-2-0-9

import cv2
import numpy as np
#from leap_listener import LeapEventListener
from image_utils import *
from thread_definition import *

PATH_CAM_IMG = "cam_images"
PATH_LEAP_IMG = "leap_images"

## Leap Motion SDK v3: https://developer.leapmotion.com/releases/leap-motion-orion-321
## Set up guide: https://developer-archive.leapmotion.com/documentation/python/devguide/Project_Setup.html#importing-the-leap-motion-module

def capture_images(cam, leap, image_visualizer):
    # Capture images until 'q' is pressed
    print("Please, press 'q' to stop capturing images and 's' to save them.")      
    save_images = False
    while(True):
        # read frames
        cam_frame = cam.read_frame()
        left_raw_image, right_raw_image, undistorted_left, undistorted_right = leap.read_images() 
        if not (cam_frame is None):
            # display webcam frame
            cv2.imshow('Webcam images', cam_frame)
        if not (left_raw_image is None):
            # display leap images
            # image_visualizer.imshowpair('Left and right images', left_raw_image, right_raw_image)
            image_visualizer.imshowpair('Left and right undistorted images', undistorted_left, undistorted_right)
        key = cv2.waitKey(1)
        if key == ord('q'): # Exit
            break
        elif key == ord('s'):  
            if not save_images:
                num_img = 1
                save_images = True
        if save_images:    
            save_image(PATH_CAM_IMG, str(num_img), cam_frame)  # save_image(folder, file_name, image)  
            # save_image(PATH_LEAP_IMG, str(num_img)+'_left_raw_image', left_raw_image) # save_image(folder, file_name, image)
            # save_image(PATH_LEAP_IMG, str(num_img)+'_right_raw_image', right_raw_image) # save_image(folder, file_name, image)
            save_image(PATH_LEAP_IMG, str(num_img)+'_undistorted_left', undistorted_left) # save_image(folder, file_name, image)           
            save_image(PATH_LEAP_IMG, str(num_img)+'_undistorted_right', undistorted_right) # save_image(folder, file_name, image)         
            num_img += 1   
    cam.release_cam()
    cv2.destroyAllWindows()

def main():
    image_visualizer = ImageVisualizer() 

    # Create setting window
    image_visualizer.createSettingWindow('Leap Image Settings')    
            
    # Create an event listener
    #listener = LeapEventListener()
    
    # Get the controller
    controller = Leap.Controller()
    # Before you can get image data, you must set the POLICY_IMAGES flag
    controller.set_policy(Leap.Controller.POLICY_IMAGES)
    
    # Example -- Add listener
    #controller.add_listener(listener)    
    # Keep this process running until Enter is pressed
    # print("Press Enter to quit...")
    # sys.stdin.readline()
    # Remove the sample listener when done
    #controller.remove_listener(listener) 
       
    # Start the Leap Capture Thread
    leap = LeapImageThread(controller)
    leap.start()
    
    # Start the Webcam Capture Thread: title, camID, resolution
    cam = CamThread(0, (640, 360)) # 640, 480
    cam.start()  
    
    capture_images(cam, leap, image_visualizer)
        
if __name__ == "__main__":
    main()
