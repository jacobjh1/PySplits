'''
Created on June 16, 2021

@author: Jacob H.

load a JSON file from disk and use it to populate various settings
2 kinds of files: one for the timer settings, and one for run data

file_loader.py
'''

import json
from collections import defaultdict
from split import Split

class File_loader:
    def __init__ (self, va):
        self._va = va
        
    def path_to_dict (self, path):
        infile = open(path, 'r')
        return (infile, json.load(infile))

    def get_timer (self, path):
        try:
            infile, timer_prefs = self.path_to_dict(path)
        except json.decoder.JSONDecodeError as e:
            # TODO: print(e)-ish to explain the syntax error - try message box this time?
            # self._va._root.bell() actually maybe I should let the caller handle the exceptions?
            # also implies maybe I should move the error handling try/except to path_to_dict
            #    note visual_assembly, end of __init__ and file_menu in various places all may need to deal with decode error...
            #    so that's another argument towards handling syntax errors here, then maybe reraising the error anyway
            raise e
        except Exception as e:
            print(type(e))
            raise e
            
        # question: should I reset the timer or anything like that? I don't think it's really necessary
        # since this part is all just cosmetic 
        # should probably make sure that there are no other menus open?
            
        # defaults in case the file didn't have the info 
        self._va._timer.set_precision(1)
        self._va.splits_on_screen = 4
        self._va.num_prev = 2
        self._va.include_last_split = True
        
        if "precision" in timer_prefs:
            self._va._timer.set_precision(timer_prefs["precision"])
            
        if "splits_on_screen" in timer_prefs:
            self._va.splits_on_screen = timer_prefs["splits_on_screen"]
            
        if "prev_splits_on_screen" in timer_prefs:
            self._va.num_prev = timer_prefs["prev_splits_on_screen"]
            
        if "include_last_split" in timer_prefs: 
            self._va.include_last_split = timer_prefs["include_last_split"]
            
        # assume "colors" in timer_prefs:
        self.get_colors(defaultdict(lambda: "black", timer_prefs["colors"]))
        
        # assume "fonts" in timer_prefs:
        self.get_fonts(defaultdict(lambda: "TkDefaultFont", timer_prefs["fonts"]))
        
        # assume "hotkeys" in timer_prefs:
        self.get_hotkeys(defaultdict(lambda: None, timer_prefs["hotkeys"]))
        
        self._va.update_all()
        self._va.update_fonts_colors()
        
        infile.close()       
    
    def get_run (self, path):
        try:
            infile, run_data = self.path_to_dict(path)
        except json.decoder.JSONDecodeError as e:
            # TODO: print(e)-ish to explain the syntax error - try message box this time? 
            # self._va._root.bell() actually maybe I should let the caller handle the exceptions?
            raise e
        except Exception as e:
            print(type(e))
            raise e
        
        # defaults
        self._va._timer.set_title("Untitled Run")
        self._va._timer.set_description("")
        self._va._timer.set_offset(0)
        
        if "title" in run_data:
            self._va._timer.set_title(run_data["title"])
            
        if "desc" in run_data:
            self._va._timer.set_description(run_data["desc"])
            
        if "offset" in run_data:
            self._va._timer.set_offset(run_data["offset"])
        
        # assume even with 0 splits, you have an empty list
        self.get_splits(run_data["splits"])
        
        self._va.update_all()
        self._va.update_fonts_colors()
        
        infile.close()
    
    def get_colors (self, colors):
        self._va.bg_color = colors["bg"]
        self._va.mid_color = colors["mid"]
        self._va.accent_color = colors["accent"]
        self._va.title_color = colors["title"]
        self._va.desc_color = colors["desc"]
        self._va.split_text_color = colors["split"]
        self._va.lower_text_color = colors["lower"]
        self._va.time_color = colors["time"]
        self._va.ahead = colors["ahead"]
        self._va.behind = colors["behind"]
        self._va.best_color = colors["best"]
    
    def get_fonts (self, fonts):
        self._va.title_font = fonts["title"]
        self._va.desc_font = fonts["desc"]
        self._va.split_font  = fonts["split"]
        self._va.big_time_font = fonts["big_time"]
        self._va.small_time_font = fonts["small_time"]
    
    def get_hotkeys (self, hotkeys):
        bindings = self._va._binder._bindings
        bindings.clear() # maintains the same address as _bindings
        
        for action, (keynum, keyname) in hotkeys.items():
            bindings[keynum] = (action, keyname)
            bindings[action] = keynum
    
    def get_splits (self, new_splits):
        old_splits = self._va._timer._splits    
        old_len = len(old_splits)
        new_len = len(new_splits)
        old_splits.clear()
        
        # print('on screen are', old_len, 'splits')
        # print('next, I want', new_len, 'splits')
        
        if new_len == 0:
            old_splits.append(Split()) # splits can't legally be empty
        else:
            for split in new_splits:
                # I assume null in JSON converts to None in Python?
                old_splits.append(Split(split["name"], split["last"], split["last_c"], split["best"]))
        
        if new_len < old_len:
            self._va.remove_splits(new_len)
        elif new_len > old_len:
            self._va.add_splits(new_len)