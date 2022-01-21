import PySimpleGUI as sg
import numpy as np
import random as rnd
import matplotlib.pyplot as plt
from webbrowser import open as op
from collections import Counter
import methods
import chronos
import layouts
import _helper_code.Progress_Bar as cpb
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

dT = chronos.current_date()

# VARS CONSTS:
AppFont = 'Any 16'
_VARS = {'window': False, 'fig_agg': False, 'pi_agg': False, 'pltFig': False,
            'pltPi': False, 'win2': False, 'winWarn': False, 'winFirst': False, 'winRename': False, 'winHelp': False}
AppIcon =  "Files/_icons/HER_logo_trans.ico"

def makeSynthData():
    xData = np.array(["D%s"%(i) for i in range(1,int(methods.get_true())+1)])
    yData = np.array(methods.get_points())
    return (xData, yData)

def fixOverLappingText(text):

    # if undetected overlaps reduce sigFigures to 1
    sigFigures = 2
    positions = [(round(item.get_position()[1],sigFigures), item) for item in text]

    overLapping = Counter((item[0] for item in positions))
    overLapping = [key for key, value in overLapping.items() if value >= 2]

    for key in overLapping:
        textObjects = [text for position, text in positions if position == key]

        if textObjects:

            # If bigger font size scale will need increasing
            scale = 0.07 #Original=0.05

            spacings = np.linspace(0,scale*len(textObjects),len(textObjects))

            for shift, textObject in zip(spacings,textObjects):
                textObject.set_y(key + shift)

def drawpichart(mode = "default"):
    if mode == "default":
        _VARS['pltPi'] = plt.figure(figsize=(4.25, 3.25))
        per = methods.generate_per_pi()
        y = per.values() 
        labels = per.keys()
        explode = [0]*7
        idx = np.argmax(list(y))
        explode[idx]=0.1
        plt.axis("equal")
        plot = plt.pie(y, autopct="%1.1f%%", labels = labels, explode = explode, shadow = True)[1]
        fixOverLappingText(plot)
        plt.legend(loc="best")
        plt.title("Trips by Weekdays")
        _VARS['pi_agg'] = draw_figure(
            _VARS['window']['figCanvasPi'].TKCanvas, _VARS['pltPi'])
    if mode == "noTrip":
        _VARS['pltPi'] = plt.figure(figsize=(4.25, 3.25))
        N = 30
        y = [1]*N
        rand_colors = []
        for _ in range(N):
            color = ["#"+''.join([rnd.choice('ABCDEF0123456789') for _ in range(6)])]
            rand_colors.append(color[0])
        plt.axis("equal")
        plot = plt.pie(y, colors = rand_colors)
        plt.title("No Trips yet! Cool!")
        _VARS['pi_agg'] = draw_figure(
            _VARS['window']['figCanvasPi'].TKCanvas, _VARS['pltPi'])

def drawChart():
    _VARS['pltFig'] = plt.figure(figsize=(6, 4.25))
    dataXY = makeSynthData()
    green = []
    red = []
    
    green = np.split(dataXY[1], np.where(np.diff(dataXY[1]) < 0)[0] + 1)
    bases = np.split(dataXY[0], np.where(np.diff(dataXY[1]) < 0)[0] + 1)
    red_alpha = np.split(dataXY[1], np.where(np.diff(dataXY[1]) > 0)[0] + 1)
    rb_alpha = np.split(dataXY[0], np.where(np.diff(dataXY[1]) > 0)[0] + 1)
    red = []
    rb = []
    for list1, list2 in zip(red_alpha, rb_alpha):
        if (len(list1)>1):
            red.append([list1[-1:][0], list1[-2:][0]]) #Pick last Two elements
            rb.append([list2[-1:][0], list2[-2:][0]])

    for i in range(len(green)):
        plt.plot(bases[i], green[i], "g-")

    for i in range(len(red)):
        plt.plot(rb[i], red[i], "r-")

    plt.axhline(y=90, color='darkorchid', linestyle='--')
    # plt.colorbar()
    plt.xlabel("Days Passed")
    plt.ylabel("Success Percentage")
    plt.title("Success Over Time")
    divider = len(dataXY[0])/5
    plt.xticks(range(0,len(dataXY[0]),int(divider)))  #displays x-axis in intervals of four - six
    _VARS['fig_agg'] = draw_figure(
        _VARS['window']['figCanvas'].TKCanvas, _VARS['pltFig'])

