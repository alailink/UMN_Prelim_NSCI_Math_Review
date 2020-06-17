# -*- coding: utf-8 -*-
"""
Created on Thu May 21 13:40:45 2020

@author: Clay


Notes:
Add fpr and tpr display underneath graph
AUC functionality?
"""

from tkinter import *
from random import randint
import PySimpleGUI as sg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, FigureCanvasAgg
from matplotlib.figure import Figure
from matplotlib.backends import _backend_tk
import tkinter as Tk
import random
import numpy as np
from sklearn.metrics import roc_curve
from sklearn.metrics import roc_auc_score
from matplotlib import pyplot
pyplot.style.use('dark_background')
###########
pts =  1000
###########

#Distribution
fig = Figure(figsize = (6.4*1.3,4.8*1.3))
ax = fig.add_subplot(111)
ax.set_xlabel("X axis", size=16)
ax.set_ylabel("Y axis", size=16)


#ROC Curve
fig2 = Figure(figsize = (6.4*1.3,4.8*1.3))
ax2 = fig2.add_subplot(111)
ax2.set_xlabel("FPR", size=16)
ax2.set_ylabel("TPR", size=16)

sg.theme('DarkBlue')
column1 = [[sg.Text('Distribution 1', justification='center', font='Helvetica 14')],
            [sg.Text('Mean'), sg.Spin(values=[i for i in range(10)], size=(20, 12), key='mean1', enable_events=True,initial_value=4)],
            [sg.Text('Std   '), sg.Spin(values=[i for i in range(10)], size=(20, 12), key='var1', enable_events=True,initial_value=1)]]
column2 = [[sg.Text('Distribution 2', justification='center', font='Helvetica 14')],
            [sg.Text('Mean'), sg.Spin(values=[i for i in range(10)], size=(20, 12), key='mean2', enable_events=True,initial_value=7)],
            [sg.Text('Std   '), sg.Spin(values=[i for i in range(10)], size=(20, 12), key='var2', enable_events=True,initial_value=1)]] 
column3 = [[sg.Text('TPR'), sg.Text(size=(5,1), key='-OUTPUT_TPR-')],
            [sg.Text('FPR'), sg.Text(size=(5,1), key='-OUTPUT_FPR-')],
            [sg.Text('AUC'), sg.Text(size=(5,1), key='-OUTPUT_AUC-')]]


layout = [[sg.Text('ROC Visualization', size=(40, 1), justification='center', font='Helvetica 20')],
           [sg.Canvas(size=(640*1.3, 480*1.3), background_color='black', key='canvas'), sg.Canvas(size=(640*1.3, 480*1.3), key='canvas_ROC')],
           [sg.Slider(range=(0, 99), key='slider', enable_events = True, 
                      pad=((100,0),0), default_value=5, size=(35, 20), 
                      orientation='h', font=("Helvetica", 15)),sg.Text(' ' * 2)],
           [sg.Column(column1,pad=((100,0),0)), 
            sg.Column(column2,pad=((10,0),0)),
            sg.Column(column3, pad=((150,0),0)),
            sg.Button('Exit', size=(10, 2), pad=((300, 0), 0), font='Helvetica 14')]]

# create the window and show it without the plot    


window = sg.Window('Simple GUI to envision ROC curves', layout)
window.Finalize()  # needed to access the canvas element prior to reading the window

canvas_elem = window['canvas']
graph = FigureCanvasTkAgg(fig, master=canvas_elem.TKCanvas)
canvas = canvas_elem.TKCanvas

canvas_elem2 = window['canvas_ROC']
graph2 = FigureCanvasTkAgg(fig2, master=canvas_elem2.TKCanvas)
canvas2 = canvas_elem2.TKCanvas



def ROC_curve(x,y):
    fpr = []
    tpr = []
    xnp = np.asarray(x)
    ynp = np.asarray(y)
    for i in range(0,100):
       j = i/10
       tpr.append(np.sum(xnp<j)/pts)
       fpr.append(np.sum(ynp<j)/pts)
#    z = x + y
#    z1 = [1 for i in range(1000)] + [0 for i in range(1000)]
    auc = np.trapz(tpr, x=fpr)
    return fpr, tpr, auc

