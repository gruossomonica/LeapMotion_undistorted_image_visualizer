import cv2, math, ctypes
import numpy as np
import os

def save_image(folder, file_name, image):
    """
    Save image to file .png
    Input param: 
        folder: where to save the image (folder or folder path without the last '/')
        file_name: name of the file
        image: image to be saved.
    """
    if not os.path.exists(folder):
        os.makedirs(folder)
    # print(folder + '/' + file_name + '.png')
    cv2.imwrite(folder + '/' + file_name + '.png', image)

def get_image_as_numpy_array(image):
    """
    Get the numpy array related to the leap motion infrared image data
    It is useful to show the image (e.g., using the cv2.imshow method)
    """
    image_buffer_ptr = image.data_pointer # pointer to the image data buffer to directly access the memory in the data buffer using ctypes or numpy
    ctype_array_def = ctypes.c_ubyte * image.width * image.height

    # as ctypes array
    as_ctype_array = ctype_array_def.from_address(int(image_buffer_ptr))
    # as numpy array
    as_numpy_array = np.ctypeslib.as_array(as_ctype_array)
    return as_numpy_array

def convert_distortion_maps(image):
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
    
def undistort(image, coordinate_map, coefficient_map, width, height):
    destination = np.empty((width, height), dtype = np.ubyte)

    #wrap image data in numpy array
    as_numpy_array = get_image_as_numpy_array(image)
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


class ImageVisualizer:
    
    def __init__(self):
        self.gamma = 1.0 # gamma initialization
        self.alpha = 1.0 # alpha gain (contrast) initialization
        self.beta = 0 # beta bias (brightness) initialization
        
    def on_gamma_change(self, value):
        self.gamma = value/100 # value obtained from the trackbar is in percentage (from 0 to 100)
    
    def on_alpha_change(self, value):
        self.alpha = value/100 # value obtained from the trackbar is in percentage (from 0 to 100)
    
    def on_beta_change(self, value):
        self.beta = value  - 100 # value obtained from the trackbar is scaled (+100)
    
    def adjust_gamma(self, image):
        lookUpTable = np.empty((1,256), np.uint8)
        for i in range(256):
            lookUpTable[0,i] = np.clip(pow(i / 255.0, self.gamma) * 255.0, 0, 255)

        return cv2.LUT(image, lookUpTable)
    
    def adjust_contrast_brightness(self, image):
        return cv2.convertScaleAbs(image, alpha=self.alpha, beta=self.beta) # alpha gain (contrast), beta bias (brightness)
    
    def imshowpair(self, title, image_left, image_right):
        """
        Concatanate image horizontally (axis=1) and show them
        """
        # adjust gamma
        image_left = self.adjust_gamma(image_left)
        image_right = self.adjust_gamma(image_right)
        # adjust contrast and brightness
        image_left = self.adjust_contrast_brightness(image_left)
        image_right = self.adjust_contrast_brightness(image_right)
        # display images
        cv2.imshow(title, np.concatenate((image_left,image_right),axis=1))
        
    def createSettingWindow(self, title='Settings'):
        cv2.namedWindow(title, cv2.WINDOW_NORMAL)
        # createTrackbar param: trackbar name, window name, int current value, int max value (the min is always 0), onChange event function
        cv2.createTrackbar('Gamma', title, 100, 100, self.on_gamma_change) 
        cv2.createTrackbar('Alpha gain', title, 100, 500, self.on_alpha_change)
        #cv2.createTrackbar('Beta bias (brightness)', title, 100, 200 , self.on_beta_change)    
        cv2.resizeWindow(title, 500, 100)