def updateChart():
    _VARS['fig_agg'].get_tk_widget().forget()
    dataXY = makeSynthData()

    green = []
    red = []
    
    green = np.split(dataXY[1], np.where(np.diff(dataXY[1]) < 0)[0] + 1)
    bases = np.split(dataXY[0], np.where(np.diff(dataXY[1]) < 0)[0] + 1)
    red_alpha = np.split(dataXY[1], np.where(np.diff(dataXY[1]) > 0)[0] + 1)
    rb_alpha = np.split(dataXY[0], np.where(np.diff(dataXY[1]) > 0)[0] + 1)
    
   # plt.plot(dataXY[0], dataXY[1], "b-")
    red = []
    rb = []
    for list1, list2 in zip(red_alpha, rb_alpha):
        if (len(list1)>1):
            red.append([list1[-1:][0], list1[-2:][0]]) #Pick last Two elements
            rb.append([list2[-1:][0], list2[-2:][0]])

    for i in range(len(green)):
        plt.plot(bases[i], green[i], "g-")

    for i in range(len(red)):
        plt.plot(rb[i], red[i], "r-")

    plt.axhline(y=90, color='darkorchid', linestyle='--')
    # plt.colorbar()
    plt.xlabel("Days Passed")
    plt.ylabel("Success Percentage")
    plt.xticks(range(0,len(dataXY[0]),5))  #displays x-axis in intervals of five
    _VARS['fig_agg'] = draw_figure(
        _VARS['window']['figCanvas'].TKCanvas, _VARS['pltFig'])

#FIGURE GENERATOR
def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

#######################################################################################################
lay_ob = layouts.layouts()      #Generate Layout Object
#MAIN:
if methods.notnew_user():
    #UPDATES PARAMETERS FOR THE Project    
    chronos.sync_time(methods.get_head())
    methods.update_success()
    methods.checkin()
    true = int(methods.get_true())

    if true > 4:
        #LAUNCH REGULAR WINDOW
        keyo = lay_ob.gen_tab_lay()
        tb =True
        _VARS['window'] = sg.Window("HER", lay_ob.tabular_lay,
                                 finalize=True,
                                 resizable=True,
                                 location=(100,50),
                                 element_justification="left", icon = AppIcon)
        _VARS['window'].Maximize()
        #_VARS['window'].Element("_TAB2_").Select()
        drawChart()
        if int(methods.get_fails()) == 0:
            drawpichart("noTrip")
        else:
            drawpichart()
        graph = _VARS['window']['Graph']

        filename = "Files/_py_code/_helper_code/arc_png.dat"
        progress_bar = cpb.Progress_Bar(graph, filename)
        progress_bar.set_target((methods.since_lasttrip()/methods.gen_goal())*360)
    else:
            _VARS['window'] = sg.Window("HER", lay_ob.alpha_layout(),
                            finalize=True,
                            resizable=True,
                            location=(100,50),
                            element_justification="center", icon = AppIcon)
            graph = _VARS['window']['Graph']

            filename = "Files/_py_code/_helper_code/arc_png.dat"
            progress_bar = cpb.Progress_Bar(graph, filename)
            progress_bar.set_target((true/4)*360)
