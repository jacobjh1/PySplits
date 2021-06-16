'''
Created on June 15, 2021

@author: Jacob H.

first new file since winter break! allows changing the colors and fonts used throughout the app

color_menu.py
'''

from tkinter import Toplevel, colorchooser, font, Label, Frame, Radiobutton, Button, IntVar
from tkinter import N, S, E, W

class Color_settings: # also fonts, and fonts are highly OS dependent, and I don't plan on testing on Windows for a while
    def __init__ (self, parent):
        self._parent = parent
        self._va = parent._va
        
    # I could combine these next 2 functions into one, and pass an argument that's an extended array for the RHS 
    def restore_old (self):
        self._va.title_font = self._old_fonts[0]
        self._va.desc_font = self._old_fonts[1]
        self._va.split_font = self._old_fonts[2]
        self._va.big_time_font = self._old_fonts[3]
        self._va.small_time_font = self._old_fonts[4]
        
        self._va.title_color = self._old_colors[0]
        self._va.desc_color = self._old_colors[1]
        self._va.split_text_color = self._old_colors[2] 
        self._va.lower_text_color = self._old_colors[3]
        self._va.time_color = self._old_colors[4]
        self._va.ahead = self._old_colors[5]
        self._va.behind = self._old_colors[6]
        self._va.best_color = self._old_colors[7]
        self._va.bg_color = self._old_colors[8]
        self._va.mid_color = self._old_colors[9]
        self._va.accent_color = self._old_colors[10]
        
        self._va.update_fonts_colors()
        
    def set_new (self):
        self._va.title_font = self._font_labels[0]['font']
        self._va.desc_font = self._font_labels[1]['font']
        self._va.split_font = self._font_labels[2]['font']
        self._va.big_time_font = self._font_labels[3]['font']
        self._va.small_time_font = self._font_labels[4]['font']
        
        self._va.title_color = self._color_boxes[0]['bg']
        self._va.desc_color = self._color_boxes[1]['bg']
        self._va.split_text_color = self._color_boxes[2]['bg']
        self._va.lower_text_color = self._color_boxes[3]['bg']
        self._va.time_color = self._color_boxes[4]['bg']
        self._va.ahead = self._color_boxes[5]['bg']
        self._va.behind = self._color_boxes[6]['bg']
        self._va.best_color = self._color_boxes[7]['bg']
        self._va.bg_color = self._color_boxes[8]['bg']
        self._va.mid_color = self._color_boxes[9]['bg']
        self._va.accent_color = self._color_boxes[10]['bg']
        
        self._va.update_fonts_colors()
        
    def destroy (self):
        # prevents (I think?) a weird bug where the font menu persists into the next execution of the app
        self._window.tk.call('tk', 'fontchooser', 'hide')
        self._parent._layer1 = False
        self._window.destroy()
        
    def testing (self):
        self.set_new()
        
    def confirming (self):
        self.set_new()
        self.destroy() 
        
    def canceling (self):
        self.restore_old()
        self.destroy()
    
    def fonts_colors (self):
        # kinda just realized... I should probably make this "locking" bit a parent method
        if self._parent._layer1:
            self._parent._root.bell()
            return 
        self._parent._layer1 = True
        
        self._old_fonts = [self._va.title_font, self._va.desc_font, self._va.split_font, self._va.big_time_font, self._va.small_time_font]
        self._old_colors = [self._va.title_color, self._va.desc_color, self._va.split_text_color, self._va.lower_text_color, self._va.time_color, 
                            self._va.ahead, self._va.behind, self._va.best_color, self._va.bg_color, self._va.mid_color, self._va.accent_color]
            
        self._window = Toplevel(self._parent._root)
        self._window.title('Fonts and Colors')
        self._window.protocol('WM_DELETE_WINDOW', self.canceling)
        
        # bulk of the self._window
        self.fonts() # uses self._window rows 0-1, column 0
        self.colors() # uses self._window row 2, column 0
        
        # footer of self._window with cancel, test, and confirm
        self.footer() # uses self._window row 3, column 0
        
    # font picker
    def fonts (self):
        font_frame = Frame(self._window)
        font_frame.grid(row = 0, column = 0, sticky = (N, S, E, W))
        self._window.rowconfigure(0, weight = 1)
        self._window.columnconfigure(0, weight = 1)
        
        get_font_btn = Button(self._window, text = 'Fonts...')
        get_font_btn.grid(row = 1, column = 0, pady = (5, 30))
        # self._window.rowconfigure(1, weight = 0)
        
        # super simple to add more color options: just add to this list
        # um also depending on what I do later, add'l colors may factor into label backgrounds, idk yet
        # so this list may need to become an instance variable 
        # also the 3 footer functions should be updated as well 
        # also also note that order matters in that this should match __init__
        self._font_labels = [Label(font_frame, font = self._va.title_font, text = 'Run title font'),
                       Label(font_frame, font = self._va.desc_font, text = 'Run description font'),
                       Label(font_frame, font = self._va.split_font, text = 'Information font'),
                       Label(font_frame, font = self._va.big_time_font, text = 'Main stopwatch font'),
                       Label(font_frame, font = self._va.small_time_font, text = 'Secondary stopwatch font')]
        
        update = IntVar(value = 0)
        font_rbs = [Radiobutton(font_frame, variable = update, value = i) for i in range(len(self._font_labels))]
       
        for i, (lbl, rb) in enumerate(zip(self._font_labels, font_rbs)):
            lbl.grid(row = i, column = 0, sticky = W)
            Label(font_frame, font = 'TkDefaultFont', text = 'Modify:').grid(row = i, column = 1, sticky = E)
            rb.grid(row = i, column = 2, sticky = W)
            font_frame.rowconfigure(i, weight = 1)
            
        font_frame.columnconfigure(0, weight = 1)
        # font_frame.columnconfigure(1, weight = 0)
        # font_frame.columnconfigure(2, weight = 0)
        
        def set_font (font): 
            # doesn't change the corresponding global font var just yet
            self._font_labels[update.get()].config(font = font)
            # self._window.tk.call('tk', 'fontchooser', 'hide') not really a point if I'm not going to use a lock for fonts
        
        callback_fxn = self._window.register(set_font)
        def callback_font ():    
            # note all widgets have a .cget('attribute') method, and subscripting ['attribute'] is another way
            self._window.tk.call('tk', 'fontchooser', 'hide')
            self._window.tk.call('tk', 'fontchooser', 'configure', '-font', self._font_labels[update.get()]['font'], '-command', callback_fxn)
            self._window.tk.call('tk', 'fontchooser', 'show')
    
        get_font_btn.config(command = callback_font)
    
    # color picker
    def colors (self):
        color_frame = Frame(self._window)
        color_frame.grid(row = 2, column = 0, sticky = (N, S, E, W), padx = 25)
        self._window.rowconfigure(2, weight = 1)
        
        # 11 colors for now, 4 text colors on left, 4 text colors in center, 3 app colors on right
        
        color_labels = [Label(color_frame, text = 'Title text color'),
                        Label(color_frame, text = 'Description text color'),
                        Label(color_frame, text = 'Split text color'),
                        Label(color_frame, text = 'Lower text color'),
                        Label(color_frame, text = 'Stopwatch text color'),
                        Label(color_frame, text = 'Ahead of splits color'),
                        Label(color_frame, text = 'Behind splits color'),
                        Label(color_frame, text = 'Best split color'),
                        Label(color_frame, text = 'App background color'),
                        Label(color_frame, text = 'App middle layer color'),
                        Label(color_frame, text = 'App accent color')]
        
        self._color_boxes = [Label(color_frame, text = '   ', relief = 'ridge', bg = self._va.title_color), 
                       Label(color_frame, text = '   ', relief = 'ridge', bg = self._va.desc_color), 
                       Label(color_frame, text = '   ', relief = 'ridge', bg = self._va.split_text_color), 
                       Label(color_frame, text = '   ', relief = 'ridge', bg = self._va.lower_text_color), 
                       Label(color_frame, text = '   ', relief = 'ridge', bg = self._va.time_color), 
                       Label(color_frame, text = '   ', relief = 'ridge', bg = self._va.ahead), 
                       Label(color_frame, text = '   ', relief = 'ridge', bg = self._va.behind), 
                       Label(color_frame, text = '   ', relief = 'ridge', bg = self._va.best_color), 
                       Label(color_frame, text = '   ', relief = 'ridge', bg = self._va.bg_color), 
                       Label(color_frame, text = '   ', relief = 'ridge', bg = self._va.mid_color), 
                       Label(color_frame, text = '   ', relief = 'ridge', bg = self._va.accent_color)]
        
        for i, (lbl, box) in enumerate(zip(color_labels, self._color_boxes)):
            if 0 <= i <= 3:
                column = 0
            elif 3 < i <= 7:
                column = 2
            else: # 7 < i <= 10
                column = 4
            
            lbl.grid(row = i % 4, column = column, sticky = E)
            box.grid(row = i % 4, column = column + 1, sticky = W)
            
        
        def choose_color (index):
            hex_code = colorchooser.askcolor(title = color_labels[index]['text'])
            if hex_code[1] is not None:
                self._color_boxes[index].config(bg = hex_code[1])    
        
        # bc I keep making all the bindings apply to the last color if I try it in the for loop
        # and I tried making copies but that didn't work either 
        # idk maybe I just had a silly mistake somewhere, but this works regardless
        def do_binding (index):
            # https://www.python-course.eu/tkinter_events_binds.php
            self._color_boxes[index].bind('<Button-1>', lambda _ : choose_color(index)) # left click
            
        do_binding(0)
        do_binding(1)
        do_binding(2)
        do_binding(3)
        do_binding(4)
        do_binding(5)
        do_binding(6)
        do_binding(7)
        do_binding(8)
        do_binding(9)
        do_binding(10)
            
        color_frame.columnconfigure(0, weight = 1)
        color_frame.columnconfigure(2, weight = 1)
        color_frame.columnconfigure(4, weight = 1)
        for i in range(4):
            color_frame.rowconfigure(i, weight = 1)
                
            
    def footer (self):
        foot = Frame(self._window)
        foot.grid(row = 3, column = 0, sticky = (N, S, E, W), pady = 25)
        # self._window.rowconfigure(3, weight = 0)
    
        cancel = Button(foot, text = 'Cancel', command = self.canceling)
        test = Button(foot, text = 'Test', command = self.testing)
        confirm = Button(foot, text = 'Confirm', command = self.confirming)
        
        cancel.grid(row = 0, column = 0)
        test.grid(row = 0, column = 1)
        confirm.grid(row = 0, column = 2)
        
        foot.rowconfigure(0, weight = 1, pad = 20)
        foot.columnconfigure(0, weight = 1)
        foot.columnconfigure(1, weight = 1)
        foot.columnconfigure(2, weight = 1)
        