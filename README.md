# Segmentation App
## Table of Contents
* **[About](#about)**
  * [manualSegmentation.py](#manualsegmentationpy)
  * [semanticSegmentation.py](#semanticsegmentationpy)
* **[Installation](#installation)**
  * [Installing Executables](#installing-executables)
  * [Installing Python](#installing-python)
  * [Installing Required Packages](#installing-required-packages)
  * [Installing Script Files](#installing-script-files)
* **[Manual](#manual)**
  * [Preparing Image Label Creation](#preparing-image-label-creation)
  * [Create Image Reference Labels](#create-image-reference-labels)
  * [Train and Save a Model](#train-and-save-a-model)
  * [Predict an Image From a Loaded Model](#predict-an-image-from-a-loaded-model)
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
Use this script for manual label creation. After that, create labels using the image crop tool.<br><br>
![Image of manualSegmentation.py after loading an image and tracing.](https://github.com/kerimyalcin95/deep-learning-segmentation/raw/main/screenshots/manualSegmentation01.jpg "Screenshot of manualSegmentation.py in action")<br><br>
### semanticSegmentation.py
Use this script for creating and training a ResNet34 model. After that, predict images using the trained model.<br><br>
![Image of semanticSegmentation.py after predicting an image using a trained model](https://github.com/kerimyalcin95/deep-learning-segmentation/raw/main/screenshots/semanticSegmentation01.jpg "Screenshot of semanticSegmentation.py in action")<br><br>
## Installation
The application can either be started using the executable or directly by running the scripts after installing Python and the required packages.
### Installing Executables
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
### Installing Required Packages
You need `fastai v2` and `OpenCV` in order to use the script files.

Documentation:
* [fastai](https://docs.fast.ai/)
* [OpenCV](https://docs.opencv.org/4.9.0/d6/d00/tutorial_py_root.html)

Steps:
1. start `cmd.exe` and type `pip install opencv-python`
2. after that, type `pip install fastai`

### Installing Script Files
This is similar to installing the executables

Steps:
1. create a folder named *structureAnalysis* or similar
2. copy both `manualSegmentation.py` and `semanticSegmentation.py` in this folder
3. copy `codes.txt` in this folder
4. start either one of the scripts by double clicking on the files

After that, you should see the directories `/labels`, `/images`, `/raw` and `/raw/labels` created automatically.

## Manual
### Preparing Image Label Creation
1. start `manualSegmentation`
2. on the left side load an image with `[Load Image]`<br><br>
![Image of manualSegmentation.py after loading an image.](https://github.com/kerimyalcin95/deep-learning-segmentation/raw/main/screenshots/manualSegmentation02.jpg "Screenshot of manualSegmentation.py in action")<br><br>
3. adjust thresholding output using brightness and gaussian-blur filters
4. adjust brush size and brush color with `[Black/White]`
5. invert the image with `[Invert]`
6. align both previews with `[Sync]`
7. on the right side trace image features using the brush tool<br><br>
![Image of manualSegmentation.py after tracing.](https://github.com/kerimyalcin95/deep-learning-segmentation/raw/main/screenshots/manualSegmentation03.jpg "Screenshot of manualSegmentation.py in action")<br><br>
8. save the output image for later tracing with `[Save Image]`
9. close `manualSegmentation`
   
### Create Image Reference Labels
1. start `manualSegmentation`
2. on the left side load an image with `[Load Image]`<br><br>
![Image of manualSegmentation.py after loading an image.](https://github.com/kerimyalcin95/deep-learning-segmentation/raw/main/screenshots/manualSegmentation02.jpg "Screenshot of manualSegmentation.py in action")<br><br>
3. on the right side load the corresponding image you have prepared for image label creation<br><br>
![Image of manualSegmentation.py after tracing.](https://github.com/kerimyalcin95/deep-learning-segmentation/raw/main/screenshots/manualSegmentation03.jpg "Screenshot of manualSegmentation.py in action")<br><br>
4. set image size (default: 336x336 px)
5. set image increment (default: 0) which saves each image counting upwards
6. on the right side click to save one label each (until you have about 60-80 labels; image increment adds one [increments] each time)<br><br>
![Image of manualSegmentation.py after loading an image and tracing.](https://github.com/kerimyalcin95/deep-learning-segmentation/raw/main/screenshots/manualSegmentation01.jpg "Screenshot of manualSegmentation.py in action")<br><br>
7. close `manualSegmentation`

You find the labels in `/images`, `/labels` and `/raw/labels`. The labels in `/images` and `/labels` are required to train a model. Use the labels in `/raw/labels` for your own documentation purposes.

### Train and Save a Model
### Predict an Image from a Loaded Model

## Notice
* Reading and saving image file names are not supported in Unicode due to OpenCV `imread` and `imwrite` function.
  Avoid file names containing chars like Umlaute äüö or special characters.
* Cancelling the file dialog without selecting a path can lead to termination of the app
* an internet connection is required to create the ResNet32 model
* if `semanticSegmentation` app does not respond due to threading you have to restart the application
