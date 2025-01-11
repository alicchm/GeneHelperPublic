import customtkinter as ctk
import tkinter as tk
from model import Model
from view import View
from controller import Controller

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        view = View(self)
        model = Model()
        controller = Controller(view, model)
        view.set_controller(controller)
        
if __name__ == '__main__':
    app = App()
    app.mainloop()