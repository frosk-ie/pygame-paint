"""
Programme réalisé le, 08/08/2021
"""

from os import remove
import pygame, sys
from pygame.locals import *
from classes import *
from time import sleep
from functools import partial
from PIL import Image
import os

from tkinter import filedialog, Tk
from tkinter.messagebox import *

### VARIABLES ###
fps = 60

grid = New_Grid(length = 62, height = 62)
mouse = False
pen = New_Pen(size=3) # default color is black, default tool is pen

panel_length = 200
pixel_size = 10
mouse_offset = int(panel_length/pixel_size)

last_saved_file = ''

window = Tk()
window.withdraw()

### IMAGES ###

default_image_size = (26, 26)
pen_tool = pygame.transform.scale(pygame.image.load('pen.png'), default_image_size)
eyedropper_tool = pygame.transform.scale(pygame.image.load('eyedropper.png'), default_image_size)
eraser_tool = pygame.transform.scale(pygame.image.load('eraser.png'), default_image_size)
fill_tool = pygame.transform.scale(pygame.image.load('fill.png'), default_image_size)
pygame.display.set_icon(pen_tool)

### PYGAME STUFF ###
pygame.init()
screen_height = grid.height*pixel_size
screen_length = grid.length*pixel_size+panel_length # +200 for panel
screen = pygame.display.set_mode((screen_length, screen_height))
pygame.display.set_caption("Paint")
clock = pygame.time.Clock()

# GUI
buttons = []
sliders = []

def none():
    return

def remove_transparency(im, bg_colour=(255, 255, 255)):

    # Only process if image has transparency (http://stackoverflow.com/a/1963146)
    if im.mode in ('RGBA', 'LA') or (im.mode == 'P' and 'transparency' in im.info):

        # Need to convert to RGBA if LA format due to a bug in PIL (http://stackoverflow.com/a/1963146)
        alpha = im.convert('RGBA').split()[-1]

        # Create a new background image of our matt color.
        # Must be RGBA because paste requires both images have the same format
        # (http://stackoverflow.com/a/8720632  and  http://stackoverflow.com/a/9459208)
        bg = Image.new("RGBA", im.size, bg_colour + (255,))
        bg.paste(im, mask=alpha)
        return bg

    else:
        return im
        
def save_as_file():
    window = Tk()
    window.withdraw()
    file = filedialog.asksaveasfilename(defaultextension='.jpg', filetypes=[('JPG File','.jpg'), ('PNG File','.png'), ('TIFF File','.tif'), ('Bitmap File','.bmp'), ('Icon File','.ico'), ('All files','.*')])
    if not file:
        showerror(title='File error', message='The given image file cannot be saved.')
    try:
        
        image = Image.new('RGB', (grid.length, grid.height))
        for y in range(grid.height):
            for x in range(grid.length):
                image.putpixel([x,y], grid.grid[y][x])
        image.save(file)
        global last_saved_file
        last_saved_file = str(file)
        showinfo(title='Save', message='Successfully saved the image.')
    except:
            showerror(title='File error', message='The given image file cannot be converted.')

def save_file(last_save): 
    window = Tk()
    window.withdraw()
    try:
        image = Image.new('RGB', (grid.length, grid.height))
        for y in range(grid.height):
            for x in range(grid.length):
                image.putpixel([x,y], grid.grid[y][x])
        image.save(last_save)
        showinfo(title='Save', message='Successfully saved the image.')
    except:
        save_as_file()

def open_file():
    window = Tk()
    window.withdraw()
    file = filedialog.askopenfilename(filetypes=[('JPG File','.jpg'), ('PNG File','.png'), ('TIFF File','.tif'), ('Bitmap File','.bmp'), ('Icon File','.ico'), ('All files','.*')])
    if not file:
        showerror(title='File error', message='The given file cannot be opened.')
    try:
        image = remove_transparency(Image.open(file)) 
        if image.size[0] <= grid.length and image.size[1] <= grid.height:
            for y in range(image.size[1]):
                for x in range(image.size[0]):
                    grid.grid[y][x] = image.getpixel((x, y))
        else:
            showerror(title='Invalid dimensions', message='The maximum image dimensions are 65x65.')
        global last_saved_file
        last_saved_file = str(file)
    except:
            showerror(title='File error', message='The given image file or its extension cannot be processed.')

