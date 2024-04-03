# Segmentation App
## Table of Contents
* **[About](#about)**
  * [manualSegmentation.py](#manualsegmentationpy)
  * [semanticSegmentation.py](#semanticsegmentationpy)
* **[Installation](#installation)**
  * [Installing the Executable](#installing-the-executable)
  * [Installing Python](#installing-python)
  * [Installing required packages](#installing-required-packages)
* **[Manual](#manual)**
* **[Notice](#notice)**
    
## About
Based on the bachelor-thesis "Microstructure analysis of materials with the assistance of artificial technology" by Kerim Yalcin from Feb 2024. 
  
Features:
* read and save image files
* use filters to change brightness and gaussian-blur amount of loaded images
* apply binarization and tresholding
* trace boundaries using resizable brush tool in black or white
* create image labels for a Resnet34 model (max. 2 classifications)
* create and train a ResNet34 model with created labels
* predict images using a trained ResNet34 model

### manualSegmentation.py
Use this script for manual label creation. After that, create labels using the image crop tool.

![Image of manualSegmentation.py after loading an image and tracing.](https://github.com/kerimyalcin95/deep-learning-segmentation/raw/main/screenshots/manualSegmentation01.jpg "Screenshot of manualSegmentation.py in action")
### semanticSegmentation.py
Use this script for creating and training a ResNet34 model. After that, predict images using the trained model.

![Image of semanticSegmentation.py after predicting an image using a trained model](https://github.com/kerimyalcin95/deep-learning-segmentation/raw/main/screenshots/semanticSegmentation01.jpg "Screenshot of semanticSegmentation.py in action")
## Installation
The application can either be started using the executable or directly by running the scripts after installing Python and the required packages.
### Installing the Executable
### Installing Python
### Installing required packages
## Manual
## Notice
* Reading and saving image file names are not supported in Unicode due to OpenCV `imread` and `imwrite` function
* Cancelling the file dialog without selecting a path can lead to termination of the app
* an internet connection is required to create the ResNet32 model
