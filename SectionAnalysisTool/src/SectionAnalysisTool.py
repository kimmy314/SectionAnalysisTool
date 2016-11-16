"""
Section Analysis Tool GUI
"""
__author__ = 'RA029440 - Kim_Nguyen@haci.honda.com'
import sys
import os
import math
from MultiColumnListbox import MultiColumnListbox as MCL
from Rect import Rect
from Circ import Circ
from Poly import Poly
from Shape import Shape
from RectangleAnalysis import RectangleAnalysis as RA
from CircSegAnalysis import CircSegAnalysis as CSA
from SectionAnalysis import SectionAnalysis as SA
from PolygonAnalysis import PolygonAnalysis as PA
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import Canvas
from idlelib.ToolTip import ToolTip
import Pmw

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

global COLOR_VAL
global SF
global IDX_MIN_MAX
global canvas

WINDOW_WIDTH = 960
WINDOW_HEIGHT = 720

''' Main Window '''
root = tk.Tk()
root.wm_iconbitmap('icon.ico')
root.resizable(width=True, height=True)
root.geometry('{}x{}'.format(WINDOW_WIDTH, WINDOW_HEIGHT))
root.title('Section Analysis Tool')
tooltip = Pmw.Balloon(root)

frame = tk.Frame(root, width=500)
frame.pack(side=tk.LEFT, fill='y', padx=5, pady=5)

class ResizingCanvas(Canvas):
    def __init__(self,parent,**kwargs):
        Canvas.__init__(self,parent,**kwargs)
        self.bind("<Configure>", self.on_resize)
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()

    def on_resize(self,event):
        # determine the ratio of old width/height to new width/height
        wscale = float(event.width)/self.width
        hscale = float(event.height)/self.height
        self.width = event.width
        self.height = event.height
        # resize the canvas 
        self.config(width=self.width, height=self.height)
        # rescale all the objects tagged with the "all" tag
        self.scale("all",0,0,wscale,hscale)
        draw();
        
canvasFrame = tk.Frame(root)
canvasFrame.pack(fill=tk.BOTH, expand=tk.YES)
''' Canvas '''
canvas = ResizingCanvas(canvasFrame,width=460, height=720, bg="grey")
canvas.pack(fill=tk.BOTH, expand=tk.YES, padx=5, pady=5)

def add_item():
    '''
    add the text in the Entry widget to the end of the listbox
    '''
    global canvas
    info = sectionEntry.get().split(',')

    try:
        section = None
        if info[0][0] is 'R' or info[0][0] is 'r':
            if len(info) < 7:
                raise ValueError('Not enough inputs')
            section = RA(info[1], info[2], info[3],
                         info[4], info[5], info[6])
            shapes.append(Rect(section))
            listbox.addRow(info)
        elif info[0][0] is 'C' or info[0][0] is 'c':
            if len(info) < 8:
                raise ValueError('Not enough inputs')
            section = CSA(info[1], info[2], info[3],
                          info[4], info[5], info[6], info[7])
            shapes.append(Circ(section))
            listbox.addRow(info)
        elif info[0][0] is 'P' or info[0][0] is 'p':
            if len(info) < 8:
                raise ValueError('Not enough inputs')
            section = PA(info[1], info[2:])
            shapes.append(Poly(section))
            section.corners()
            listbox.addRow([info[0], info[1], '', '', '', '', '', ''])
        else:
            raise ValueError('R* or r* for rectangle,'
                             'C* or c* for circle segment,'
                             'P* or p* for polygon')
        sa.addSection(section)
        infoList.append(info)
        updateSectionResults()
        draw()
    except BaseException as e:
        messagebox.showerror("Error", repr(e))

def delete_item():
    '''
    delete a selected line from the listbox
    '''
    # get selected line index
    try:
        index = listbox.removeRow()
        index = int(index)
        sa.removeSection(index)
        del shapes[index]
        del infoList[index]
        updateSectionResults()
        draw()
    except BaseException as e:
        messagebox.showerror("Error", repr(e))

