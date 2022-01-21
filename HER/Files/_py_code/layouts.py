import PySimpleGUI as sg
import methods
import chronos

dT = chronos.current_date()

class layouts():

    def __init__(self):
        self.tabular_lay = []
        if methods.notnew_user():
            self.habitname = methods.get_habitname()

    def alpha_layout(self):
        sg.theme("DarkAmber")
        sg.theme_background_color('white')        #CONVERTS IT TO WHITEAMBER
        layout = [

            [sg.Text("Habit Enforcer Remodelled", font=('Lucida',11, 'bold'),text_color='Orange',background_color='White')],
            [sg.Text("Survival: "+methods.get_followed()+" Days"), 
                                                sg.VSeparator(),sg.Text("Time Elapsed: "+methods.get_true()+" Days"),
                                                sg.VSeparator(),sg.Text("Success: "+methods.get_success()+" %"),
                                                sg.VSeparator(), sg.Button("Trip")],
            [sg.HSeparator()],
            [sg.Graph((111, 111), (-55, -55), (55, 55), background_color='white',
            key='Graph',tooltip="Trial Period")],
            [sg.Text("Building Profile in: ", font=('Lucida',14, 'bold'),text_color
            ='black',background_color='White')],
            [sg.Text(methods.get_true()+" / 4 DAYS", font=('Lucida',14, 'bold'),text_color='black',background_color='White')],
            [sg.Button("EXIT"),sg.Button("Initialize")],
            [sg.Text("Current Date: "+dT.strftime("%d %B, %Y")), 
                        sg.VSeparator(), sg.Text("Habit Initiated: "+methods.get_head()),
                        sg.Stretch(background_color="White"),sg.Image("Files/_icons/gh16.png", enable_events=True, key="-GIT0-"),
                        sg.Text("abram-matthew",background_color='White',
                        font=('Lucida',7),text_color='Black', enable_events=True, key="-GIT1-",pad=(0,0))]
            ]
        return layout

    def beta_layout(self):
        sg.theme("DarkAmber")
        ####UPDATE STARS####
        streak = methods.get_streak()
        fillstar = "Files/_icons/fillstar28.png"
        unfillstar = "Files/_icons/unfillstar28_ye.png"
        starylist = [unfillstar]*5
        for idx in range(streak):
            starylist[idx] = fillstar
        #=============================================#
        
        linegraph = [[sg.Canvas(key='figCanvas',tooltip="Linechart",pad=45)], 
        [sg.Button("EXIT"),sg.Button('Refresh'),sg.Button("Initialize")]]
        circle = [[sg.Graph((111, 111), (-55, -55), (55, 55), background_color='white',
            key='Graph',tooltip="Success")], [sg.T("Down Time: "+str(methods.since_lasttrip())+"/"+str(methods.gen_goal()), 
            font=('Lucida',14, 'bold'),text_color='black',background_color='White')]]
        star = [[sg.Image(starylist[0], visible=True),sg.Image(starylist[1], visible=True),
                sg.Image(starylist[2], visible=True),sg.Image(starylist[3], visible=True),
                sg.Image(starylist[4], visible=True)],[sg.T("STREAK",font=('Lucida',14, 'bold'),
                text_color='black',background_color='White')]]
        pie = [[sg.Canvas(key='figCanvasPi',tooltip="Piechart")]]
        pie_circle = [[sg.Column(circle, element_justification='c',background_color='White'),
                     sg.Column(star, element_justification='c',background_color='White')],
                     [sg.Column(pie, element_justification='l',background_color='White')]]
        trip_record = [[sg.T("TRIP(s)", font=('Lucida',14, 'bold'),text_color='black',
                background_color='White')], [sg.T("THIS MONTH",font=('Lucida',14, 'bold'),
                text_color='black',background_color='White')],[sg.T(str(methods.trips_per_month()),
                font=('Lucida',25, 'bold'),text_color='black',background_color='White')]]

        sg.theme_background_color('white')        #CONVERTS IT TO WHITEAMBER
        layout = [
        
        [sg.Text("Survival: "+methods.get_followed()+" Days"), 
                                                sg.VSeparator(),sg.Text("Time Elapsed: "+methods.get_true()+" Days"),
                                                sg.VSeparator(),sg.Text("Success: "+methods.get_success()+" %"),
                                                sg.VSeparator(), sg.Button("Trip")],
        [sg.HSeparator()],
        [sg.Column(linegraph, element_justification='l',background_color='White'), 
        sg.Column(pie_circle, element_justification='l',background_color='White'),
        sg.Column(trip_record, element_justification='c',background_color='White')],
        
        [sg.Text("Current Date: "+dT.strftime("%d %B, %Y")), 
                        sg.VSeparator(),sg.Text("Habit Initiated: "+methods.get_head()),
                        sg.Stretch(background_color="White"),sg.Image("Files/_icons/gh16.png", enable_events=True, key="-GIT0-"),
                        sg.Text("abram-matthew",background_color='White',
                        font=('Lucida',7),text_color='Black', enable_events=True, key="-GIT1-",pad=(0,0))]
        ]
        return layout
    
    def first_layout(self):
        sg.theme("DarkAmber")
        sg.theme_background_color('white')        #CONVERTS IT TO WHITEAMBER
        layout = [[sg.Text("WELCOME TO HABIT ENFORCER", font=('Lucida',11, 'bold'),text_color='Orange', background_color='White')], 
                [sg.HSeparator()], [sg.Image("Files/_icons/HER_logo.png", visible=True)],[sg.Text("Select an option to continue.",text_color='Orange',background_color='White')], 
                [sg.Button("START")]]#, sg.Button("CONT. HABIT")]]
        return layout

    def warning_layout(self):
        sg.theme("DarkRed")
        sg.theme_background_color('white')        #CONVERTS IT TO WHITEAMBER
        layoutTrip = [
        [sg.Text("Are absolutely certain you wish to proceed? \nThis action is irreversible.",font=('Lucida',9, 'bold'),text_color='Black',background_color='White')],
        [sg.HSeparator()],
        [sg.Button("YES"),sg.Button('NO')],
        ]
        return layoutTrip

    def reinitialize_layout(self):
        layout1 = [
        [sg.Text("Enter Pilot: "), sg.In(size=(25,1), enable_events=True)],
        [sg.Text("Enter Starting Date: "), sg.In(size=(25,1), enable_events=True)],
        [sg.HSeparator()],
        [sg.Text("Optional")],
        [sg.Text("Enter Total Days: "), sg.In(size=(25,1), enable_events=True)],
        [sg.Text("Enter Successful Days: "), sg.In(size=(25,1), enable_events=True)],
        ]
        return layout1

    def renamehab_layout(self):
        layout1 = [
            [sg.Text("Input Name: "), sg.In(size=(25,1), enable_events=True,key="-TxT-")],
            [sg.Button("Confirm"),sg.Button('Cancel')]
        ]
        return layout1

    def help_layout(self):
        layout1 = [
            [sg.Text("FAQs", background_color='White', font=('Lucida',14, 'bold'),text_color='Orange')],
            [sg.HSeparator()],
            [sg.Text("Q. What does the app do?", background_color='White', font=('Lucida',11, 'bold'),text_color='Orange')],
            [sg.Text("1. This is an app that tracks how far you have pursued a habit, without abandoning it.", background_color='White', 
            font=('Lucida',10),text_color='Black')],
            [sg.Text("2. The goal of the app is not to make you follow a habit 100% but to set a threshold \n    to show what percentage of days you have followed it.", 
            background_color='White', font=('Lucida',10),text_color='Black')],
            [sg.Text("Q. What are Trips?", background_color='White', font=('Lucida',11, 'bold'),text_color='Orange')],
            [sg.Text("1. Trips are a way to acknowledge you that the habit was not followed for a day, for \n    whatever reason.", 
            background_color='White', font=('Lucida',10),text_color='Black')],
            [sg.Text("Q. What is Down Time?", background_color='White', font=('Lucida',11, 'bold'),text_color='Orange')],
            [sg.Text("1. The app calculates the amount of days you'd need before you can not follow the habit\n    again. Going against it would cause your progress to go below the set threshold of 90%.", 
            background_color='White', font=('Lucida',10),text_color='Black')],
            [sg.Text("2. Having not commited a trip past the alloted Down Time accumlates as a bragging record.", 
            background_color='White', font=('Lucida',10),text_color='Black')],
            [sg.Text("Q. What are Trips this Month?", background_color='White', font=('Lucida',11, 'bold'),text_color='Orange')],
            [sg.Text("1. It gives a number on how many days in a month the habit was not followed.", 
            background_color='White', font=('Lucida',10),text_color='Black')],
            [sg.Text("Q. What is Streak?", background_color='White', font=('Lucida',11, 'bold'),text_color='Orange')],
            [sg.Text("1. Streak builds up in packets of 7. A star would light up if a trip has not been \n    committed for over 7 days.", 
            background_color='White', font=('Lucida',10),text_color='Black')],
            [sg.Text("Q. Why are changes not updated?", background_color='White', font=('Lucida',11, 'bold'),text_color='Orange')],
            [sg.Text("1. Relaunch the application to reflect any changes.", 
            background_color='White', font=('Lucida',10),text_color='Black')],
            [sg.Stretch(background_color="White"),sg.Button("I'm Satisfied")]
        ]
        return layout1

    def gen_tab_lay(self):
        self.tabular_lay = [[sg.Text("Habit Enforcer Remodelled", relief="ridge", border_width=5,font=('Lucida',11, 'bold'),text_color='Orange',background_color='black'),
                             sg.Stretch(background_color="White"), sg.ButtonMenu('', [['reh','res','---','hp','cl'],['Rename Habit','Reset','---','Help','Close']],
                             image_filename ='Files/_icons/gear28.png',border_width=2.4,size=(2,2), button_color="white", key="-Settings-")],
                            [sg.TabGroup([[sg.Tab(self.habitname, self.beta_layout(), background_color='White', key="_TAB1_")]],
                           change_submits=True, background_color='White', border_width=0, 
                         expand_x=True, expand_y=True,key="-Tabs-")]]
        return "-Tab2-"
    
    