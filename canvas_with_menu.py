import tkinter as tk
from tkinter import ttk
import json
import os



folder_path = '/home/aries/Desktop/projects/simple-paint-app'
file_names = []
for entry in os.listdir(folder_path):
    full_path = os.path.join(folder_path, entry)
    if os.path.isfile(full_path) and entry.endswith('.canvas.json'):
        file_names.append(entry)

for file_name in file_names:
    print(file_name)


# window
window = tk.Tk()
window.geometry('600x400')
window.title('Canvas with Menu')


# menubar 
menubar = tk.Menu(window)
# window.configure(menu= menubar)
window['menu']= menubar


# file submenu
file_menu = tk.Menu(menubar, tearoff=False)
menubar.add_cascade(label ='File', menu=file_menu)

# save Canvas as JSON  and  recreate canvas from JSON
def save_canvas_to_json(canvas, filename='test.canvas.json'):
    canvas_items_data = []
    for item_id in canvas.find_all():
        item_type = canvas.type(item_id)
        coords = canvas.coords(item_id)
        options = canvas.itemconfigure(item_id)

        # Extract relevant options, ignoring Tkinter's internal ones
        clean_options = {k: v[4] for k, v in options.items() if k in {'fill','outline', 'width'}} 

        canvas_items_data.append({
            'id': item_id,
            'type': item_type,
            'coords': coords,
            'options': clean_options
        })   

    try:
        with open(filename, 'w') as f:
            json.dump(canvas_items_data,f, indent=4)
        print(f'Canvas data saved to {filename}')
    except Exception as e:
        print(f'Error saving canvas data {e}')


def load_canvas_from_json(canvas, filename='test.canvas.json'):
    try:
        with open(filename, 'r') as f:
            canvas_items_data = json.load(f)
    except FileNotFoundError:
        print(f'Error: {filename} not found.')
        return
    
    # clear existing items on the canvas before loading new ones
    # canvas.delete('all')

    for item_data in canvas_items_data:
        # item_type = item_data['type']
        coords = item_data['coords']
        options = item_data['options']

        canvas.create_oval(*coords, **options)
    
    print(f'Canvas data loaded from {filename}')


file_menu.add_command(label='Save canvas', command= lambda: save_canvas_to_json(canvas))
# file_menu.add_separator()
import_submenu = tk.Menu(menubar, tearoff=False)
for file_name in file_names: 
    import_submenu.add_command(label=file_name, command= lambda: load_canvas_from_json(canvas, file_name))
file_menu.add_cascade(label='Import', menu=import_submenu)




canvas = tk.Canvas(window, bg = 'lightblue')
canvas.pack(expand=True, fill='both')

newly_drawn_objects=[] # to store data for JSON export
brush_size = 6
brush_color = 'red'


def draw_on_canvas(event):
    x = event.x 
    y = event.y
    radius = brush_size/2
    oval_id = canvas.create_oval(x-radius,y-radius, x+radius,y+radius, fill=brush_color, outline=brush_color)
    newly_drawn_objects.append({
        'type': 'oval',
        'id': oval_id,
        'coords': (x-radius, y-radius, x+radius, y+radius),
        'options': {'fill': brush_color, 'outline': brush_color}
    }) 




canvas.bind('<B1-Motion>', draw_on_canvas)




# run
window.mainloop()
