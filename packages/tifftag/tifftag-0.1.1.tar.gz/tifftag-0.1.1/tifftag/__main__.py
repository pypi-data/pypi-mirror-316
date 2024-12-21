# -*- coding: utf-8 -*-
"""
Created on Mon Nov 27 16:02:09 2023

@author: clanglois1
"""
import os
from os.path import abspath
import sys
import pyqtgraph as pg
from PyQt5.QtWidgets import QApplication, QWidget
import numpy as np
import tifffile as tf
from tifftag import ioTIFF_v2 as zei

path2thisFile = abspath(getsourcefile(lambda:0))
uiclass, baseclass = pg.Qt.loadUiType(os.path.dirname(path2thisFile) + "/__dropTo.ui")


class MainWindow(uiclass, baseclass):
    # def __init__(self, rawImage, remOutImage, parent):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        self.imageView.ui.histogram.hide()
        self.imageView.ui.roiBtn.hide()
        self.imageView.ui.menuBtn.hide()

        self.drag_and_drop.textChanged.connect(self.dropE)

    def dropE(self):        

        text = self.drag_and_drop.toPlainText()
        print("\n" + text)
        self.getPathfromURL(text)

    def getPathfromURL(self, text):
        self.path = text[8:]
        self.openImage()
        
    def openImage(self):

        if self.path != "":
            self.image = tf.TiffFile(self.path).asarray()
            
            self.image = np.flip(self.image, 1)
            self.image = np.rot90(self.image, k=1)
            
            self.imageView.ui.histogram.hide()
            self.imageView.ui.roiBtn.hide()
            self.imageView.ui.menuBtn.hide()
            self.imageView.setImage(self.image)  
            self.imageView.autoRange()
            
            self.displayTags()        


        
    def displayTags(self):

        dictZeiss = zei.readZeissMD(self.path)
        
        tagsDict = dictZeiss.__dict__
        
        MostUsefulZeissTags = ('AP_STAGE_AT_T', 'AP_ACTUALKV', 'AP_IMAGE_PIXEL_SIZE', 'AP_MAG',
                               'AP_FRAME_TIME', 'AP_DATE', 'SV_IMAGE_PATH',
                               'SV_USER_NAME', 'WIDTH', 'HEIGHT', 'AP_APERTURESIZE',
                               'DP_SCAN_ROT', 'AP_SCANROTATION', 'AP_STAGE_AT_R')
        
        
        UsefulZeissTags_FIB = ('COLOR_DEPTH', 'DP_DWELL_TIME', 'DP_IMAGE_STORE',
                           'DP_TILT_CORRECTION', 'DP_LARGE_BEAMSHIFT', 'DP_SCANRATE', 'DP_NOISE_REDUCTION',
                           'AP_BRIGHTNESS', 'AP_CONTRAST', 'AP_WD')
        
        UsefulZeissTags = ('DP_BSD_AUTOLEVEL_MODE', 'DP_HIGH_CURRENT',
                           'COLOR_DEPTH', 'DP_DWELL_TIME', 'DP_COMPUCENTRIC_MODE', 'DP_TILTED', 'DP_4QBSD_GAIN', 'DP_IMAGE_STORE',
                           'DP_BSD_MODE', 'DP_BSD_AUTO', 'DP_USE_REF_MAG', 'DP_DETECTOR_TYPE',
                           'DP_OPTIBEAM', 'DP_FINAL_LENS', 'DP_DYNFOCUS', 'DP_TILT_CORRECTION', 'DP_PIXEL_SIZE',
                           'DP_COLUMN_TYPE', 'DP_LARGE_BEAMSHIFT',  'DP_SEM', 'DP_SCANRATE', 'DP_NOISE_REDUCTION',
                           'AP_FRAME_INT_COUNT', 'AP_MAG', 'AP_FREE_WD', 'AP_SPOTSIZE', 'AP_APERTURESIZE', 'AP_BEAM_CURRENT', 'AP_PIXEL_SIZE',
                           'AP_BRIGHTNESS', 'AP_CONTRAST', 'AP_WD', 'AP_STAGE_GOTO_T', 'AP_ESB_GRID',
                           'AP_WIDTH', 'AP_TIME')
        
        tags = "Most important information : \n"       
 
        if len(tagsDict) > 0:
            for key in MostUsefulZeissTags:
                tags += str(tagsDict[key]) + "\n"
            
            tags +="\n\nDetails : \n"

            try:                    
                for key in UsefulZeissTags:
                    tags += str(tagsDict[key]) + "\n"
            except:
                for key in UsefulZeissTags_FIB:
                    tags += str(tagsDict[key]) + "\n"               
        
        self.tags_browser.setText(
            "\n\n\n\n" + self.path + 
            "\n\n\n" + tags
            ) 
        
        self.tags_browser.verticalScrollBar().setValue(
            self.tags_browser.verticalScrollBar().minimum()
            )
        
        self.drag_and_drop.clear()
        self.drag_and_drop.setAcceptDrops(True)
        self.drag_and_drop.textChanged.connect(self.dropE)
        print("---------------------------------------------------------------")

def main():

	app = QApplication(sys.argv)
	w = MainWindow()
	w.show()
	app.setQuitOnLastWindowClosed(True)
	app.exec_() 
		
#%% Opening of the initial data    
if __name__ == '__main__':
	main()