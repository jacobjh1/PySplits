'''
Created on Nov 9, 2019

Updated 11/15/19
Did lots of stuff 12/19/2020

@author: jacobhuang

Create functions that construct menu(s) for the main application

menus.py
'''

############################################################
# TODO Later
# 1) consider doing something about negatives c times...
#    maybe yank up the most negative time and set that as 0
#    then bring all other times up by that much...
############################################################


from tkinter import Menu, Toplevel, Frame, Canvas, Listbox, Scrollbar, Label, Button, Entry, StringVar, PhotoImage
from tkinter import CASCADE, CHECKBUTTON, COMMAND, RADIOBUTTON, SEPARATOR
from tkinter import TOP, LEFT, RIGHT, BOTH, Y, N, S, E, W, VERTICAL
from tkinter import ttk

import re

from split import Split
import helpers
from run_menu import Run_settings
from hotkey_menu import Hotkey_settings
from timer_menu import Timer_settings
from color_menu import Color_settings
from file_menu import File_settings

# some comments about the structure of the "subclass" Menus 
# from 2021, since I didn't really make high level comments last year
#
# so I currently have 3 "subclass" Menus which aren't really subclasses bc they don't inherit
# but I do pass this MenuSystem object, and I call it _parent in the subclasses, so it's kind of similar 
#    (I don't remember why I chose not to inherit here)
# anyway
# each subclass (Run_settings, Hotkey_settings, Timer_settings) takes 1 arg: the MenuSystem
# each subclass has one really big function that gets called when the user opens the particular menu
#    note when I add_command, I have to pass a function
# of note, the Run and Timer menus have an update and cancel button
#    the update button calls an updating() function that updates the GUI/VA appropriately
#    so the bulk of each menu's functionality is related to the TopLevel window, not the root

class MenuSystem:
    
    def __init__ (self, root, timer, splits, bindings_listener, visual_assembly):
        self._root = root
        self._timer = timer
        self._splits = splits
        # probably need to rework this bc bindings can change, also splits can change and this seems sketch
        # or maybe not... depends how Python arguments work, idr
        self._binder = bindings_listener                 
        self._va = visual_assembly
        
        self._menu_bar = Menu(self._root)
        
        # one menu open at a time (possibly might have menus within menus, so layers is an idea)
        #    kind of like a lock, but there's no parallel anything here
        self._layer1 = False
        self._layerbind = False
        ####### Almost certainly should prevent accessing the run menu while the timer is on bc I don't deal with the current time at all
        # nor does it even make a whole lot of sense to change a split mid-run...
        
        self._run_menu = Menu(self._menu_bar)
        # layout/timer settings relate more to the visual appearance, interactions with the timer; the UX/UI/user interactions side of things
        self._layout_menu = Menu(self._menu_bar)
        self._file_menu = Menu(self._menu_bar)
        
        run_settings = Run_settings(self)
        hotkey_settings = Hotkey_settings(self)
        timer_settings = Timer_settings(self)
        color_settings = Color_settings(self)
        file_settings = File_settings(self)
        #self.run_settings()
        
        # edit title, description (category), add/remove splits, change times
        self._run_menu.add_command(label = 'Edit Run...', command = run_settings.run)
        self._menu_bar.add_cascade(label = 'Run', menu = self._run_menu)
    
        # self-descriptive
        self._layout_menu.add_command(label = 'Edit Hotkeys...', command = hotkey_settings.hotkeys)
        # edit timer precision, splits to display at once, previous splits to see on screen, show best/sum of best
        #    add an initial offset
        self._layout_menu.add_command(label = 'Timer Preferences...', command = timer_settings.timer)
        # self-descriptive
        self._layout_menu.add_command(label = 'Fonts and Colors...', command = color_settings.fonts_colors)
        
        self._menu_bar.add_cascade(label = 'Timer', menu = self._layout_menu)
        
        self._file_menu.add_command(label = 'Open Run...', command = file_settings.open_run)
        self._file_menu.add_command(label = 'Save Run As...', command = file_settings.save_run_as)
        self._file_menu.add_command(label = 'Save Run', command = file_settings.save_run)
        self._file_menu.add_separator()
        self._file_menu.add_command(label = 'Open Timer Settings...', command = file_settings.open_timer)
        self._file_menu.add_command(label = 'Save Timer Settings As...', command = file_settings.save_timer_as)
        self._file_menu.add_command(label = 'Save Timer Settings', command = file_settings.save_timer)
        
        self._menu_bar.add_cascade(label = 'File', menu = self._file_menu)