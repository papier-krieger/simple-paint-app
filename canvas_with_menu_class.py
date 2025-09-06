import tkinter as tk
from tkinter import ttk
# from tkinter import simpledialog
from tkinter import filedialog
# from tkinter import messagebox
import json
import os


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry('600x400')
        self.title('Canvas with Menu written Object oriented')

        self.canvas = Canvas(self)
        self.main_panel = MainPanel(self)
        self.color_panel = ColorPanel(self)
        self.menu_bar = MenuBar(self)

        self.mainloop()
        
class Canvas(tk.Canvas):
    def __init__(self, parent):
        super().__init__(parent)
        self.place(x=0,y=0, relwidth=0.9, relheight=0.9)
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

class MainPanel(ttk.Frame):
    def __init__(self,parent):
        super().__init__(parent)
        self.parent= parent
        self.place(relx=0, rely=1, relwidth=0.9, relheight=0.1, anchor='sw')

        
        global item_ids
        item_ids = []

        global brush_color
        global brush_size
        brush_color = tk.StringVar(value='black')
        brush_size = tk.IntVar(value=6)

        # methods
        def decrease_brush_size():
            global brush_size
            current_brush_size = max(0,brush_size.get()-1)
            brush_size.set(current_brush_size) 

        def increase_brush_size():
            global brush_size
            current_brush_size = min(30,brush_size.get()+1)
            brush_size.set(current_brush_size) 


        # widgets
        ttk.Button(self, text='-' , command= decrease_brush_size).pack(side='left', expand=True, fill='x')
        ttk.Label(self, textvariable=brush_size , anchor='center' , font=(20)).pack(side='left', expand=True, fill='x')
        ttk.Button(self, text='+' , command= increase_brush_size).pack(side='left', expand=True, fill='x')


class ColorPanel(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.place(relx=1, rely=0, relwidth=0.1 , relheight= 0.9, anchor='ne')
        self.pack_propagate(False)

        # methods 
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
        ttk.Button(self, style='Red.TButton', command = lambda: set_color('red')).pack(expand=True, fill='both')
        ttk.Button(self, style='Green.TButton', command = lambda: set_color('green')).pack(expand=True, fill='both')
        ttk.Button(self, style='Yellow.TButton',command = lambda: set_color('yellow')).pack(expand=True, fill='both')
        ttk.Button(self, style='Blue.TButton', command = lambda: set_color('blue')).pack(expand=True, fill='both')
        ttk.Button(self, style='Black.TButton', command = lambda: set_color('black')).pack(expand=True, fill='both')
        ttk.Button(self, style='Purple.TButton', command = lambda: set_color('purple')).pack(expand=True, fill='both')
        ttk.Button(self, style='Orange.TButton', command = lambda: set_color('orange')).pack(expand=True, fill='both')
        ttk.Button(self, style='Grey.TButton', command = lambda: set_color('grey')).pack(expand=True, fill='both')
        ttk.Button(self, style='Pink.TButton', command = lambda: set_color('pink')).pack(expand=True, fill='both')
        ttk.Button(self, style='Brown.TButton', command = lambda: set_color('brown')).pack(expand=True, fill='both')
        ttk.Button(self, style='Gold.TButton', command = lambda: set_color('gold')).pack(expand=True, fill='both')
        ttk.Button(self, style='White.TButton', command = lambda: set_color('white')).pack(expand=True, fill='both')

class MenuBar(tk.Menu):
    def __init__(self,parent):
        super().__init__(parent)
        parent['menu']= self   # Main MenuBar
        self.parent= parent


        # methods
        def import_json_data():
            filepath = filedialog.askopenfilename(
                title='Select the JSON file you want to import:',
                initialdir='./',
                filetypes=[('JSON files', '*.json')]
            )

            if filepath:
                try:
                    with open(filepath, 'r') as f:
                        canvas_items_data = json.load(f)
                except FileNotFoundError:
                    print(f'Error: {filepath} not found.')
                    return
                
                # clear existing items on the canvas before loading new ones
                # canvas.delete('all')

                for item_data in canvas_items_data:
                    # item_type = item_data['type']
                    coords = item_data['coords']
                    options = item_data['options']

                    self.parent.canvas.create_oval(*coords, **options)
                
                print(f'Canvas data loaded from {filepath}')




        def save_as():
            filename = filedialog.asksaveasfilename(
                title='Save your painting as JSON',
                defaultextension='.json',
                filetypes=[('JSON files', '*.json')]
            )
            data= create_dict_for_json()

            if filename:
                try:
                    with open(filename, 'w') as f:
                        json.dump(data,f, indent=4)

                    print(f'Canvas saved to {filename}')
                except Exception as e:
                    print(f'Error saving file: {e}')
            else:
                print('Save operation canceled.')
                
        def create_dict_for_json():
            canvas_items_data = []
            can= self.parent.canvas
            for item_id in can.find_all():
                item_type = can.type(item_id)
                coords = can.coords(item_id)
                options = can.itemconfigure(item_id)

                # Extract relevant options, ignoring Tkinter's internal ones
                clean_options = {k: v[4] for k, v in options.items() if k in {'fill','outline', 'width'}} 

                canvas_items_data.append({
                    'id': item_id,
                    'type': item_type,
                    'coords': coords,
                    'options': clean_options
                })   
            return canvas_items_data

        def delete_canvas():
            self.parent.canvas.delete('all') 

        def delete_last_item():
            for i in range(3):
                if item_ids: # Check if there are items to delete
                    id_to_delete = item_ids.pop() # Get the last added ID and remove it from the list
                    self.parent.canvas.delete(id_to_delete)


        # Options in MenuBar 

        self.add_command(label='Save as', command= save_as)
        self.add_command(label='New', command=delete_canvas)
        self.add_command(label='Exit', command=self.parent.destroy)
        self.add_command(label='Import', command=import_json_data)
        self.add_command(label='Export')
        self.add_command(label='<--', command=delete_last_item)






if __name__ == '__main__':

    App()