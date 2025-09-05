import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
from tkinter import messagebox
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


def load_canvas_from_json(canvas, filename):
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




def save_as(canvas):
    name = simpledialog.askstring('Input','Save canvas as: ')
    name = name + '.canvas.json'
    if name != '.canvas.json':
        if name not in file_names:
            save_canvas_to_json(canvas=canvas, filename=name)
        else:
            print('Name is already used!!! Are you sure to use this name?')
            save_as_2(canvas, name)
    else:
        print('Empty name string is not allowed')
        save_as(canvas)

def save_as_2(canvas, name):
    result = messagebox.askokcancel('Confirmation',f'The name "{name[:-12]}" is already in use. Do you want to use it anyway?')

    if result:
        save_canvas_to_json(canvas=canvas, filename=name)
    else:
        print('Saving process aborted')


def delete_canvas(canvas, filename):
    folder_path = '/home/aries/Desktop/projects/simple-paint-app'
    file_name = filename
    file_path = os.path.join(folder_path, file_name)
    try:
        os.remove(file_path)
        file_names.remove(file_name)
        delete_submenu.delete(file_name[:-12])
        import_submenu.delete(file_name[:-12])
        print(f'The file "{file_name}" deleted successfully.')
    except Exception as e:
        print(f'An unexpected error occured: {e}')



file_menu.add_command(label='Save as', command= lambda: save_as(canvas))
# file_menu.add_separator()
import_submenu = tk.Menu(menubar, tearoff=False)
for file_name in file_names:
    f_n = file_name
    import_submenu.add_command(label=file_name[:-12], command= lambda f_n = file_name: load_canvas_from_json(canvas, filename=f_n))
file_menu.add_cascade(label='Import', menu=import_submenu)

delete_submenu = tk.Menu(menubar, tearoff=False)
for file_name in file_names:
    f_n = file_name
    delete_submenu.add_command(label=file_name[:-12], command= lambda f_n = file_name: delete_canvas(canvas, filename=f_n))
file_menu.add_cascade(label='Delete', menu=delete_submenu)


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
