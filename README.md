# Segmentation App
## Table of Contents
* **[About](#about)**
  * [manualSegmentation.py](#manualsegmentationpy)
  * [semanticSegmentation.py](#semanticsegmentationpy)
* **[Installation](#installation)**
  * [Installing the Executables](#installing-the-executables)
  * [Installing Python](#installing-python)
  * [Installing required packages](#installing-required-packages)
  * [Installing script files](#installing-script-files)
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
* create and train a ResNet34 model by using the labels
* predict images with a trained ResNet34 model

### manualSegmentation.py
Use this script for manual label creation. After that, create labels using the image crop tool.

![Image of manualSegmentation.py after loading an image and tracing.](https://github.com/kerimyalcin95/deep-learning-segmentation/raw/main/screenshots/manualSegmentation01.jpg "Screenshot of manualSegmentation.py in action")
### semanticSegmentation.py
Use this script for creating and training a ResNet34 model. After that, predict images using the trained model.

![Image of semanticSegmentation.py after predicting an image using a trained model](https://github.com/kerimyalcin95/deep-learning-segmentation/raw/main/screenshots/semanticSegmentation01.jpg "Screenshot of semanticSegmentation.py in action")
## Installation
The application can either be started using the executable or directly by running the scripts after installing Python and the required packages.
### Installing the Executables
The executables are created using [auto-py-to-exe](https://pypi.org/project/auto-py-to-exe/) by Brent Vollebregt and can be downloaded [here](https://github.com/kerimyalcin95/deep-learning-segmentation/releases) under *Assets*. The interpreter version used is: Python 3.11.8

Steps:
1. create a folder named *structureAnalysis* or similar
2. copy both `manualSegmentation.exe` and `semanticSegmentation.exe` in this folder
3. copy `codes.txt` in this folder
4. start either one of the applications

After that, you should see the directories `/labels`, `/images`, `/raw` and `/raw/labels` created automatically.

### Installing Python
Steps:
1. Download [Python 3.11.x](https://www.python.org/downloads/)
2. Run the installation (add environment PATH, remove MAX_PATH limitation)
3. open `cmd.exe` and type `python --version`

You should see something like `Python 3.x.x` on the console output.
### Installing required packages
You need `fastai v2` and `OpenCV` in order to use the script files.

Documentation:
* [fastai](https://docs.fast.ai/)
* [OpenCV](https://docs.opencv.org/4.9.0/d6/d00/tutorial_py_root.html)

Steps:
1. start `cmd.exe` and type `pip install opencv-python`
2. after that, type `pip install fastai`

### Installing script files
This is similar to installing the executables

Steps:
1. create a folder named *structureAnalysis* or similar
2. copy both `manualSegmentation.py` and `semanticSegmentation.py` in this folder
3. copy `codes.txt` in this folder
4. start either one of the scripts by double clicking on the files

After that, you should see the directories `/labels`, `/images`, `/raw` and `/raw/labels` created automatically.

## Manual
## Notice
* Reading and saving image file names are not supported in Unicode due to OpenCV `imread` and `imwrite` function
* Cancelling the file dialog without selecting a path can lead to termination of the app
* an internet connection is required to create the ResNet32 model