mean1, mean2, var1, var2 = 4, 7, 1, 1

x = [random.gauss(mean1,var1) for _ in range(pts)]
y = [random.gauss(mean2,var2) for _ in range(pts)]
fpr, tpr, auc = ROC_curve(x,y)

bins = np.linspace(0, 10, 100)
dpts = [i/2 for i in range(20)]




def update_graph():
    slide = int(values['slider'])
    
    ax.cla()

    ax.hist(x, bins, alpha=0.5, label='x', color='pink')
    ax.hist(y, bins, alpha=0.5, label='y', color='deepskyblue')
    ax.legend(loc='upper right')
    
    ax.axvline(x=slide/10, ymin=0, ymax=20)
    graph.draw()
    
    figure_x, figure_y, figure_w, figure_h = fig.bbox.bounds
    figure_w, figure_h = int(figure_w), int(figure_h)
    photo = Tk.PhotoImage(master=canvas, width=figure_w, height=figure_h)
    canvas.image = photo
    canvas.create_image(640*1.3 / 2, 480*1.3 / 2, image=photo)
    figure_canvas_agg = FigureCanvasAgg(fig)
    figure_canvas_agg.draw()
 

    _backend_tk.blit(photo, figure_canvas_agg.get_renderer()._renderer, (0, 1, 2, 3))

    #Do it all again for the ROC curve
    ax2.cla()

    ax2.plot(fpr,tpr, linewidth=3, color='deeppink')
    ax2.plot(fpr[slide], tpr[slide], '*', color='deepskyblue', markersize=20)
    ax2.set_xlabel("FPR")
    ax2.set_ylabel("TPR")   
    graph2.draw()
    
    figure_x, figure_y, figure_w, figure_h = fig2.bbox.bounds
    figure_w, figure_h = int(figure_w), int(figure_h)
    photo = Tk.PhotoImage(master=canvas2, width=figure_w, height=figure_h)
    canvas2.image = photo
    canvas2.create_image(640*1.3 / 2, 480*1.3 / 2, image=photo)
    figure_canvas_agg2 = FigureCanvasAgg(fig2)
    figure_canvas_agg2.draw()
 

    _backend_tk.blit(photo, figure_canvas_agg2.get_renderer()._renderer, (0, 1, 2, 3))
    ##and update the output values
    window['-OUTPUT_TPR-'].update(f'{tpr[slide]:.3f}')
    window['-OUTPUT_FPR-'].update(f'{fpr[slide]:.3f}')
    window['-OUTPUT_AUC-'].update(f'{auc:.3f}')


# Our event loop      
while True:
    event, values = window.read(timeout=10)

    if event == 'Exit' or event is None:
        break
    if event == 'mean1':
        mean1 = values['mean1']
        x = [random.gauss(mean1,var1) for _ in range(pts)]
        fpr, tpr, auc = ROC_curve(x,y)
        update_graph()
    if event == 'var1':
        var1 = values['var1']
        x = [random.gauss(mean1,var1) for _ in range(pts)]
        fpr, tpr, auc = ROC_curve(x,y)
        update_graph()
    if event == 'mean2':
        mean2 = values['mean2']
        y = [random.gauss(mean2,var2) for _ in range(pts)]
        fpr, tpr, auc = ROC_curve(x,y)
        update_graph()
    if event == 'var2':
        var2 = values['var2']
        y = [random.gauss(mean2,var2) for _ in range(pts)]
        fpr, tpr, auc = ROC_curve(x,y)
        update_graph()
    if event == 'Update' or event == 'slider':
        update_graph()
        

window.close()

#
#
#pyplot.style.use('dark_background')
#
#fig, ax = pyplot.subplots()
#
#L = 6
#x = np.linspace(0, L)
#ncolors = len(pyplot.rcParams['axes.prop_cycle'])
#shift = np.linspace(0, L, ncolors, endpoint=False)
#for s in shift:
#    ax.plot(x, np.sin(x + s), 'o-')
#ax.set_xlabel('x-axis')
#ax.set_ylabel('y-axis')
#ax.set_title("'dark_background' style sheet")
#
#plt.show()