else:
    _VARS['winFirst'] = sg.Window("HER", lay_ob.first_layout(),
                            finalize=True,
                            resizable=True,
                            location=(550,250),
                            element_justification="center", icon = AppIcon)
    while True:
        event, values = _VARS["winFirst"].read()
        if event == "EXIT" or event == sg.WIN_CLOSED:
            break
        if event == "START":
            methods.prepare_new_profile()  ###NEEDS WORK
            break
        if event == "CONT. HABIT":         ###NEEDS WORK
            break
    _VARS["winFirst"].close()
    
    #sg.theme('LightGrey1')
    _VARS['window'] = sg.Window("HER", lay_ob.alpha_layout(),
                            finalize=True,
                            resizable=True,
                            location=(100,50),
                            element_justification="center", icon = AppIcon)
    graph = _VARS['window']['Graph']

    filename = "Files/_py_code/_helper_code/arc_png.dat"
    progress_bar = cpb.Progress_Bar(graph, filename)
    progress_bar.set_target((int(methods.get_true())/4)*360)

##EVENT HANDLER
while True:
    event, values = _VARS["window"].read(timeout=20)

    if event == "EXIT" or event == sg.WIN_CLOSED:
        break
    if event == 'Refresh':
        updateChart()
        #window.Element('-TEXTBOX-').update()
    if event == '__TIMEOUT__':
        progress_bar.move()
    if event == 'Initialize': 
        # _VARS['win2'] = sg.Window("Enter Details", lay_ob.reinitialize_layout(),
        #                     finalize=True,
        #                     resizable=True,
        #                     location=(100,50),
        #                     element_justification="left")
        # while True: 
        #     event1, values1 = _VARS["win2"].read()
        #     if event1 == sg.WIN_CLOSED:
        #         break
        # _VARS["win2"].close()
        pass
    
    if event == 'Trip': 
        _VARS['winWarn'] = sg.Window("Warning", lay_ob.warning_layout(),
                            finalize=True,
                            resizable=True,
                            location=(100,50),
                            element_justification="center", icon = AppIcon)
        while True: 
            event1, values1 = _VARS["winWarn"].read()
            if event1 == sg.WIN_CLOSED:
                break
            if event1 == 'YES': 
                methods.update_fails()
                methods.update_log(dT.strftime("%d %B, %Y"))
                break
            if event1 == 'NO': 
                break
        _VARS["winWarn"].close()
    
    if event == "-Settings-" and values["-Settings-"] == "Rename Habit":
        _VARS['winRename'] = sg.Window("Pick a new name", lay_ob.renamehab_layout(),
                            finalize=True,
                            resizable=True,
                            location=(100,50),
                            element_justification="center", icon = AppIcon)
        while True: 
            event1, values1 = _VARS['winRename'].read()
            if event1 == sg.WIN_CLOSED:
                break
            if event1 == 'Enter': 
                methods.update_habitname(values1["-TxT-"]) 
                print(values1["-TxT-"])
                break
            if event1 == 'Cancel': 
                break
        _VARS['winRename'].close()

    if event == "-Settings-" and values["-Settings-"] == "Help":
        _VARS['winHelp'] = sg.Window("HELP", lay_ob.help_layout(),
                            finalize=True,
                            resizable=True,
                            location=(100,50),
                            element_justification="left",icon = AppIcon)
        while True: 
            event1, values1 = _VARS['winHelp'].read()
            if event1 == sg.WIN_CLOSED:
                break
            if event1 == "I'm Satisfied": 
                break
        _VARS['winHelp'].close()
    
    if event == "-Settings-" and values["-Settings-"] == "Reset":
        _VARS['winWarn'] = sg.Window("CLEAR ALL DATA", lay_ob.warning_layout(),
                            finalize=True,
                            resizable=True,
                            location=(100,50),
                            element_justification="center",icon = AppIcon)
        while True: 
            event1, values1 = _VARS['winWarn'].read()
            if event1 == sg.WIN_CLOSED:
                break
            if event1 == "YES":
                methods.reset() 
                break
            if event1 == "NO": 
                break
        _VARS['winWarn'].close()

    if event == "-GIT0-" or event == "-GIT1-":
        op("https://github.com/abram-matthew")
        
_VARS["window"].close()