def new_file():
    for y in range(grid.height):
        for x in range(grid.length):
            grid.grid[y][x] = (255, 255, 255)

def change_tool(tool):
    pen.tool = tool

def change_color(color__):
    for i in range(len(sliders)):
        sliders[i].slider_position.x = int(round(color__[i]/sliders[i].max_value*(sliders[i].length-10)))+sliders[i].bar_position.x
        sliders[i].value = color__[i]

def text(surface, string, size, position, line, is_bold=False):
    font = pygame.font.SysFont('SegoeUI', size, bold=is_bold)
    text = font.render(string, 1, (0,0,0))
    surface.blit(text, (position.x, position.y))
    if line:
        pygame.draw.rect(screen, (0,0,0), pygame.Rect(position.x, position.y + size + 6, 190, 1))

# 90px between each section.
'''File buttons'''
buttons.append(New_Button(position=Vector2(10, 50), dimension=Vector2(85, 30), color=(150, 150, 150), action=lambda:open_file(), text='Open'))
buttons.append(New_Button(position=Vector2(105, 50), dimension=Vector2(85, 30), color=(150, 150, 150), action=lambda:new_file(), text='New'))
buttons.append(New_Button(position=Vector2(10, 90), dimension=Vector2(85, 30), color=(150, 150, 150), action=lambda:save_file(last_saved_file), text='Save'))
buttons.append(New_Button(position=Vector2(105, 90), dimension=Vector2(85, 30), color=(150, 150, 150), action=lambda:save_as_file(), text='Save as'))

'''Tools buttons'''
buttons.append(New_Button(position=Vector2(10, 180), dimension=Vector2(40, 40), color=(150, 150, 150), action=lambda:change_tool('pen'), image=pen_tool))
buttons.append(New_Button(position=Vector2(57, 180), dimension=Vector2(40, 40), color=(150, 150, 150), action=lambda:change_tool('eyedropper'), image=eyedropper_tool))
buttons.append(New_Button(position=Vector2(104, 180), dimension=Vector2(40, 40), color=(150, 150, 150), action=lambda:change_tool('eraser'), image=eraser_tool))
buttons.append(New_Button(position=Vector2(151, 180), dimension=Vector2(40, 40), color=(150, 150, 150), action =lambda:change_tool('fill'), image=fill_tool))

'''Color buttons'''
palettes = [
            [(255, 26, 42), (255, 70, 80), (255, 79, 90), (255, 105, 114), (255, 132, 139), (255, 158, 163), (255, 185, 187), (255, 211, 211)],
            [(255, 152, 25), (255, 164, 53), (255, 177, 82), (255, 189, 110), (255, 201, 138), (255, 213, 166), (255, 226, 195), (255, 238, 223)],
            [(94, 182, 0), (115, 192, 31), (136, 203, 63), (157, 213, 94), (179, 224, 126), (200, 234, 157), (221, 245, 189), (242, 255, 220)],
            [(0, 132, 255), (33, 148, 255), (67, 164, 255), (100, 180, 255), (134, 196, 255), (167, 212, 255), (201, 228, 255), (234, 244, 255)],
            [(170, 0, 255), (182, 34, 255), (193, 67, 255), (205, 101, 255), (216, 134, 255), (228, 168, 255), (239, 201, 255), (251, 235, 255)],
            [(0, 0, 0), (36, 36, 36), (73, 73, 73), (109, 109, 109), (146, 146, 146), (182, 182, 182), (219, 219, 219), (255, 255, 255)]
           ]
for i in range(len(palettes)):
    for j in range(len(palettes[0])):
        rgb = tuple(palettes[i][j])
        value = 22 if j > 4 else 23
        buttons.append(New_Button(position=Vector2(10+ j*22, 280+i*28),dimension=Vector2(value, 23), color=rgb, action=partial(change_color, rgb), text=''))
        # it doesn't work this lambda: since lambda: would use the value of rgb on call of the function, not the one that was registered in the button
        # functools.partials allow you to do this