def edit_item():
    '''
    edits the selected item with the input box
    '''
    info = sectionEntry.get().split(',')
    try:
        index = listbox.index()
        sa.editSection(index, info)
        listbox.editRow(info)
        if info[0][0] is 'R' or info[0][0] is 'r':
            shapes[index] = Rect(sa.sections[index])
        elif info[0][0] is 'C' or info[0][0] is 'c':
            shapes[index] = Circ(sa.sections[index])
        elif info[0][0] is 'P' or info[0][0] is 'p':
            shapes[index] = Poly(sa.sections[index])
        else:
            raise ValueError('R* or r* for rectangle,'
                             'C* or c* for circle segment,'
                             'P* or p* for polygon')
        infoList[index] = info
        updateSectionResults()
        draw()
    except BaseException as e:
        messagebox.showerror("Error", repr(e))

def getCanvasData():
    '''
    calculates the in to pixel conversion and origin for the canvas
    '''
    minIn, maxIn, = sa.getMinMax()

    if maxIn == 0 and minIn == 0:
        inToPix = 1
        origin = [(canvas.winfo_width()) / 2, canvas.winfo_height() / 2]
    else:
        inToPix = (canvas.winfo_width() - 30) / (maxIn - minIn)
        origin = int(-minIn * inToPix) + 15
        origin = [origin, canvas.winfo_height() - origin]

    return inToPix, origin

def draw():
    global canvas
    inToPix, origin = getCanvasData()
    canvas.delete("all")
    pad = 7
    # axis
    canvas.create_line(origin[0], 0,
                       origin[0], canvas.winfo_height(),
                       fill='blue',
                       width='1')
    canvas.create_line(0, origin[1],
                       canvas.winfo_width(), origin[1],
                       fill='blue',
                       width='1')
    # arrows
    canvas.create_text(42, canvas.winfo_height() - pad, text='X', fill='yellow')
    canvas.create_line(pad, canvas.winfo_height() - pad,
                       pad, canvas.winfo_height() - 40,
                       fill='yellow',
                       width='1',
                       arrow=tk.LAST)
    canvas.create_text(pad, canvas.winfo_height() - 47, text='X', fill='yellow')
    canvas.create_line(pad, canvas.winfo_height() - pad,
                       40, canvas.winfo_height() - pad,
                       fill='yellow',
                       width='1',
                       arrow=tk.LAST)

    try:
        for shape in shapes:
            shape.draw(canvas, inToPix, origin)
        # stress fild
        for s in SF:
            x, y = Shape.inLocToPix(Shape, inToPix, origin[0], origin[1], s[0], s[1])
            item = Shape.point(Shape, canvas, x, y, s[2], COLOR_VAL[0], COLOR_VAL[1])
            tooltip.tagbind(canvas, item, ('({}, {}) : {}'
                                           .format(round(s[0], 2),
                                                   round(s[1], 2),
                                                   round(s[2], 2))))

        if not len(SF) is 0:
            minX, minY = Shape.inLocToPix(Shape, inToPix,
                                          origin[0], origin[1],
                                          SF[IDX_MIN_MAX[0]][0], SF[IDX_MIN_MAX[0]][1])
            minRect = canvas.create_rectangle(minX - 2, minY - 2, minX + 2, minY + 2,
                                              fill='yellow',
                                              outline='black')
            tooltip.tagbind(canvas, minRect, ('({}, {}) : {}'
                                              .format(round(SF[IDX_MIN_MAX[0]][0], 2),
                                                      round(SF[IDX_MIN_MAX[0]][1], 2),
                                                      round(SF[IDX_MIN_MAX[0]][2], 2))))
            maxX, maxY = Shape.inLocToPix(Shape, inToPix,
                                          origin[0], origin[1],
                                          SF[IDX_MIN_MAX[1]][0], SF[IDX_MIN_MAX[1]][1])
            maxRect = canvas.create_rectangle(maxX - 2, maxY - 2, maxX + 2, maxY + 2,
                                              fill='yellow',
                                              outline='black')
            tooltip.tagbind(canvas, maxRect, ('({}, {}) : {}'
                                              .format(round(SF[IDX_MIN_MAX[1]][0], 2),
                                                      round(SF[IDX_MIN_MAX[1]][1], 2),
                                                      round(SF[IDX_MIN_MAX[1]][2], 2))))
        for i in range(int((canvas.winfo_width() - 100) / 2)):
            Shape.point(Shape, canvas, 51 + i * 2, 6, i, 0, int((canvas.winfo_width() - 100) / 2))
            Shape.point(Shape, canvas, 51 + i * 2, 8, i, 0, int((canvas.winfo_width() - 100) / 2))
            Shape.point(Shape, canvas, 51 + i * 2, 10, i, 0, int((canvas.winfo_width() - 100) / 2))

        canvas.create_text(25, 7, text=int(COLOR_VAL[0]),
                           fill='yellow',
                           font='Helvetica 6')
        canvas.create_text(canvas.winfo_width() - 25, 7, text=int(COLOR_VAL[1]),
                           fill='yellow',
                           font='Helvetica 6')
    except BaseException as e:
        messagebox.showerror("Error", repr(e))
    # rotated axis
    rx = None
    ry = None
    try:
        theta = sa.theta
        xcg, ycg = Shape.inLocToPix(Shape, inToPix, origin[0], origin[1], sa.xcg, sa.ycg)
        rx = canvas.create_line(xcg - ycg * math.tan(theta), 0,
                                xcg + (canvas.winfo_height() - ycg) * math.tan(theta), canvas.winfo_height(),
                                fill='cyan',
                                width='1',
                                dash=(3, 4))
        ry = canvas.create_line(0, ycg + xcg * math.tan(theta),
                                canvas.winfo_width(), ycg - (canvas.winfo_width() - xcg) * math.tan(theta),
                                fill='cyan',
                                width='1',
                                dash=(3, 4))
    except BaseException as e:
        canvas.delete(rx)
        canvas.delete(ry)

