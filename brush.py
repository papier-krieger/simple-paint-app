import tkinter as tk
from tkinter import ttk


# window
window = tk.Tk()
window.title('Implementation of a brush')
window.geometry('600x600')

# canvas
canvas = tk.Canvas(window)
canvas.pack(expand=True, fill='both')

# menu frame
frame = ttk.Frame(window)
frame.pack(fill='x')

# tk Variables
brush_size = tk.IntVar(value=20)
brush_density = tk.IntVar(value=5)

r= brush_size.get()/2
d= brush_density.get() # min 3, max:r


def change_brush_size(value):
    print('changing brush size', value)
    global slider_density
    slider_density.pack_forget()
    new_max = brush_size.get()//2
    print('new radius, new max for density:',new_max)
    slider_density = ttk.Scale(frame, from_=3, to=new_max, length=300, command= change_brush_density , variable= brush_density)
    slider_density.pack(side='left', padx=10)

    global dot_grid
    r= brush_size.get()/2
    d= brush_density.get() # min 3, max:r
    # dot_grid = [(x,y) for x in float_range(-r,r,d) for y in float_range(-r,r,d) if x**2 + y**2 <= r**2]
    dot_grid = [(x,y) for x in float_range(-r,r,d) for y in float_range(-r,r,d) ]



def change_brush_density(value):
    print('changing brush density', value)
    global dot_grid
    r= brush_size.get()/2
    d= brush_density.get() # min 3, max:r
    # dot_grid = [(x,y) for x in float_range(-r,r,d) for y in float_range(-r,r,d) if x**2 + y**2 <= r**2]
    dot_grid = [(x,y) for x in float_range(-r,r,d) for y in float_range(-r,r,d) ]


    



# Sliders
slider_brush = ttk.Scale(frame, from_=0, to=50, length=300, command= change_brush_size , variable= brush_size)
slider_brush.pack(side='left', padx=10)

slider_density = ttk.Scale(frame, from_=3, to=r, length=300, command= change_brush_density , variable= brush_density)
slider_density.pack(side='left', padx=10)



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

def get_grid():
    global do_grid
    r= brush_size.get()/2
    d= brush_density.get() # min 3, max:r
    # dot_grid = [(x,y) for x in float_range(-r,r,d) for y in float_range(-r,r,d) if x**2 + y**2 <= r**2]
    dot_grid = [(x,y) for x in float_range(-r,r,d) for y in float_range(-r,r,d) ]
    return dot_grid



def brush_on_canvas(event):
    x= event.x
    y= event.y
    for point in dot_grid: 
        canvas.create_oval(x+point[0]-1/10, y+point[1]-1/10, x+point[0]+1/10, y+point[1]+1/10, fill='black', outline='black')




canvas.bind('<B1-Motion>', brush_on_canvas)



# run
window.mainloop()