sliders.append(New_Slider(Vector2(60, 466), 120, 'horizontal', (150,150,150), (36, 129, 252), 0, 255))
sliders.append(New_Slider(Vector2(60, 496), 120, 'horizontal', (150,150,150), (36, 129, 252), 0, 255))
sliders.append(New_Slider(Vector2(60, 526), 120, 'horizontal', (150,150,150), (36, 129, 252), 0, 255))

### MAIN LOOP ###
while True:
    cursor_pos = pygame.mouse.get_pos()

    # Clear screen 
    screen.fill((0,0,0))

    coords = pygame.mouse.get_pos() # -10 for panel offset
    if coords[0] > 200:
        pygame.mouse.set_visible(0)
    else:
        pygame.mouse.set_visible(1)

    #  Event handler
    for event in pygame.event.get():
        
        pen.color = (sliders[0].value, sliders[1].value, sliders[2].value)

        for i in buttons:
            if i.color == (125,125,125) or i.color == (150,150,150) or i.color == (100,100,100):
                if i.is_over(Vector2(cursor_pos[0], cursor_pos[1])):
                    i.color = (125,125,125)
                else:
                    i.color = (150,150,150)
        for i in sliders:
            if i.slider_color == (36, 129, 252) or i.slider_color == (0, 111, 255):
                if i.is_over(Vector2(cursor_pos[0], cursor_pos[1])):
                    i.slider_color = (0, 111, 255)
                else :
                    i.slider_color = (36, 129, 252)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1: pen.color = (0,0,0)
            elif event.key == pygame.K_2 : pen.color = (255,0,0)
            elif event.key == pygame.K_3 : pen.color = (0,255,0)
            elif event.key == pygame.K_4 : pen.color = (0,0,255)
            elif event.key == pygame.K_5 : pen.color = (255,255,255)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            for i in buttons:
                if i.is_over(Vector2(cursor_pos[0], cursor_pos[1])):
                    i.action()
                    if i.color == (125,125,125) or i.color == (150,150,150):
                        i.color = (100,100,100)
            
            mouse = True
            if event.button == 4 : 
                if pen.size < 10 : pen.size += 1
            if event.button == 5 : 
                if pen.size > 1 : pen.size -= 1

        elif event.type == pygame.MOUSEBUTTONUP:
            mouse = False

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Mouse events
    if mouse:
        for i in sliders:
                if i.is_over(Vector2(cursor_pos[0], cursor_pos[1])):
                    i.slider_isPressed = True
                if i.slider_isPressed:
                        i.slider_position.x = cursor_pos[0]
                        if i.slider_position.x > i.bar_position.x + i.length - 10:
                            i.slider_position.x = i.bar_position.x + i.length - 10   
                        if i.slider_position.x < i.bar_position.x:
                            i.slider_position.x = i.bar_position.x

                        slider_value = i.slider_position.x-i.bar_position.x
                        i.value = int(round(slider_value*i.max_value/(i.length-10)))
                        print(i.value)



        coords = (pygame.mouse.get_pos()[0]//pixel_size-mouse_offset, pygame.mouse.get_pos()[1]//pixel_size) # -10 for panel offset
        if coords[0] >= 0 and coords[0] < screen_length and coords[1] >= 0 and coords[1] < screen_height:
            
            if pen.tool == 'pen' :
                if pen.size > 1:
                    for i in range(0, pen.size):
                        for j in range(0, pen.size):
                            try: grid.grid[coords[1]+i][coords[0]+j] = pen.color
                            except: pass
                else:
                    grid.grid[coords[1]][coords[0]] = pen.color
                    pen.tool = 'pen'
            
            elif pen.tool == 'eyedropper' :
                (sliders[0].value, sliders[1].value, sliders[2].value) = grid.grid[coords[1]][coords[0]]

            elif pen.tool == 'eraser':
                if pen.size > 1:
                        for i in range(0, pen.size):
                            for j in range(0, pen.size):
                                try: grid.grid[coords[1]+i][coords[0]+j] = (255,255,255)
                                except: pass
                else:
                    grid.grid[coords[1]][coords[0]] = (255,255,255)
            
            elif pen.tool == 'fill':
                pen.iterative_fill(grid, Vector2(coords[0], coords[1]), grid.grid[coords[1]][coords[0]], pen.color)
                pen.tool = 'pen'
    else:
        for i in sliders:
            i.slider_isPressed = False

    # Canvas Drawing
    for y in range(grid.height):
        for x in range(grid.length):
            pygame.draw.rect(screen, grid.grid[y][x], pygame.Rect(x*pixel_size+panel_length, y*pixel_size, pixel_size, pixel_size))

    # Panel Drawing
    pygame.draw.rect(screen, (200,200,200), pygame.Rect(0, 0, panel_length, screen_height))

    # GUI Drawing
    coords = (pygame.mouse.get_pos()[0]//pixel_size-mouse_offset, pygame.mouse.get_pos()[1]//pixel_size) # -10 for panel offset
    if coords[0] >= 0 and coords[0] < screen_length and coords[1] >= 0 and coords[1] < screen_height:
        pygame.draw.rect(screen, (50,50,50) if grid.grid[coords[1]][coords[0]][0] > 50 and grid.grid[coords[1]][coords[0]][1] > 50 and grid.grid[coords[1]][coords[0]][2] > 50 else (205,205,205), pygame.Rect(coords[0]*pixel_size+panel_length,coords[1]*pixel_size, pixel_size*(pen.size if (pen.tool=='pen' or pen.tool == 'eraser') else 1), pixel_size*(pen.size if (pen.tool=='pen' or pen.tool == 'eraser') else 1)))
        if pen.size > 1 and (pen.tool == 'pen' or pen.tool == 'eraser'):
            for i in range(0, pen.size):
                for j in range(0, pen.size):
                    offset_left = 1 if j == 0 else 0
                    offset_right = 1 if j == pen.size-1 else 0
                    offset_top = 1 if i == 0 else 0
                    offset_bottom = 1 if i == pen.size-1 else 0
                    try:
                        pygame.draw.rect(screen, grid.grid[i+coords[1]][j+coords[0]], pygame.Rect((coords[0]+j)*pixel_size+panel_length+offset_left,(coords[1]+i)*pixel_size+offset_top, pixel_size-offset_right, pixel_size-offset_bottom))
                    except: pass
        else:
            pygame.draw.rect(screen, grid.grid[coords[1]][coords[0]], pygame.Rect(coords[0]*pixel_size+panel_length+1, coords[1]*pixel_size+1, pixel_size-2, pixel_size-2))

    cursor_pos = pygame.mouse.get_pos()
    for i in range(len(buttons)):
        buttons[i].draw(screen, ((0,0,0) if buttons[i].is_over(Vector2(cursor_pos[0], cursor_pos[1])) and i > 8 else None))
    for i in sliders:
        i.draw(screen)
    text(screen, 'File', 20, Vector2(10, 10), True)
    text(screen, 'Tools', 20, Vector2(10, 140), True)
    text(screen, 'Colors', 20, Vector2(10, 240), True)

    text(screen, 'R', 15, Vector2(13, 457), False, True)
    text(screen, 'G', 15, Vector2(12, 487), False, True)
    text(screen, 'B', 15, Vector2(13, 517), False, True)

    text(screen, str(sliders[0].value), 15, Vector2(28, 457), False)
    text(screen, str(sliders[1].value), 15, Vector2(28, 487), False)
    text(screen, str(sliders[2].value), 15, Vector2(28, 517), False)

    pygame.draw.rect(screen, pen.color, pygame.Rect(75, 553, 50, 50))
    screen.blit(pygame.transform.scale(pygame.image.load(pen.tool+'.png'), (22, 22)), (10, 579))

    # Update
    pygame.display.update()
    clock.tick(fps)