def updateSectionResults():
    if len(sa.sectionArr) > 0:
        infos = [sa.getIp()[0],
                 sa.getIp()[1],
                 sa.thetaD,
                 sa.areaTot,
                 sa.xcg,
                 sa.ycg]
        for i in range(6):
            resultVar = tk.StringVar()
            resultVar.set('%.4f' %infos[i])
            resultLabels[i].configure(textvariable=resultVar, relief='flat')
    else:
        for i in range(6):
            resultVar = tk.StringVar()
            resultVar.set('{:^}'.format(''))
            resultLabels[i].configure(textvariable=resultVar, relief='flat')

def runAnalysis():
    '''
    Runs the analysis on the section
    '''
    try:
        global COLOR_VAL
        global SF
        global IDX_MIN_MAX
        sa.Pz = entryPz.get()
        sa.Mx = entryMx.get()
        sa.My = entryMy.get()
        sa.xP = entryXP.get()
        sa.yP = entryYP.get()
        updateSectionResults()
        stressVar.set('Stress: %.2f ' %sa.getStress(entryX.get(), entryY.get()))
        stressLabel.config(textvariable=stressVar, relief='flat')
        temp = sa.stressField()
        SF = temp[0]
        COLOR_VAL = [temp[1], temp[2]]
        IDX_MIN_MAX = [temp[3], temp[4]]
        draw()
    except BaseException as e:
        messagebox.showerror("Error", repr(e))

def loadFile():
    fname = filedialog.askopenfilename()
    if fname:
        try:
            with open(fname, 'r+') as f:
                for line in f:
                    sectionEntry.delete(0, tk.END)
                    sectionEntry.insert(0, line)
                    add_item()
        except BaseException as e:
            messagebox.showerror("Error", repr(e))


def saveFile():
    fname = filedialog.asksaveasfilename()
    if fname:
        try:
            with open(fname, 'w') as f:
                for info in infoList:
                    f.write(', '.join(str(x) for x in info))
        except BaseException as e:
            messagebox.showerror("Error", repr(e))

def saveStress():
    fname = filedialog.asksaveasfilename()
    if fname:
        try:
            with open(fname, 'w') as f:
                for s in SF:
                    f.write(', '.join(str(x) for x in s))
                    f.write('\n')
        except BaseException as e:
            messagebox.showerror("Error", repr(e))

def clearList():
    global SF
    global COLOR_VAL
    sa.clear()
    listbox.clear()
    del shapes[:]
    del infoList[:]
    del SF[:]
    COLOR_VAL = [0, 0]
    updateSectionResults()
    draw()

