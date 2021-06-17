'''
Created on June 16, 2021

@author: Jacob H.

manage opening and saving various JSON files

file_menu.py
'''

from tkinter import filedialog 
from json.decoder import JSONDecodeError
from file_loader import File_loader
from file_saver import File_saver
import os.path

class File_settings:
    def __init__ (self, parent):
        self._parent = parent
        self._loader = File_loader(parent._va)
        self._saver = File_saver(parent._va)
    
    def update_curr_run_path (self, new_path):
        self._parent._va._curr_run_path = new_path
        self._saver.update_recents()
        
    def update_curr_timer_path (self, new_path):
        self._parent._va._curr_timer_path = new_path
        self._saver.update_recents()
    
    def open_timer (self):
        # fairly certain that the file dialog blocks so I don't need to obtain the lock here
        if self._parent._layer1:
            self._parent._root.bell()
            return 
        
        filename = filedialog.askopenfilename()
        if filename == "":
            return
        
        try:
            self._loader.get_timer(filename)
            self.update_curr_timer_path(filename)
        except JSONDecodeError:
            self._parent._root.bell()
        except Exception:
            pass
    
    def open_run (self):
        # so much easier to just force a reset before opening a new run
        # bc of saving shenanigans and parallel-but-not execution 
        if self._parent._layer1 or not self._parent._va._timer.is_reset():
            self._parent._root.bell()
            return 
        
        filename = filedialog.askopenfilename()
        if filename == "":
            return
        
        try:
            self._loader.get_run(filename)
            self.update_curr_run_path(filename)
        except JSONDecodeError:
            self._parent._root.bell()
        except Exception:
            pass
        
    def save_timer (self):
        if self._parent._layer1:
            self._parent._root.bell()
            return 
        
        if self._parent._va._curr_timer_path is None:
            self.save_timer_as()
            return
        
        # implication is that the user should want to replace an existing file
        if not os.path.isfile(self._parent._va._curr_timer_path):
            # TODO: probably should have an error message for invalid path
            self._parent._root.bell()
            return
        
        self._saver.save_timer(self._parent._va._curr_timer_path)
    
    def save_timer_as (self):
        if self._parent._layer1:
            self._parent._root.bell()
            return 
        
        # probably won't need to catch FileNotFound
        filename = filedialog.asksaveasfilename(defaultextension = '.json', confirmoverwrite = True)
        if filename == "":
            return
        
        self._saver.save_timer(filename)
        self.update_curr_timer_path(filename)
    
    # during a reset, when confirming PB/bests, in misc_menuing, there's the case where the user wants to save 
    # but layer1 = True bc that's what the confirm toplevel wanted
    def save_run (self, force_save = False):
        if self._parent._layer1 and not force_save:
            self._parent._root.bell()
            return 
        
        if self._parent._va._curr_run_path is None:
            self.save_run_as()
            return
        
        # implication is that the user should want to replace an existing file
        if not os.path.isfile(self._parent._va._curr_run_path):
            # TODO: probably should have an error message for invalid path
            self._parent._root.bell()
            return
        
        self._saver.save_run(self._parent._va._curr_run_path)
    
    def save_run_as (self):
        if self._parent._layer1:
            self._parent._root.bell()
            return 
        
        filename = filedialog.asksaveasfilename(defaultextension = '.json', confirmoverwrite = True)
        if filename == "":
            return
        
        self._saver.save_run(filename)
        self.update_curr_run_path(filename)