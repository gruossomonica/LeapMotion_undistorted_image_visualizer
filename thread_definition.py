import cv2
import threading
from image_utils import *

import sys
sys.path.append("lib") 
import Leap

class CamThread(threading.Thread):
    """
    A class used to define the webcam thread
    ...

    Attributes
    ----------
    camID : int
        the webcam device ID
    resolution : (int, int)
        the (width, height) webcam resolution 
    """

    def __init__(self, camID, resolution):        
        threading.Thread.__init__(self)
        self.camID = camID  
        self.resolution = resolution
        self.initialiaze_cam() 
        
    def initialiaze_cam(self):
        self.cam = cv2.VideoCapture(self.camID, cv2.CAP_DSHOW)
        self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, self.resolution[0])
        self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, self.resolution[1]) 
        
    def run(self):        
        print("CamThread is running...")
        #self.cam_preview()
        
    # def cam_preview(self):
        # if self.cam is None or not self.cam.isOpened():
            # print('Warning: unable to open cam preview! Check camID, which is set to ', self.camID)
            # rval = False            
        # else:  # try to get the first frame
            # rval, frame = self.cam.read()
        # while(rval):
            # cv2.imshow(self.title, frame)            
            # rval, frame = self.cam.read() # read new image  
            # key = cv2.waitKey(1)
            # if key == ord('q'): # Exit
                # break                
        # self.cam.release()
        # cv2.destroyWindow(self.title)
        
    def read_frame(self):
        if self.cam.isOpened():  # try to get the first frame
            rval, frame = self.cam.read()
            if rval:
                return frame
            else:
                return None
    
    def release_cam(self):
        self.cam.release()

class LeapImageThread(threading.Thread):
    """
    A class used to define the Leap Motion camera thread
    ...

    Attributes
    ----------
    controller: the Leap Motion controller object
    maps_initialized: False if the distortion maps are not coverts
    left_coordinates, left_coefficients: output of the convert_distortion_maps method in the case of left images
    right_coordinates, right_coefficients: output of the convert_distortion_maps method in the case of right images
    """
    
    def __init__(self, controller):
        threading.Thread.__init__(self)
        self.controller = controller
        self.maps_initialized = False
        self.left_coordinates = None
        self.left_coefficients = None
        self.right_coordinates = None
        self.right_coefficients = None
    
    def run(self):
        print("LeapImageThread is running...")  
        
        # Create setting window
        # self.image_visualizer.createSettingWindow('Leap Image Settings')
        
        #image read loop
        # while(True):
            # left_raw_image, right_raw_image, undistorted_left, undistorted_right = self.read_images() 
            # self.image_visualizer.imshowpair('Left and right images', left_raw_image, right_raw_image) 
            # self.image_visualizer.imshowpair('Left and right undistorted images', undistorted_left, undistorted_right)            
            # key = cv2.waitKey(1)
            # if key == ord('q'): # Exit
                # break
            # # elif key == ord('s'): # save images
                # # if not os.path.exists(PATH_LEAP_IMG):
                    # # os.makedirs(PATH_LEAP_IMG)
                # # cv2.imwrite(PATH_LEAP_IMG + '/' + str(i) + "img_raw_left.png", get_image_as_numpy_array(frame.images[0]))
                # # cv2.imwrite(PATH_LEAP_IMG + '/' + str(i) + "img_raw_right.png", get_image_as_numpy_array(frame.images[1]))
                # # cv2.imwrite(PATH_LEAP_IMG + '/' + str(i) + "img_undist_left.png", undistorted_left)
                # # cv2.imwrite(PATH_LEAP_IMG + '/' + str(i) + "img_undist_right.png", undistorted_right)
        # cv2.destroyAllWindows()
    
    def read_images(self): 
        frame = self.controller.frame()
        if frame.images[0].is_valid and frame.images[1].is_valid:
            left_raw_image = get_image_as_numpy_array(frame.images[0])
            right_raw_image = get_image_as_numpy_array(frame.images[1])        
            if not self.maps_initialized: # The following code only converts the distortion maps once (but doesn’t handle the cases where the distortion maps can change)
                self.left_coordinates, self.left_coefficients = convert_distortion_maps(frame.images[0])
                self.right_coordinates, self.right_coefficients = convert_distortion_maps(frame.images[1])
                self.maps_initialized = True
            undistorted_left = undistort(frame.images[0], self.left_coordinates, self.left_coefficients, 600, 600)
            undistorted_right = undistort(frame.images[1], self.right_coordinates, self.right_coefficients, 600, 600)
        return left_raw_image, right_raw_image, undistorted_left, undistorted_right
                   