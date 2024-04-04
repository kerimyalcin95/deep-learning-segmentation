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
Use it for various segmentation task. Features include image label creation, ResNet34 neural network model (arch) training and image prediction.

Based on the bachelor-thesis "Microstructure analysis of materials with the assistance of artificial technology" by Kerim Yalcin on February 2024.

Usage examples:
* metallographic image segmentation 
* medical image segmentation (tumor detection, organ detection)
* object detection
* road segmentation
* crop yield detection in agriculture
* microscopy image analysis

Features:
* read and save image files
* use filters to change brightness and gaussian-blur amount of loaded images
* apply binarization and tresholding
* invert image output
* trace desired image features using resizable brush tool in black or white
* create image labels for a model (max. 2 classifications)
* create and train a model by using the labels
* predict images with a model

Implemented packages
* `tkinter` - integrated GUI library in Python
* `PIL` - image processing library
* `OpenCV` - computer vision library
* `fastai v2` - deep learning library
* `numpy` - library for arrays and matrices
* `threading` - integrated threading library in Python

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
6. turn on image crop mode using `[Save-Crop ON/Save-Crop OFF]`
7. on the right side click to save one label each (until you have about 60-80 labels; image increment adds one [increments] each time)<br><br>
![Image of manualSegmentation.py after loading an image and tracing.](https://github.com/kerimyalcin95/deep-learning-segmentation/raw/main/screenshots/manualSegmentation01.jpg "Screenshot of manualSegmentation.py in action")<br><br>
8. close `manualSegmentation`

You find the labels in `/images`, `/labels` and `/raw/labels`. The labels in `/images` and `/labels` are required to train a model. Use the labels in `/raw/labels` for your own documentation purposes.

### Train and Save a Model
1. start `semanticSegmentation` (this may take a while depending on how fast your setup is)
2. set to TRAIN mode with `[TRAIN mode/PREDICT mode]`
3. set the path and name of the model with `[Save path]`
4. start model training with `[TRAIN]` (this can take at least 10 min or more)
5. close `semanticSegmentation`

Console output while training should be something like:
```
-- Starting thread
-- Running TRAIN mode
-- Home path: .
epoch     train_loss  valid_loss  time
0         0.729087    0.415635    01:34
epoch     train_loss  valid_loss  time
Epoch 1/6 : |███████-----------------------------------------------------| 12.50% [1/8 00:10<01:14]
```

### Predict an Image From a Loaded Model
1. start `semanticSegmentation` (this may take a while depending on how fast your setup is)
2. on the left side load an image which you want to predict using `[Load Image]`<br><br>
![Image of semanticSegmentation.py after loading an image](https://github.com/kerimyalcin95/deep-learning-segmentation/raw/main/screenshots/semanticSegmentation02.jpg "Screenshot of semanticSegmentation.py in action")<br><br>
3. set to PREDICT mode with `[TRAIN mode/PREDICT mode]`
4. load the model with `[Load path]`
5. start model prediction with `[PREDICT]` (this can take at least 1 min or more)<br><br>
![Image of semanticSegmentation.py after image prediction](https://github.com/kerimyalcin95/deep-learning-segmentation/raw/main/screenshots/semanticSegmentation03.jpg "Screenshot of semanticSegmentation.py in action")<br><br>
6. on the right side save the predicted image using `[Save image]`
7. close `semanticSegmentation`

Console output after prediction should be something like:
```
-- Starting thread
-- Running PREDICT mode
-- Try to load model at: C:/Users/path/to/your/model/your_trained_model.pkl
fastai\learner.py:59: UserWarning: Saved file doesn't contain an optimizer state.
  elif with_opt: warn("Saved file doesn't contain an optimizer state.")
-- Thread finished
```

## Notice
* Reading and saving image file names are not supported in Unicode due to OpenCV `imread` and `imwrite` function.
  Avoid file names containing chars like Umlaute äüö or special characters.
* Cancelling the file dialog without selecting a path can lead to termination of the app
* an internet connection is required to create the ResNet32 model
* if `semanticSegmentation` app does not respond due to threading you have to restart the application
