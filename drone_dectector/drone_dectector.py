# Drone dectector - Drone detector
# Copyright (C) 2023 - Malapert
#
# This file is part of Drone dectector.
#
# Drone dectector is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Drone dectector is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Drone dectector.  If not, see <https://www.gnu.org/licenses/>.
"""This module contains the library."""
import logging
import configparser
from ._version import __name_soft__
from abc import ABC, abstractmethod

import cv2
import numpy as np

logger = logging.getLogger(__name__)


class Detector:
    
    def __init__(self, input):
        self.__input = input
        self.__contour_area: int = 0
        self.__treshold: int = 0
        
    @property
    def input(self):
        return self.__input
    
    @property
    def contour_area(self):
        return self.__contour_area
    
    @contour_area.setter
    def contour_area(self, val: int):
        if val <= 0 :
            raise ValueError("val cannot be <= 0")
        self.__contour_area = val
        
    @property
    def treshold(self):
        return self.__treshold
    
    @treshold.setter
    def treshold(self, val:int):
        if val < 0 or val > 255:
            raise ValueError("Treshod must be in [0, 255]")        
        self.__treshold = val
    
    @abstractmethod
    def _condition(self, video_capture):
        pass
    
    def _prepare_image(self, img_rgb):
        prepared_frame = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        prepared_frame = cv2.GaussianBlur(src=prepared_frame, ksize=(5,5), sigmaX=0)
        return prepared_frame  
    
    def _dilute_image(self, diff_frame):
        kernel = np.ones((5, 5))
        diff_frame = cv2.dilate(diff_frame, kernel, 1) 
        return diff_frame  
    
    def _filter_and_plot_contours(self, contours, img_rgb):        
        countour_nb = 0                
        for contour in contours:
            if (cv2.contourArea(contour) < self.contour_area ):
                # too small: skip!
                continue
            (x, y, w, h) = cv2.boundingRect(contour)                
            cv2.rectangle(img=img_rgb, pt1=(x, y), pt2=(x + w, y + h), color=(0, 255, 0), thickness=2) 
            countour_nb = countour_nb + 1
        if countour_nb > 0:
            logger.debug(f"{countour_nb} contours have been detected !!!")
                    
                         
    def detect(self):
        logger.info("Press Esc to exit !")
        logger.info(f"A threshold > {self.treshold} is applied")
        logger.info(f"Filter with contourArea < {self.contour_area} is applied")
        frame_count = 0
        previous_frame = None        
        cam = cv2.VideoCapture(self.input)
        while self._condition(cam):

            ret_val, img_brg = cam.read()
            img_brg = cv2.flip(img_brg, 1)
            img_rgb = cv2.cvtColor(src=img_brg, code=cv2.COLOR_BGR2RGB)
                        
            if ((frame_count % 2) == 0):

                # 2. Prepare current image; grayscale and blur
                current_frame = self._prepare_image(img_rgb)
        
                # 3. Set previous frame and continue if there is None
                if (previous_frame is None):
                    # First frame; there is no previous one yet
                    previous_frame = current_frame
                    continue
                    
                # calculate difference and update previous frame
                diff_frame = cv2.absdiff(src1=previous_frame, src2=current_frame)
                previous_frame = current_frame

                # 4. Dilute the image a bit to make differences more seeable; more suitable for contour detection
                diff_frame = self._dilute_image(diff_frame)

                # 5. Only take different areas that are different enough (>20 / 255)
                thresh_frame = cv2.threshold(src=diff_frame, thresh=self.treshold, maxval=255, type=cv2.THRESH_BINARY)[1]                       
                contours, _ = cv2.findContours(image=thresh_frame, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_SIMPLE)
                
                # 6. Some rule to apply to keep or skip contours                            
                self._filter_and_plot_contours(contours, img_rgb)
                
                # 7. plot result
                cv2.imshow('Drone detector', img_rgb)

                if (cv2.waitKey(30) == 27):
                    break   
            
    
class CameraDetector(Detector):
    
    def __init__(self):
        super().__init__(0)
        logger.info("Use camera")
    
    def _condition(self, video_capture):
        return True
    
    
    
class MovieDetector(Detector):
    
    def __init__(self, file: str):
        super().__init__(file)
        logger.info(f"Use video {file}")
    
    def _condition(self, video_capture):
        return video_capture.isOpened()    
               
    
class DetectorFactory:
    
    @staticmethod
    def create(input) -> Detector:
        detector: Detector
        if type(input) == int :
            detector = CameraDetector()
        elif type(input) == str:
            detector = MovieDetector(input)
        else:
            raise Exception("Unknown type for input")
        return detector
                 

class DroneDectectorLib:
    """The library"""

    def __init__(self, treshold: int, contour_area: int, *args, **kwargs):
        # pylint: disable=unused-argument
        if "level" in kwargs:
            DroneDectectorLib._parse_level(kwargs["level"])
            
        if "file" in kwargs:
            self.__file = kwargs["file"]
        else:
            self.__file = 0
            
        self.__contour_area = contour_area
        self.__treshold = treshold
        
    @property
    def contour_area(self):
        return self.__contour_area
    
    @property
    def treshold(self):
        return self.__treshold

    @staticmethod
    def _parse_level(level: str):
        """Parse level name and set the rigt level for the logger.
        If the level is not known, the INFO level is set

        Args:
            level (str): level name
        """
        logger_main = logging.getLogger(__name_soft__)
        if level == "INFO":
            logger_main.setLevel(logging.INFO)
        elif level == "DEBUG":
            logger_main.setLevel(logging.DEBUG)
        elif level == "WARNING":
            logger_main.setLevel(logging.WARNING)
        elif level == "ERROR":
            logger_main.setLevel(logging.ERROR)
        elif level == "CRITICAL":
            logger_main.setLevel(logging.CRITICAL)
        elif level == "TRACE":
            logger_main.setLevel(logging.TRACE)  # type: ignore # pylint: disable=no-member
        else:
            logger_main.warning(
                "Unknown level name : %s - setting level to INFO", level
            )
            logger_main.setLevel(logging.INFO)

    @property
    def file(self) -> str:
        """The video file.

        :getter: Returns the video file
        :type: str
        """
        return self.__file
    
    def detect(self):
        cam: Detector = DetectorFactory.create(self.file)
        cam.contour_area = self.contour_area
        cam.treshold = self.treshold
        cam.detect()
    
    


