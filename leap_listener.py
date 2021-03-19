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
    
    maps_initialized = False
    
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
        
        if left_image.is_valid and right_image.is_valid:
            #print("left_image w - h: ", left_image.width, " - ", left_image.height) # 640 - 240
            ## Display distorted raw images
            # cv2.imshow('Left image', self.get_image_as_numpy_array(left_image))
            # cv2.imshow('Right image', self.get_image_as_numpy_array(right_image))
            
            if not self.maps_initialized: # The following code doesn’t handle the cases where the distortion maps can change
                print("Converting distortion maps...")
                left_coordinates, left_coefficients = self.convert_distortion_maps(left_image)
                right_coordinates, right_coefficients = self.convert_distortion_maps(right_image)
                maps_initialized = True

            print("Start computing undistorted images...")
            undistorted_left = self.undistort(left_image, left_coordinates, left_coefficients, 400, 400)
            undistorted_right = self.undistort(right_image, right_coordinates, right_coefficients, 400, 400)

            # display images
            cv2.imshow('Left Camera', undistorted_left)
            cv2.imshow('Right Camera', undistorted_right)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                #closing all open windows  
                cv2.destroyAllWindows()
            
    def get_image_as_numpy_array(self, image):
        '''
        Get the numpy array related to the leap motion infrared image data
        It is useful to show the image (e.g., using the cv2.imshow method)
        '''
        image_buffer_ptr = image.data_pointer # pointer to the image data buffer to directly access the memory in the data buffer using ctypes or numpy
        ctype_array_def = ctypes.c_ubyte * image.width * image.height

        # as ctypes array
        as_ctype_array = ctype_array_def.from_address(int(image_buffer_ptr))
        # as numpy array
        as_numpy_array = np.ctypeslib.as_array(as_ctype_array)
        return as_numpy_array
        
    def convert_distortion_maps(self, image):
        distortion_length = image.distortion_width * image.distortion_height
        xmap = np.zeros(distortion_length//2, dtype=np.float32)
        ymap = np.zeros(distortion_length//2, dtype=np.float32)

        for i in range(0, distortion_length, 2):
            xmap[distortion_length//2 - i//2 - 1] = image.distortion[i] * image.width
            ymap[distortion_length//2 - i//2 - 1] = image.distortion[i + 1] * image.height

        xmap = np.reshape(xmap, (image.distortion_height, image.distortion_width//2))
        ymap = np.reshape(ymap, (image.distortion_height, image.distortion_width//2))

        #resize the distortion map to equal desired destination image size
        resized_xmap = cv2.resize(xmap,
                                  (image.width, image.height),
                                  0, 0,
                                  cv2.INTER_LINEAR)
        resized_ymap = cv2.resize(ymap,
                                  (image.width, image.height),
                                  0, 0,
                                  cv2.INTER_LINEAR)

        #Use faster fixed point maps
        coordinate_map, interpolation_coefficients = cv2.convertMaps(resized_xmap,
                                                                     resized_ymap,
                                                                     cv2.CV_32FC1,
                                                                     nninterpolation = False)

        return coordinate_map, interpolation_coefficients
        
    def undistort(self, image, coordinate_map, coefficient_map, width, height):
        destination = np.empty((width, height), dtype = np.ubyte)

        #wrap image data in numpy array
        as_numpy_array = self.get_image_as_numpy_array(image)
        img = np.reshape(as_numpy_array, (image.height, image.width))

        #remap image to destination
        destination = cv2.remap(img,
                                coordinate_map,
                                coefficient_map,
                                interpolation = cv2.INTER_LINEAR)

        #resize output to desired destination size
        destination = cv2.resize(destination,
                                 (width, height),
                                 0, 0,
                                 cv2.INTER_LINEAR)
        return destination
