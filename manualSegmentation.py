# Script-name: Manual Segmentation
# Author: Kerim Yalcin
# Last-edit: Feb 08, 2024

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
        self.size = tkinter.StringVar()
        self.size.set('336')

        self.brightness = tkinter.StringVar()
        self.blurRadius = tkinter.StringVar()

        self.brushColorBlack = True
        self.brushRadius = tkinter.StringVar()

        self.invert = True

        self.increment = tkinter.StringVar()
        self.increment.set('0')

        self.cropEnabled = False

        # Main window config
        tkMain.title("Manual Segmentation")
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
            command=self.tkBtLoadImgBefore_loadImage_applyFiltering)
        self.tkBtSaveImgBefore = tkinter.Button(
            master=self.tkFrameLeft,
            height=1,
            width=10,
            text="Save image",
            command=self.tkBtSaveImgBefore_saveImage)
        self.tkScaleBrightnessImgBefore = tkinter.Scale(
            master=self.tkFrameLeft,
            label="Brightness",
            variable=self.brightness,
            orient=tkinter.HORIZONTAL,
            from_=-255,
            to=255,
            background='#111111',
            foreground='#DDDDDD',
            highlightbackground='#111111',
            sliderlength=16)
        self.tkScaleBlurImgBefore = tkinter.Scale(
            master=self.tkFrameLeft,
            label="Gaussian-Blur",
            variable=self.blurRadius,
            orient=tkinter.HORIZONTAL,
            from_=1,
            to=255,
            background='#111111',
            foreground='#DDDDDD',
            highlightbackground='#111111',
            sliderlength=16)

        # Right frame
        self.tkFrameRight = tkinter.Frame(
            master=tkMain,
            background='#111111',
            highlightbackground='#DDDDDD',
            highlightthickness=1)
        self.tkBtLoadImgAfter = tkinter.Button(
            master=self.tkFrameRight,
            height=1,
            width=10,
            text="Load image",
            command=self.tkBtLoadImgAfter_loadImage)
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
        self.tkBtSwitchCropImgAfter = tkinter.Button(
            master=self.tkFrameRight,
            height=1,
            width=16,
            text="Save-Crop OFF",
            background='#000000',
            foreground='#DDDDDD',
            command=self.tkBtSwitchCropImgAfter_switchImageSaveCropMode)

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

        self.tkLabelFImgSize_ImgAfter = tkinter.LabelFrame(
            master=self.tkFrameRight,
            text=" Image size ",
            background='#111111',
            foreground='#DDDDDD')
        self.tkTfImgSize_ImgAfter = tkinter.Entry(
            self.tkLabelFImgSize_ImgAfter,
            width=10,
            background='#333333',
            foreground='#FFFFFF',
            insertbackground='#DDDDDD',
            textvariable=self.size,
            validate='key')
        self.tkLabelFIncrement_ImgAfter = tkinter.LabelFrame(
            master=self.tkFrameRight,
            text=" Increment next to save ",
            background='#111111',
            foreground='#DDDDDD')
        self.tkTfImageIncrement_ImgAfter = tkinter.Entry(
            self.tkLabelFIncrement_ImgAfter,
            width=10,
            background='#333333',
            foreground='#FFFFFF',
            insertbackground='#DDDDDD',
            textvariable=self.increment,
            validate='key')

        self.appSetWidgetLayout()
        self.appSetKeybindEvents()
        self.appRegisterValidateCmd()

        self.appSetDefaultScaleValuesImgBefore()
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
        self.tkBtSaveImgBefore.grid(
            column=1, row=0, sticky='e', padx=10, pady=10)
        self.tkScaleBrightnessImgBefore.grid(
            column=0, row=2, columnspan=2, sticky='we', padx=10, pady=0)
        self.tkScaleBlurImgBefore.grid(
            column=0, row=3, columnspan=2, sticky='we', padx=10, pady=0)

        # Right frame grid layout
        self.tkFrameRight.grid(
            column=2,
            row=2,
            sticky='news',
            padx=10,
            pady=10)
        self.tkBtLoadImgAfter.grid(
            column=0, row=0, sticky='w', padx=10, pady=10)
        self.tkBtSyncImgAfter.grid(
            column=1, row=0, padx=10, pady=10)
        self.tkBtInvertImgAfter.grid(
            column=1, row=1, padx=10, pady=10)
        self.tkBtSwitchCropImgAfter.grid(
            column=1, row=2, padx=10, pady=10)

        self.tkBtSaveImgAfter.grid(
            column=2, row=0, sticky='e', padx=10, pady=10)
        self.tkLabelFImgSize_ImgAfter.grid(
            column=2, row=1, sticky='news', padx=10, pady=0)
        self.tkTfImgSize_ImgAfter.grid(
            column=1, row=1, padx=10, pady=10, sticky='w')
        self.tkLabelFIncrement_ImgAfter.grid(
            column=2, row=2, sticky='news', padx=10, pady=5)
        self.tkTfImageIncrement_ImgAfter.grid(
            column=1, row=1, padx=10, pady=10, sticky='w')

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

        self.tkScaleBrightnessImgBefore.bind(
            sequence='<ButtonRelease-1>',
            func=self.tkScaleBrightnessImgBefore_onButton1Release
        )

        self.tkScaleBlurImgBefore.bind(
            sequence='<ButtonRelease-1>',
            func=self.tkScaleBlurImgBefore_onButton1Release
        )

        self.tkCanvasAfter.bind(
            sequence='<B1-Motion>',
            func=self.tkScaleBlurImgBefore_onButton1Motion)
        self.tkCanvasAfter.bind('<1>', self.tkCanvasAfter_onButton1Click)
        self.tkCanvasAfter.bind(
            sequence='<Enter>',
            func=self.tkCanvasAfter_onMouseEnter)

    def appRegisterValidateCmd(self):
        self.tkTfImgSize_ImgAfter['validatecommand'] = (
            tkMain.register((self.tk_valTf_ImgSize)), '%P')
        self.tkTfImageIncrement_ImgAfter['validatecommand'] = (
            tkMain.register((self.tk_valTf_Increment)), '%P')

    def tkCanvasBeforeScrollVertically(self, event):
        self.tkCanvasBefore.yview_scroll(int(event.delta / -100), 'units')

    def tkCanvasBeforeScrollHorizontally(self, event):
        self.tkCanvasBefore.xview_scroll(int(event.delta / -100), 'units')

    def tkCanvasAfterScrollVertically(self, event):
        self.tkCanvasAfter.yview_scroll(int(event.delta / -100), 'units')

    def tkCanvasAfterScrollHorizontally(self, event):
        self.tkCanvasAfter.xview_scroll(int(event.delta / -100), 'units')

    def tkBtLoadImgBefore_loadImage_applyFiltering(self):
        self.appGetImageLoadPath()
        self.appSetDefaultScaleValuesImgBefore()
        self.appApplyImgFilterAndTreshold()

    def tkBtLoadImgAfter_loadImage(self):
        self.appGetImageLoadPath()

        self.cvImgAfter = cv2.cvtColor(
            cv2.imread(self.imageLoadPath),
            cv2.COLOR_BGR2GRAY)
        self.height, self.width = self.cvImgAfter.shape

        self.tkCanvasAfter.configure(
            scrollregion=(
                0, 0, self.width, self.height))

        self.pilImgAfter = PIL.ImageTk.PhotoImage(
            image=PIL.Image.fromarray(self.cvImgAfter))

        self.tkCanvasAfter.create_image(
            0, 0, image=self.pilImgAfter, anchor=tkinter.NW)

    def tkBtSaveImgBefore_saveImage(self):
        self.appGetImageSavePath()
        cv2.imwrite(self.imageSavePath, self.cvImgBefore)

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

    def tkBtSwitchCropImgAfter_switchImageSaveCropMode(self):
        if not self.cropEnabled:
            self.cropEnabled = True
            self.tkBtSwitchCropImgAfter.config(
                text='Save-Crop ON', background='#FFFF00', foreground='#111111')
        else:
            self.cropEnabled = False
            self.tkBtSwitchCropImgAfter.config(
                text='Save-Crop OFF', background='#000000', foreground='#DDDDDD')

        self.pilImgAfter = PIL.ImageTk.PhotoImage(
            image=PIL.Image.fromarray(self.cvImgAfter))
        self.tkCanvasAfter.create_image(
            0, 0, image=self.pilImgAfter, anchor=tkinter.NW)

    def appGetImageLoadPath(self):
        self.imageLoadPath = tkinter.filedialog.askopenfilename()

    def appGetImageSavePath(self):
        self.imageSavePath = tkinter.filedialog.asksaveasfilename(
            filetypes=(('PNG', '*.png'), ('JPEG', '*.jpeg'), ('All files', '*.*')), defaultextension='*.png', initialfile="image")

    def tkScaleBrightnessImgBefore_onButton1Release(self, event):
        self.appApplyImgFilterAndTreshold()

    def tkScaleBlurImgBefore_onButton1Release(self, event):
        value = int(self.blurRadius.get())

        if value % 2 == 0:
            value = value + 1

        self.blurRadius.set(str(value))
        self.tkScaleBlurImgBefore.set(value)

        self.appApplyImgFilterAndTreshold()

    def tkCanvasAfter_onMouseEnter(self, event):
        self.tkCanvasAfter.config(cursor='tcross')

    def tkCanvasAfter_onMouseLeave(self, event):
        self.tkCanvasAfter.config(cursor='arrow')

    def tkCanvasAfter_onButton1Click(self, event):

        if not self.cropEnabled:
            self.appUpdateCanvasClickCoordinates(event=event)
            self.appDrawFilledCircle(event)
        else:
            self.appUpdateCanvasClickCoordinates(event=event)
            self.appDrawCropRectangle_saveCroppedImages_incrementCounter(
                event=event)

    def tkScaleBlurImgBefore_onButton1Motion(self, event):

        if not self.cropEnabled:
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

        self.pilImgAfter = PIL.ImageTk.PhotoImage(
            image=PIL.Image.fromarray(self.cvImgAfter))

        self.tkCanvasAfter.create_image(
            0, 0, image=self.pilImgAfter, anchor=tkinter.NW)

    def appApplyImgFilterAndTreshold(self):

        cvImgHsv = cv2.cvtColor(
            src=cv2.imread(self.imageLoadPath),
            code=cv2.COLOR_BGR2HSV
        )

        h, s, v = cv2.split(cvImgHsv)

        value = numpy.int16(self.brightness.get())
        MAX = numpy.int16(255)

        if value > 0:
            v[v > (MAX - value)] = MAX
            v[(v <= (MAX - value))] = v[(v <= (MAX - value))] + value
        if value < 0:
            v[v < -value] = 0
            v[v >= -value] = v[v >= -value] + value

        cvImgHsv = cv2.merge((h, s, v))
        cvImgRGB = cv2.cvtColor(
            src=cvImgHsv,
            code=cv2.COLOR_HSV2RGB)

        cvImgGray = cv2.cvtColor(
            src=cvImgRGB,
            code=cv2.COLOR_RGB2GRAY)
        self.height, self.width = cvImgGray.shape

        self.tkCanvasBefore.configure(
            scrollregion=(0, 0, self.width, self.height))
        self.tkCanvasAfter.configure(
            scrollregion=(
                0, 0, self.width, self.height))

        self.cvImgBefore = cv2.GaussianBlur(
            cvImgGray,
            (numpy.uint16(self.blurRadius.get()),
             numpy.uint16(self.blurRadius.get())),
            0)

        # Otsu binarization
        if self.invert:
            cvRet, self.cvImgAfter = cv2.threshold(
                self.cvImgBefore, 255, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        else:
            cvRet, self.cvImgAfter = cv2.threshold(
                self.cvImgBefore, 255, 255, cv2.THRESH_OTSU)

        self.pilImgBefore = PIL.ImageTk.PhotoImage(
            image=PIL.Image.fromarray(self.cvImgBefore))
        self.pilImgAfter = PIL.ImageTk.PhotoImage(
            image=PIL.Image.fromarray(self.cvImgAfter))

        self.tkCanvasBefore.create_image(
            0, 0, image=self.pilImgBefore, anchor=tkinter.NW)
        self.tkCanvasAfter.create_image(
            0, 0, image=self.pilImgAfter, anchor=tkinter.NW)

    def appSetDefaultScaleValuesImgBefore(self):
        self.tkScaleBrightnessImgBefore.set(0)
        self.tkScaleBlurImgBefore.set(1)

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
                thickness=-1,
                lineType=-1,
                shift=0
            )
        else:
            cv2.circle(
                img=self.cvImgAfter,
                center=(int(self.canvasAfter_x), int(self.canvasAfter_y)),
                radius=numpy.uint8(self.brushRadius.get()),
                color=(255, 255, 255),
                thickness=-1,
                lineType=-1,
                shift=0
            )

        self.pilImgAfter = PIL.ImageTk.PhotoImage(
            image=PIL.Image.fromarray(self.cvImgAfter))

        self.tkCanvasAfter.create_image(
            0, 0, image=self.pilImgAfter, anchor=tkinter.NW)

    def appDrawCropRectangle_saveCroppedImages_incrementCounter(self, event):

        size = int(self.size.get())

        rectStartx = int(self.canvasAfter_x - size / 2)
        rectStarty = int(self.canvasAfter_y - size / 2)
        rectEndx = int(self.canvasAfter_x + size / 2)
        rectEndy = int(self.canvasAfter_y + size / 2)

        if rectStartx <= 0:
            rectStartx = 0
            rectEndx = size

        if rectStarty <= 0:
            rectStarty = 0
            rectEndy = size

        if rectEndx >= self.width:
            rectEndx = self.width
            rectStartx = self.width - size

        if rectEndy >= self.height:
            rectEndy = self.height
            rectStarty = self.height - size

        cvImgAfterOverlay = cv2.cvtColor(self.cvImgAfter, cv2.COLOR_GRAY2RGB)

        cv2.rectangle(cvImgAfterOverlay,
                      (rectStartx, rectStarty),
                      (rectEndx, rectEndy),
                      color=((255, 255, 0)),
                      thickness=2,
                      shift=0,
                      lineType=cv2.LINE_4)

        self.pilImgAfter = PIL.ImageTk.PhotoImage(
            image=PIL.Image.fromarray(cvImgAfterOverlay))

        self.tkCanvasAfter.create_image(
            0, 0, image=self.pilImgAfter, anchor=tkinter.NW)

        cvImgBeforeCropped = self.cvImgBefore[rectStarty:rectEndy,
                                              rectStartx:rectEndx]
        cvImgAfterCropped = self.cvImgAfter[rectStarty:rectEndy,
                                            rectStartx:rectEndx]

        cv2.imwrite('images/' +
                    self.increment.get() +
                    '.png', cvImgBeforeCropped)
        cv2.imwrite('raw/labels/' +
                    self.increment.get() +
                    '_A.png', cvImgBeforeCropped)
        cv2.imwrite('raw/labels/' +
                    self.increment.get() +
                    '_B.png', cvImgAfterCropped)
        
        cvImgAfterCropped[cvImgAfterCropped == 255] = 1

        cv2.imwrite('labels/' +
                    self.increment.get() +
                    '_P.png', cvImgAfterCropped)
        
        cvImgAfterCropped[cvImgAfterCropped == 1] = 255

        self.increment.set(str(int(self.increment.get()) + 1))

    def tk_valTf_Increment(self, P):
        if str.isdigit(P) or P == '':
            return True
        else:
            return False

    def tk_valTf_ImgSize(self, P):

        if str.isdigit(P) or P == '':
            return True
        else:
            return False


tkMain = tkinter.Tk()
TkApp(tkMain)
tkMain.mainloop()
