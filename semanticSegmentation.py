# Script-name: Semantic Segmentation
# Author: Kerim Yalcin
# Last-edit: Feb 08, 2024

import fastai.vision.all as fastai_vision
import threading
import tkinter
import tkinter.filedialog
import tkinter.messagebox
import cv2
import PIL.Image
import PIL.ImageTk
import numpy
import os


class TkApp:

    def __init__(self, tkMain):

        abspath = os.path.abspath(__file__)
        dname = os.path.dirname(abspath)
        os.chdir(dname)

        self.width = 0
        self.height = 0
        self.lock = False
        self.task = threading.Thread(target=self.appThreadTrain)
        self.path = fastai_vision.Path('.')
        self.modelPath = 'model/resnet32_336x336_defaultMaterial.pkl'
        self.trainingMode = True

        self.brushColorBlack = True
        self.brushRadius = tkinter.StringVar()

        self.invert = True

        self.aiLearner = 0

        # Main window config
        tkMain.title("Semantic Segmentation")
        tkMain.geometry("1600x900")
        tkMain.minsize(900, 600)
        tkMain.state('zoomed')
        tkMain.configure(background='#111111')

        # Canvas scrollbars
        self.tkSbCanvasBefore_h = tkinter.Scrollbar(
            tkMain, orient=tkinter.HORIZONTAL)
        self.tkSbCanvasBefore_v = tkinter.Scrollbar(
            master=tkMain, orient=tkinter.VERTICAL)
        self.tkSbCanvasAfter_h = tkinter.Scrollbar(
            tkMain, orient=tkinter.HORIZONTAL)
        self.tkSbCanvasAfter_v = tkinter.Scrollbar(
            master=tkMain, orient=tkinter.VERTICAL)

        # Canvas image-before
        self.tkCanvasBefore = tkinter.Canvas(
            tkMain,
            scrollregion=(
                0,
                0,
                self.width,
                self.height),
            background='#111111',
            yscrollcommand=self.tkSbCanvasBefore_v.set,
            xscrollcommand=self.tkSbCanvasBefore_h.set)
        self.tkSbCanvasBefore_h['command'] = self.tkCanvasBefore.xview
        self.tkSbCanvasBefore_v['command'] = self.tkCanvasBefore.yview

        # Canvas image-after
        self.tkCanvasAfter = tkinter.Canvas(
            tkMain,
            scrollregion=(
                0,
                0,
                self.width,
                self.height),
            background='#111111',
            yscrollcommand=self.tkSbCanvasAfter_v.set,
            xscrollcommand=self.tkSbCanvasAfter_h.set)
        self.tkSbCanvasAfter_h['command'] = self.tkCanvasAfter.xview
        self.tkSbCanvasAfter_v['command'] = self.tkCanvasAfter.yview

        # Left frame
        self.tkFrameLeft = tkinter.Frame(
            tkMain,
            background='#111111',
            highlightbackground='#DDDDDD',
            highlightthickness=1,
            height=200)
        self.tkFrameLeft.grid_propagate(False)
        self.tkBtLoadImgBefore = tkinter.Button(
            master=self.tkFrameLeft,
            height=1,
            width=10,
            text="Load image",
            command=self.tkBtLoadImgBefore_loadImage)
        self.tkBtModelSessionImgBefore = tkinter.Button(
            master=self.tkFrameLeft,
            height=1,
            width=10,
            text="TRAIN",
            command=self.tkBtModelSessionImgBefore_runModelSession)

        self.tkLabelFModelSetupImgBefore = tkinter.LabelFrame(
            master=self.tkFrameLeft,
            text=" Model/Arch setup ",
            background='#111111',
            foreground='#DDDDDD')
        self.tkBtSetModelImgBefore = tkinter.Button(
            master=self.tkLabelFModelSetupImgBefore,
            height=1,
            width=10,
            text="Save path",
            command=self.tkBtSetModelImgBefore_setModelPath)
        self.tkBtSwitchModelModeImgBefore = tkinter.Button(
            master=self.tkLabelFModelSetupImgBefore,
            height=1,
            width=14,
            text="TRAIN Mode",
            background='#f6781d',
            command=self.tkBtSwitchModelModeImgBefore_switchModelMode)

        # Right frame
        self.tkFrameRight = tkinter.Frame(
            master=tkMain,
            background='#111111',
            highlightbackground='#DDDDDD',
            highlightthickness=1)
        self.tkBtSyncImgAfter = tkinter.Button(
            master=self.tkFrameRight,
            height=1,
            width=10,
            text="Sync",
            command=self.tkBtSyncImgAfter_syncCanvas)
        self.tkBtInvertImgAfter = tkinter.Button(
            master=self.tkFrameRight,
            height=1,
            width=10,
            text="Invert",
            background='#000000',
            foreground='#DDDDDD',
            command=self.tkBtInvertImgAfter_invertAfterImage)
        self.tkBtSaveImgAfter = tkinter.Button(
            master=self.tkFrameRight,
            height=1,
            width=10,
            text="Save image",
            command=self.tkBtSaveImgAfter_saveImage)

        self.tkBtSwitchBlackWhiteBrush = tkinter.Button(
            master=self.tkFrameRight,
            height=1,
            width=10,
            text="Black",
            background='#000000',
            foreground='#DDDDDD',
            command=self.tkBtSwitchBlackWhiteBrush_switchColorBrush)
        self.tkScaleBrushRadiusImgAfter = tkinter.Scale(
            master=self.tkFrameRight,
            label="Brush-Radius",
            variable=self.brushRadius,
            orient=tkinter.HORIZONTAL,
            from_=1,
            to=50,
            background='#111111',
            foreground='#DDDDDD',
            highlightbackground='#111111',
            sliderlength=16)

        self.appSetWidgetLayout()
        self.appSetKeybindEvents()

        self.appSetDefaultScaleValuesImgAfter()

    def appSetWidgetLayout(self):
        self.tkCanvasBefore.grid(column=0, row=0, sticky='news')
        self.tkSbCanvasBefore_h.grid(column=0, row=1, sticky='we')
        self.tkSbCanvasBefore_v.grid(column=1, row=0, sticky='ns')

        self.tkCanvasAfter.grid(column=2, row=0, sticky='news')
        self.tkSbCanvasAfter_h.grid(column=2, row=1, sticky='we')
        self.tkSbCanvasAfter_v.grid(column=3, row=0, sticky='ns')

        # Left frame grid layout
        self.tkFrameLeft.grid(
            column=0,
            row=2,
            sticky='news',
            padx=10,
            pady=10)
        self.tkBtLoadImgBefore.grid(
            column=0, row=0, sticky='w', padx=10, pady=10)
        self.tkBtModelSessionImgBefore.grid(
            column=2, row=0, padx=10, pady=10, sticky='e')

        self.tkLabelFModelSetupImgBefore.grid(
            column=0, columnspan=3, row=1, sticky='we', padx=10, pady=10)
        self.tkBtSwitchModelModeImgBefore.grid(
            column=0, row=0, sticky='w', padx=10, pady=10)
        self.tkBtSetModelImgBefore.grid(
            column=1, row=0, sticky='w', padx=10, pady=10)

        # Right frame grid layout
        self.tkFrameRight.grid(
            column=2,
            row=2,
            sticky='news',
            padx=10,
            pady=10)
        self.tkBtSyncImgAfter.grid(
            column=1, row=0, padx=10, pady=10)
        self.tkBtInvertImgAfter.grid(
            column=1, row=1, padx=10, pady=10)
        self.tkBtSaveImgAfter.grid(
            column=2, row=0, sticky='e', padx=10, pady=10)

        self.tkBtSwitchBlackWhiteBrush.grid(
            column=0, row=1, sticky='w', padx=10, pady=10)
        self.tkScaleBrushRadiusImgAfter.grid(
            column=0, row=2, sticky='we', padx=10, pady=0
        )

        # Grid row/column weight configuration
        tkMain.grid_rowconfigure(0, weight=1)
        tkMain.grid_columnconfigure(0, weight=1)
        tkMain.grid_columnconfigure(2, weight=1)

        self.tkFrameLeft.grid_columnconfigure(0, weight=1)
        self.tkFrameLeft.grid_columnconfigure(1, weight=1)
        self.tkFrameLeft.grid_columnconfigure(2, weight=1)
        self.tkFrameRight.grid_columnconfigure(0, weight=1)
        self.tkFrameRight.grid_columnconfigure(1, weight=1)
        self.tkFrameRight.grid_columnconfigure(2, weight=1)

    def appSetKeybindEvents(self):

        # Vertical and horizontal scrolling
        self.tkCanvasBefore.bind(
            '<MouseWheel>',
            self.tkCanvasBeforeScrollVertically)
        self.tkCanvasBefore.bind(
            '<Shift-MouseWheel>',
            self.tkCanvasBeforeScrollHorizontally)
        self.tkCanvasAfter.bind(
            '<MouseWheel>',
            self.tkCanvasAfterScrollVertically)
        self.tkCanvasAfter.bind(
            '<Shift-MouseWheel>',
            self.tkCanvasAfterScrollHorizontally)

        self.tkCanvasAfter.bind(
            sequence='<B1-Motion>',
            func=self.tkScaleBlurImgBefore_onButton1Motion)
        self.tkCanvasAfter.bind('<1>', self.tkCanvasAfter_onButton1Click)
        self.tkCanvasAfter.bind(
            sequence='<Enter>',
            func=self.tkCanvasAfter_onMouseEnter)

    def tkCanvasBeforeScrollVertically(self, event):
        self.tkCanvasBefore.yview_scroll(int(event.delta / -100), 'units')

    def tkCanvasBeforeScrollHorizontally(self, event):
        self.tkCanvasBefore.xview_scroll(int(event.delta / -100), 'units')

    def tkCanvasAfterScrollVertically(self, event):
        self.tkCanvasAfter.yview_scroll(int(event.delta / -100), 'units')

    def tkCanvasAfterScrollHorizontally(self, event):
        self.tkCanvasAfter.xview_scroll(int(event.delta / -100), 'units')

    def tkBtLoadImgBefore_loadImage(self):
        self.appGetImageLoadPath()

        self.cvImgBefore = cv2.cvtColor(
            cv2.imread(self.imageLoadPath),
            cv2.COLOR_BGR2RGB)
        self.height, self.width, _ = self.cvImgBefore.shape

        self.tkCanvasBefore.configure(
            scrollregion=(
                0, 0, self.width, self.height))
        self.tkCanvasAfter.configure(
            scrollregion=(
                0, 0, self.width, self.height))

        self.pilTkImgBefore = PIL.ImageTk.PhotoImage(
            image=PIL.Image.fromarray(self.cvImgBefore))

        self.tkCanvasBefore.create_image(
            0, 0, image=self.pilTkImgBefore, anchor=tkinter.NW)

    def tkBtSaveImgAfter_saveImage(self):
        self.appGetImageSavePath()
        cv2.imwrite(self.imageSavePath, self.cvImgAfter)

    def tkBtSyncImgAfter_syncCanvas(self):
        top, _ = self.tkCanvasAfter.xview()
        self.tkCanvasBefore.xview_moveto(top)
        top, _ = self.tkCanvasAfter.yview()
        self.tkCanvasBefore.yview_moveto(top)

    def tkScaleBrightnessImgBefore_onChanged(self, event):
        self.appApplyImgFilterAndTreshold()

    def tkBtSwitchBlackWhiteBrush_switchColorBrush(self):
        if self.brushColorBlack:
            self.brushColorBlack = False
            self.tkBtSwitchBlackWhiteBrush.config(
                text='White', background='#FFFFFF', foreground='#111111')
        else:
            self.brushColorBlack = True
            self.tkBtSwitchBlackWhiteBrush.config(
                text='Black', background='#000000', foreground='#DDDDDD')

    def tkBtSetModelImgBefore_setModelPath(self):
        if self.trainingMode:
            self.modelPath = tkinter.filedialog.asksaveasfilename(
                filetypes=(('PKL', '*.pkl'), ('All files', '*.*')), defaultextension='*.pkl', initialfile="resnet32_336x336_defaultMaterial.pkl")
        else:
            self.modelPath = tkinter.filedialog.askopenfilename(
                filetypes=(('PKL', '*.pkl'), ('All files', '*.*')), defaultextension='*.pkl', initialfile="resnet32_336x336_defaultMaterial.pkl")

    def appGetImageLoadPath(self):
        self.imageLoadPath = tkinter.filedialog.askopenfilename()

    def appGetImageSavePath(self):
        self.imageSavePath = tkinter.filedialog.asksaveasfilename(
            filetypes=(('PNG', '*.png'), ('JPEG', '*.jpeg'), ('All files', '*.*')), defaultextension='*.png', initialfile="image")

    def tkCanvasAfter_onMouseEnter(self, event):
        self.tkCanvasAfter.config(cursor='tcross')

    def tkCanvasAfter_onMouseLeave(self, event):
        self.tkCanvasAfter.config(cursor='arrow')

    def tkCanvasAfter_onButton1Click(self, event):
        self.appUpdateCanvasClickCoordinates(event=event)
        self.appDrawFilledCircle(event)

    def tkScaleBlurImgBefore_onButton1Motion(self, event):
        self.appUpdateCanvasClickCoordinates(event=event)
        self.appDrawFilledCircle(event)

    def tkBtInvertImgAfter_invertAfterImage(self):
        if self.invert:
            self.invert = False
            self.tkBtInvertImgAfter.config(
                background='#FFFFFF', foreground='#111111')
        else:
            self.invert = True
            self.tkBtInvertImgAfter.config(
                background='#000000', foreground='#DDDDDD')

        self.cvImgAfter = cv2.bitwise_not(self.cvImgAfter)

        self.pilTkImgAfter = PIL.ImageTk.PhotoImage(
            image=PIL.Image.fromarray(self.cvImgAfter))

        self.tkCanvasAfter.create_image(
            0, 0, image=self.pilTkImgAfter, anchor=tkinter.NW)

    def tkBtSwitchModelModeImgBefore_switchModelMode(self):
        if self.trainingMode:
            self.trainingMode = False
            self.tkBtSwitchModelModeImgBefore.config(
                text='PREDICT mode', background='#7dabfb')
            self.tkBtModelSessionImgBefore.config(text='PREDICT')
            self.tkBtSetModelImgBefore.config(text='Load path')
        else:
            self.trainingMode = True
            self.tkBtSwitchModelModeImgBefore.config(
                text='TRAIN mode', background='#f6781d')
            self.tkBtModelSessionImgBefore.config(text='TRAIN')
            self.tkBtSetModelImgBefore.config(text='Save path')

    def tkBtModelSessionImgBefore_runModelSession(self):
        self.appTrain()

    def appSetDefaultScaleValuesImgAfter(self):
        self.tkScaleBrushRadiusImgAfter.set(3)

    def appUpdateCanvasClickCoordinates(self, event):
        self.canvasAfter_x = event.widget.canvasx(event.x)
        self.canvasAfter_y = event.widget.canvasy(event.y)

    def appDrawFilledCircle(self, event):

        if self.brushColorBlack:
            cv2.circle(
                img=self.cvImgAfter,
                center=(int(self.canvasAfter_x), int(self.canvasAfter_y)),
                radius=numpy.uint8(self.brushRadius.get()),
                color=(0, 0, 0),
                thickness=0,
                lineType=-1,
                shift=0
            )
        else:
            cv2.circle(
                img=self.cvImgAfter,
                center=(int(self.canvasAfter_x), int(self.canvasAfter_y)),
                radius=numpy.uint8(self.brushRadius.get()),
                color=(255, 255, 255),
                thickness=0,
                lineType=-1,
                shift=0
            )

        self.pilTkImgAfter = PIL.ImageTk.PhotoImage(
            image=PIL.Image.fromarray(self.cvImgAfter))

        self.tkCanvasAfter.create_image(
            0, 0, image=self.pilTkImgAfter, anchor=tkinter.NW)

    def appTrain(self):
        if self.lock == True:
            print('-- Cannot start another thread: Already running.')
        else:
            print('-- Starting thread')
            self.task.start()

    def appThreadTrain(self):

        def label_func(fn):
            return self.path / "labels" / f"{fn.stem}_P{fn.suffix}"

        codes = numpy.loadtxt(self.path / 'codes.txt', dtype=str)
        fnames = fastai_vision.get_image_files(self.path / 'images')
        dls = fastai_vision.SegmentationDataLoaders.from_label_func(
            self.path, bs=8, fnames=fnames, label_func=label_func, codes=codes, num_workers=0)
        self.aiLearner = fastai_vision.unet_learner(
            dls, fastai_vision.resnet34)

        if self.trainingMode:
            print('-- Running TRAIN mode')
            print('-- Home path: ' + str(self.path))

            self.aiLearner.fine_tune(6)

            print('-- Try to save model at: ' + self.modelPath)
            fastai_vision.save_model(
                file=self.modelPath,
                model=self.aiLearner,
                with_opt=False,
                opt=None)
        else:
            print('-- Running PREDICT mode')
            print('-- Try to load model at: ' + self.modelPath)
            fastai_vision.load_model(self.modelPath, self.aiLearner, opt=None)
            pilImgBefore = PIL.ImageTk.getimage(self.pilTkImgBefore)
            pilImgBefore = pilImgBefore.convert('RGB')

            self.cvImgAfter = numpy.array(
                self.aiLearner.predict(pilImgBefore)[0]).astype(
                numpy.uint8)

            self.cvImgAfter[self.cvImgAfter == 1] = 255

            cv2.cvtColor(self.cvImgAfter, cv2.COLOR_GRAY2RGB)

            self.pilTkImgAfter = PIL.ImageTk.PhotoImage(
                image=PIL.Image.fromarray(self.cvImgAfter))
            self.tkCanvasAfter.create_image(
                0, 0, image=self.pilTkImgAfter, anchor=tkinter.NW)

        print('-- Thread finished')
        self.task = threading.Thread(target=self.appThreadTrain)
        self.lock = False


tkMain = tkinter.Tk()
TkApp(tkMain)
tkMain.mainloop()