# file manager
fileFrame = tk.Frame(frame)
fileFrame.pack(side=tk.TOP, fill='x')
loadBtn = tk.Button(fileFrame, text='Load File', command=loadFile)
loadBtn.pack(side=tk.LEFT, padx=5, pady=5)
clearBtn = tk.Button(fileFrame, text='Clear List', command=clearList)
clearBtn.pack(side=tk.LEFT, padx=5, pady=5)
saveBtn = tk.Button(fileFrame, text='Save File', command=saveFile)
saveBtn.pack(side=tk.LEFT, padx=5, pady=5)

# Load labels
loadFrames = tk.Frame(frame)
loadFrames.pack(side=tk.TOP, fill='x')
labelPz = tk.Label(loadFrames, text='Pz', width=10)
labelPz.pack(side=tk.LEFT, padx=5, pady=5)
labelMx = tk.Label(loadFrames, text='Mx', width=10)
labelMx.pack(side=tk.LEFT, padx=5, pady=5)
labelMy = tk.Label(loadFrames, text='My', width=10)
labelMy.pack(side=tk.LEFT, padx=5, pady=5)
labelXP = tk.Label(loadFrames, text='xP', width=10)
labelXP.pack(side=tk.LEFT, padx=5, pady=5)
labelYP = tk.Label(loadFrames, text='yP', width=10)
labelYP.pack(side=tk.LEFT, padx=5, pady=5)
ToolTip(labelPz, 'Pz is the load in the Z direction'
                 '\nPositive Pz is out of the page')
ToolTip(labelMx, 'Mx is the moment in the X direction')
ToolTip(labelMy, 'My is the moment in the Y direction')
ToolTip(labelXP, 'Load application location')
ToolTip(labelYP, 'Load application location')

# Load entries
lEntryFrames = tk.Frame(frame)
lEntryFrames.pack(side=tk.TOP, fill='x')
entryPz = tk.Entry(lEntryFrames, width=10, bg='yellow')
entryPz.pack(side=tk.LEFT, padx=5, pady=5)
entryPz.insert(0, 0)
entryMx = tk.Entry(lEntryFrames, width=10, bg='yellow')
entryMx.pack(side=tk.LEFT, padx=5, pady=5)
entryMx.insert(0, 0)
entryMy = tk.Entry(lEntryFrames, width=10, bg='yellow')
entryMy.pack(side=tk.LEFT, padx=5, pady=5)
entryMy.insert(0, 0)
entryXP = tk.Entry(lEntryFrames, width=10, bg='yellow')
entryXP.pack(side=tk.LEFT, padx=5, pady=5)
entryXP.insert(0, 0)
entryYP = tk.Entry(lEntryFrames, width=10, bg='yellow')
entryYP.pack(side=tk.LEFT, padx=5, pady=5)
entryYP.insert(0, 0)

sectionFrame = tk.Frame(frame)
sectionFrame.pack(side=tk.TOP,fill='x')
# section list
sectionEntry = tk.Entry(sectionFrame, bg='yellow')
sectionEntry.pack(side=tk.TOP, pady=5, fill='x')
sectionEntry.insert(0, 'shape, id, x, y, dim1, dim2, orient, alpha')
ToolTip(sectionEntry, 'Sections must contain the following:'
                      '\nshape: The shape to be added'
                      '\n\tshapes can start with'
                      '\n\tR/r, C/c, or P/p'
                      '\n\tR is for Rectangle'
                      '\n\tC is for Circle Segment'
                      '\n\tP is for Polygon'
                      '\nid: the id for the section'
                      '\n\nif the shape is an R then'
                      '\nx, y, dim1, dim2 and orient must be filled'
                      '\nif the shape is an C then'
                      '\nx, y, dim1, dim2, orient and alpha must be filled'
                      '\nif the shape is a P then'
                      '\nit should be followed by x0, y0, x1, y1, etc'
                      '\n\nx: the x coordinate for the section'
                      '\n\tx for the R is the bottom left corner'
                      '\n\tx for the C is the center of the circle'
                      '\ny: the y coordinate for the section'
                      '\n\ty for the R is the bottom left corner'
                      '\n\ty for the C is the center of the circle'
                      '\ndim1: dimension 1 for the section'
                      '\n\tdim1 for the R is the length in x'
                      '\n\tdim1 for the C is the outter radius'
                      '\ndim2: dimension 2 for the section'
                      '\n\tdim2 for the R is the length in y'
                      '\n\tdim2 for the C is the inner radius'
                      '\norient: dimension 1 for the section'
                      '\n\torient for the R is the angle'
                      '\n\tbetween the x axis and base CW'
                      '\n\torient for the C is the angle'
                      '\n\tto the midpoint of the arc'
                      '\n\trelative to the center of the circle'
                      '\nalpha: the angle fo the circle section')
