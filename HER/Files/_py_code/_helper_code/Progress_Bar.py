import pickle
from random import randint
import PySimpleGUI as sg

class Progress_Bar():

    def __init__(self, graph, filename, text_color='black',
            font=('Courier New', 10)):
        self.graph = graph
        with open (filename, 'rb') as file:
            self.data = pickle.load(file)
        self.text_color = text_color
        self.font = font
        self.p, self.t   = None, None
        self.initial()

    def initial(self, angle=0):
        self.circle = self.graph.draw_image(
            data=self.data[361], location=(-50, 50))
        self.set_now(angle)
        self.set_target(angle)

    def set_target(self, angle=0, step=10):
        self.target = min(360, max(0, int(angle)))
        self.step = min(360, max(1, int(step)))

    def set_now(self, angle=0):
        self.angle = min(360, max(0, int(angle)))

    def move(self):
        if self.target == self.angle:
            text = f'{self.angle/3.6:.1f}%'
            self.p = self.graph.draw_image(data=self.data[self.angle],
            location=(-50, 50))
            self.t = self.graph.draw_text(text, (0, 0), color=self.text_color,
            font=self.font, text_location=sg.TEXT_LOCATION_CENTER)
            return True
        if self.angle < self.target:
            self.angle = min(self.target, self.angle+self.step)
        else:
            self.angle = max(self.target, self.angle-self.step)
        if self.p:
            self.graph.delete_figure(self.p)
        if self.t:
            self.graph.delete_figure(self.t)
        text = f'{self.angle/3.6:.1f}%'
        self.p = self.graph.draw_image(data=self.data[self.angle],
            location=(-50, 50))
        self.t = self.graph.draw_text(text, (0, 0), color=self.text_color,
            font=self.font, text_location=sg.TEXT_LOCATION_CENTER)
        return False


###########DISCLAIMER:
####CODE IN THIS FILE BY: jason990420 : https://github.com/PySimpleGUI/PySimpleGUI/issues/3736
####ALL CODE AND RESOURCES RELATED TO CIRCULAR PROGRESS BAR OBATINED FROM THE ABOVE LINK
