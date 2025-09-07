import tkinter as tk
from tkinter import ttk


# window
window = tk.Tk()
window.title('Implementation of a brush')
window.geometry('900x600')

# canvas
canvas = tk.Canvas(window)
canvas.pack(expand=True, fill='both')

# frame for title for sliders
frame_label = ttk.Frame(window)
frame_label.pack(fill='x')

# frame for sliders
frame_slider = ttk.Frame(window)
frame_slider.pack(fill='x')

# frame for values of sliders 
frame_label_value = ttk.Frame(window)
frame_label_value.pack(fill='x')

# tk Variables
brush_size = tk.IntVar(value=100)
grid_density = tk.DoubleVar(value=0.2)
point_size = tk.DoubleVar(value=0.2)

r= brush_size.get()/2
d= 1/grid_density.get() # min 3, max:r


def change_brush_size(value):
    print('changing brush size', value)
    global slider_grid_density
    slider_grid_density.pack_forget()
    r = brush_size.get()//2
    slider_grid_density = ttk.Scale(frame_slider, from_=1/r, to=1/3, command= change_grid_density , variable= grid_density)
    slider_grid_density.pack(side='left', padx=10, after=slider_brush_size , expand=True, fill='x')


    global dot_grid
    r= brush_size.get()/2
    d= 1/grid_density.get() # grid_density between 1/r and 1/3
    # dot_grid = [(x,y) for x in float_range(-r,r,d) for y in float_range(-r,r,d) if x**2 + y**2 <= r**2]
    dot_grid = [(x,y) for x in float_range(-r,r,d) for y in float_range(-r,r,d) ]



def change_grid_density(value):
    print('changing brush density', value)
    global dot_grid
    r= brush_size.get()/2
    d= 1/grid_density.get() # grid_density between 1/r and 1/3 
    # dot_grid = [(x,y) for x in float_range(-r,r,d) for y in float_range(-r,r,d) if x**2 + y**2 <= r**2]
    dot_grid = [(x,y) for x in float_range(-r,r,d) for y in float_range(-r,r,d) ]


# Labels for names of slider
ttk.Label(frame_label, text='Brush size', anchor='center').pack(side='left', padx=10, expand='True', fill='x')
ttk.Label(frame_label, text='Grid density', anchor='center').pack(side='left', padx=10, expand='True', fill='x')
ttk.Label(frame_label, text='Point size', anchor='center').pack(side='left', padx=10, expand='True', fill='x')


# Sliders
slider_brush_size = ttk.Scale(frame_slider, from_=4, to=500,  command= change_brush_size , variable= brush_size)
slider_brush_size.pack(side='left', padx=10, expand=True, fill='x')

slider_grid_density = ttk.Scale(frame_slider, from_=1/r, to=1/3, command= change_grid_density , variable= grid_density)
slider_grid_density.pack(side='left', padx=10, expand=True, fill='x')

slider_point_size = ttk.Scale(frame_slider, from_=0.01, to=6, command= lambda _ : print('test') , variable= point_size)
slider_point_size.pack(side='left', padx=10, expand=True, fill='x')


# Labels for values of slider
ttk.Label(frame_label_value, textvariable=brush_size, anchor='center').pack(side='left', padx=10, expand='True', fill='x')
ttk.Label(frame_label_value, textvariable=grid_density, anchor='center').pack(side='left', padx=10, expand='True', fill='x')
ttk.Label(frame_label_value, textvariable=point_size, anchor='center').pack(side='left', padx=10, expand='True', fill='x')


def float_range(start, stop, step):
    current = start
    while current <= stop:
        yield current
        current += step


# dot_grid = [(x,y) for x in float_range(-r,r,d) for y in float_range(-r,r,d) if x**2 + y**2 <= r**2]
dot_grid = [(x,y) for x in float_range(-r,r,d) for y in float_range(-r,r,d) ]

print(dot_grid)

def draw_on_canvas(event):
    x= event.x
    y= event.y
    canvas.create_oval(x-r,y-r,x+r, y+r, fill='black', outline='black')


def brush_on_canvas(event):
    x= event.x
    y= event.y
    r = point_size.get()/2
    for point in dot_grid: 
        canvas.create_oval(x+point[0]-r, y+point[1]-r, x+point[0]+r, y+point[1]+r, fill='green', outline='green')




canvas.bind('<B1-Motion>', brush_on_canvas)



# run
window.mainloop()