#buttons
buttonFrame = tk.Frame(frame);
buttonFrame.pack(side=tk.TOP,fill='x', pady=5)
button1 = tk.Button(buttonFrame, text='Add section', command=add_item)
button1.pack(side=tk.LEFT)

button2 = tk.Button(buttonFrame, text='Remove section', command=delete_item)
button2.pack(side=tk.LEFT)

button3 = tk.Button(buttonFrame, text='Edit section', command=edit_item)
button3.pack(side=tk.LEFT)

button4 = tk.Button(buttonFrame, text='Run Analysis', command=runAnalysis)
button4.pack(side=tk.LEFT)

headers = ['shape ', '  id  ', '  x   ', '  y   ', ' dim1 ', ' dim2 ', 'orient', 'alpha ']

sa = SA(0, 0, 0, 0, 0)
shapes = []
infoList = []
data = sa.sectionArr

listboxFrame = tk.Frame(frame);
listboxFrame.pack(side=tk.TOP, padx=5, pady=5, fill=tk.BOTH)
listbox = MCL(listboxFrame, headers, data, sectionEntry, infoList)
SF = []
COLOR_VAL = [0, 0]
IDX_MIN_MAX = [0, 0]

# results
bottomFrame = tk.Frame(frame)
bottomFrame.pack(side=tk.TOP, fill='x')
infoFrame = tk.Frame(bottomFrame)
infoFrame.pack(side=tk.TOP, fill='x')
nameFrame = tk.Frame(bottomFrame)
nameFrame.pack(side=tk.TOP, fill='x')
labelFrame = tk.Frame(bottomFrame)
labelFrame.pack(side=tk.TOP, fill='x')
eNameFrame = tk.Frame(bottomFrame)
eNameFrame.pack(side=tk.TOP, fill='x')
entryFrame = tk.Frame(bottomFrame)
entryFrame.pack(side=tk.TOP, fill='x')
stressFrame = tk.Frame(bottomFrame)
stressFrame.pack(side=tk.TOP, fill='x')

label1 = tk.Label(infoFrame,
                  text='Section Analysis Results',
                  font="Helvetica 16 bold")
label1.pack(side=tk.TOP)
label2 = tk.Label(infoFrame, text='MOI about the principal axis')
label2.pack(side=tk.TOP)
labelNames = ['Ixp', 'Iyp', 'Theta', 'Area', 'Xcg', 'Ycg']
sectionLabels = []
resultLabels = []
for name in labelNames:
    labelName = tk.Label(nameFrame, text=name, width=8, relief='flat')
    labelName.pack(side=tk.LEFT, padx=3)
    sectionLabels.append(labelName)

for label in labelNames:
    resultLabel = tk.Entry(labelFrame,
                           width=8,
                           state='readonly',
                           readonlybackground='white',
                           relief='flat')
    resultLabel.pack(side=tk.LEFT, padx=3)
    resultLabels.append(resultLabel)

# get stress at location x y
eNameX = tk.Label(eNameFrame, text='X coord', width=10)
eNameX.pack(side=tk.LEFT, padx=5)
eNameY = tk.Label(eNameFrame, text='Y coord', width=10)
eNameY.pack(side=tk.LEFT, padx=5)
entryX = tk.Entry(entryFrame, width=10, bg='yellow')
entryX.pack(side=tk.LEFT, padx=5)
entryX.insert(0, 0)
entryY = tk.Entry(entryFrame, width=10, bg='yellow')
entryY.pack(side=tk.LEFT, padx=5)
entryY.insert(0, 0)
stressBtn = tk.Button(entryFrame, text='Save Stress File', command=saveStress)
stressBtn.pack(side=tk.LEFT, padx=5)
stressLabel = tk.Entry(stressFrame,
                       state='readonly',
                       readonlybackground='white')
stressLabel.pack(fill='x', padx=5, pady=5)
stressVar = tk.StringVar()
stressVar.set('Stress: ')
stressLabel.config(textvariable=stressVar, relief='flat')

draw()

root.mainloop(0)
