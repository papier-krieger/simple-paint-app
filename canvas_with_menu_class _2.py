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
        self.geometry('900x600')
        self.minsize(900,600)
        self.title('Canvas with Menu written Object oriented')

        self.canvas = Canvas(self)
        self.main_panel = MainPanel(self)
        self.color_panel = ColorPanel(self)
        self.menu_bar = MenuBar(self)

        self.mainloop()
        
class Canvas(tk.Canvas):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.place(x=0,y=0, relwidth=0.9, relheight=0.9)
        self.configure(bg='white')

        # self.bind('<B1-Motion>', self.draw_on_canvas)
        self.bind('<B1-Motion>', self.brush_on_canvas)

    def draw_on_canvas(self,event):
        x= event.x
        y= event.y
        color = self.parent.main_panel.brush_color.get()
        radius = self.parent.main_panel.brush_size.get()/2
        new_item_id = self.create_oval(x-radius, y-radius, x+radius, y+radius, fill=color, outline= color)
        self.parent.main_panel.item_ids.append(new_item_id)

    def brush_on_canvas(self,event):
        x= event.x
        y= event.y
        color = self.parent.main_panel.brush_color.get()
        r = self.parent.main_panel.gridpoint_size.get()/2
        dot_grid = self.parent.main_panel.dot_grid
        for point in dot_grid: 
            new_item_id = self.create_oval(x+point[0]-r, y+point[1]-r, x+point[0]+r, y+point[1]+r, fill=color, outline=color)
            self.parent.main_panel.item_ids.append(new_item_id)



class MainPanel(ttk.Frame):
    def __init__(self,parent):
        super().__init__(parent) # Menu MainFrame
        self.parent= parent
        self.place(relx=0, rely=1, relwidth=0.9, relheight=0.10, anchor='sw')

        # SubFrame for title for sliders
        self.frame_label = ttk.Frame(self)
        self.frame_label.pack(fill='x')

        # SubFrame for sliders
        self.frame_slider = ttk.Frame(self)
        self.frame_slider.pack(fill='x')

        # SubFrame for values of sliders 
        self.frame_label_value = ttk.Frame(self)
        self.frame_label_value.pack(fill='x')

        self.item_ids = []

        # Tk Variables
        self.brush_color = tk.StringVar(value='black')
        self.brush_size = tk.IntVar(value=10)
        self.grid_density = tk.DoubleVar(value=0.2)
        self.gridpoint_size= tk.DoubleVar(value=0.2)

        r= self.brush_size.get()/2
        d= 1/self.grid_density.get() # min 3, max:r


        # methods

        def show_brush_size(value):
            value = int(float(value))
            # print(value)
            self.brush_size.set(value)
            # print(self.brush_size.get())

        def show_grid_density(value):
            value = float(f'{float(value):.3f}')
            self.grid_density.set(value)

        def show_gridpoint_size(value):
            value = float(f'{float(value):.3f}')
            self.gridpoint_size.set(value)


        def change_brush_size(value):
            print('changing brush size to:',f'{float(value):.1f}')
            self.slider_grid_density.pack_forget()
            r = self.brush_size.get()//2+1
            self.slider_grid_density = ttk.Scale(self.frame_slider, from_=1/(10*r), to=1/3, command= change_grid_density , variable= self.grid_density)
            self.slider_grid_density.pack(side='left', padx=10, after=self.slider_brush_size , expand=True, fill='x')


            r= self.brush_size.get()/2
            d= 1/self.grid_density.get() # grid_density between 1/r and 1/3
            # dot_grid = [(x,y) for x in float_range(-r,r,d) for y in float_range(-r,r,d) if x**2 + y**2 <= r**2]
            self.dot_grid = [(x,y) for x in float_range(-r,r,d) for y in float_range(-r,r,d) ]
            show_brush_size(value)
       
        
        def change_grid_density(value):
            print('changing grid density to', f'{float(value):.3f}')
            global dot_grid
            r= self.brush_size.get()/2
            d= 1/self.grid_density.get() # grid_density between 1/r and 1/3 
            # dot_grid = [(x,y) for x in float_range(-r,r,d) for y in float_range(-r,r,d) if x**2 + y**2 <= r**2]
            self.dot_grid = [(x,y) for x in float_range(-r,r,d) for y in float_range(-r,r,d) ]
            show_grid_density(value)

        def change_gridpoint_size(value):
            print('changing gridpoint size to:', f'{float(value):.3f}')
            show_gridpoint_size(value)


        def float_range(start, stop, step):
            current = start
            while current <= stop:
                yield current
                current += step
            
        # widgets

        # Labels for names of slider
        ttk.Label(self.frame_label, text='Brush size', anchor='center').pack(side='left', padx=10, expand='True', fill='x')
        ttk.Label(self.frame_label, text='Grid density', anchor='center').pack(side='left', padx=10, expand='True', fill='x')
        ttk.Label(self.frame_label, text='Point size', anchor='center').pack(side='left', padx=10, expand='True', fill='x')


        # Sliders
        self.slider_brush_size = ttk.Scale(self.frame_slider, from_=1, to=500,  command= change_brush_size , variable= self.brush_size)
        self.slider_brush_size.pack(side='left', padx=10, expand=True, fill='x')

        self.slider_grid_density = ttk.Scale(self.frame_slider, from_=1/(10*r), to=1/3, command= change_grid_density , variable= self.grid_density)
        self.slider_grid_density.pack(side='left', padx=10, expand=True, fill='x')

        self.slider_point_size = ttk.Scale(self.frame_slider, from_=0.01, to=6, command= change_gridpoint_size , variable= self.gridpoint_size)
        self.slider_point_size.pack(side='left', padx=10, expand=True, fill='x')


        # Labels for values of slider
        ttk.Label(self.frame_label_value, textvariable=self.brush_size, anchor='center').pack(side='left', padx=10, expand='True', fill='x')
        ttk.Label(self.frame_label_value, textvariable=self.grid_density, anchor='center').pack(side='left', padx=10, expand='True', fill='x')
        ttk.Label(self.frame_label_value, textvariable=self.gridpoint_size, anchor='center').pack(side='left', padx=10, expand='True', fill='x')


        # self.dot_grid = [(x,y) for x in float_range(-r,r,d) for y in float_range(-r,r,d) if x**2 + y**2 <= r**2]
        self.dot_grid = [(x,y) for x in float_range(-r,r,d) for y in float_range(-r,r,d) ]



class ColorPanel(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        
        self.place(relx=1, rely=0, relwidth=0.1 , relheight= 0.9, anchor='ne')
        self.pack_propagate(False)

        # methods 
        def set_color(color):
            self.parent.main_panel.brush_color.set(color)  
       
        
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
                if self.parent.main_panel.item_ids: # Check if there are items to delete
                    id_to_delete = self.parent.main_panel.item_ids.pop() # Get the last added ID and remove it from the list
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