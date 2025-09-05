import tkinter as tk
from tkinter import ttk

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Simple Paint App')
        self.geometry('600x400')
        self.minsize(600,400)
        
        

        self.paint_gui = Paint(self)
        self.color_chart = Color(self)
        self.menu_bar = Menu(self)

        self.mainloop()


class Menu(ttk.Frame):
    def __init__(self,parent):
        super().__init__(parent)
        self.parent = parent
        self.columnconfigure((0,1,2,3,4,5,6,7,8,9,10,11,12), weight=1, uniform='a') 
        self.rowconfigure(0, weight=1, uniform='a')

        global item_ids
        item_ids = []

        global brush_color
        global brush_size
        brush_color = tk.StringVar(value='black')
        brush_size = tk.IntVar(value=6)

     
        # Fuctions
        def decrease_brush_size():
            global brush_size
            current_brush_size = max(0,brush_size.get()-1)
            brush_size.set(current_brush_size) 

        def increase_brush_size():
            global brush_size
            current_brush_size = min(30,brush_size.get()+1)
            brush_size.set(current_brush_size) 

        def delete_canvas_items():
            self.parent.paint_gui.delete('all') 

        def delete_last_item():
            for i in range(3):
                if item_ids: # Check if there are items to delete
                    id_to_delete = item_ids.pop() # Get the last added ID and remove it from the list
                    self.parent.paint_gui.delete(id_to_delete)

        # widgets
        ttk.Button(self, text='-' , command= decrease_brush_size).grid(column=0, row=0, sticky='nsew')
        ttk.Label(self, textvariable=brush_size , anchor='center' , font=(20)).grid(column=1, row=0, sticky='nsew')
        ttk.Button(self, text='+' , command= increase_brush_size).grid(column=2, row=0, sticky='nsew')
        ttk.Button(self, text='X' , command= delete_canvas_items).grid(column=5, row=0, sticky='nsew')
        ttk.Button(self, text='<--' , command= delete_last_item).grid(column=4, row=0, sticky='nsew')
        ttk.Entry(self).grid(column=9, row=0, columnspan=3, sticky='nsew')
        ttk.Button(self, text='save' ).grid(column=12, row=0, sticky='nsew')

        self.place(relx=1, rely=1, relwidth=1, height=30, anchor='se')

class Color(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.columnconfigure(0, weight=1, uniform='a')
        self.rowconfigure((0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16), weight=1, uniform='a')

        # functions
        def set_color(color):
            global brush_color
            brush_color.set(color)  
        
        # style object
        style = ttk.Style()
        style.configure('Red.TButton', background='red')
        style.configure('Green.TButton', background='green')
        style.configure('Yellow.TButton', background='yellow')
        style.configure('Blue.TButton', background='blue')
        style.configure('Black.TButton', background='black')
        style.configure('Purple.TButton', background='purple')
        style.configure('Orange.TButton', background='orange')
        style.configure('Grey.TButton', background='grey')
        style.configure('Pink.TButton', background='pink')
        style.configure('Brown.TButton', background='brown')
        style.configure('Gold.TButton', background='gold')
        style.configure('White.TButton', background='white')


        # buttons
        ttk.Button(self, style='Red.TButton', command = lambda: set_color('red')).grid(column=0, row=1, sticky='nsew')
        ttk.Button(self, style='Green.TButton', command = lambda: set_color('green')).grid(column=0, row=0, sticky='nsew')
        ttk.Button(self, style='Yellow.TButton',command = lambda: set_color('yellow')).grid(column=0, row=2, sticky='nsew')
        ttk.Button(self, style='Blue.TButton', command = lambda: set_color('blue')).grid(column=0, row=3, sticky='nsew')
        ttk.Button(self, style='Black.TButton', command = lambda: set_color('black')).grid(column=0, row=4, sticky='nsew')
        ttk.Button(self, style='Purple.TButton', command = lambda: set_color('purple')).grid(column=0, row=5, sticky='nsew')
        ttk.Button(self, style='Orange.TButton', command = lambda: set_color('orange')).grid(column=0, row=6, sticky='nsew')
        ttk.Button(self, style='Grey.TButton', command = lambda: set_color('grey')).grid(column=0, row=7, sticky='nsew')
        ttk.Button(self, style='Pink.TButton', command = lambda: set_color('pink')).grid(column=0, row=8, sticky='nsew')
        ttk.Button(self, style='Brown.TButton', command = lambda: set_color('brown')).grid(column=0, row=9, sticky='nsew')
        ttk.Button(self, style='Gold.TButton', command = lambda: set_color('gold')).grid(column=0, row=10, sticky='nsew')
        ttk.Button(self, style='White.TButton', command = lambda: set_color('white')).grid(column=0, row=10, sticky='nsew')
        self.place(relx=1, rely=0, width= 30, relheight= 1, anchor='ne')

class Paint(tk.Canvas):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(expand=True, fill='both')
        self.configure(bg='white')

        self.bind('<B1-Motion>', self.draw_on_canvas)


    def draw_on_canvas(self,event):
        global last_item_id
        global item_ids
        x= event.x
        y= event.y
        color = brush_color.get()
        radius = brush_size.get()/2
        new_item_id = self.create_oval(x-radius, y-radius, x+radius, y+radius, fill=color, outline= color)
        item_ids.append(new_item_id)





App()