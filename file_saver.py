'''
Created on June 16, 2021

@author: Jacob H.

save a JSON file to disk based on various current settings
2 kinds of files: one for the timer settings, and one for run data

file_saver.py
'''

import os

class File_saver:
    def __init__ (self, va):
        self._va = va
        
    def update_recents (self):
        if not os.path.isdir("pysplit_settings"):
            os.mkdir("pysplit_settings")
        
        # print(self._va._curr_timer_path + '\n' + self._va._curr_run_path)
        with open(os.path.join('pysplit_settings', 'recents.txt'), 'w') as outfile:
            to_write = self._va._curr_timer_path if self._va._curr_timer_path is not None else ""
            to_write += '\n'
            to_write += self._va._curr_run_path if self._va._curr_run_path is not None else ""
            outfile.write(to_write)
    
    # please use the exact key and value strings, including quote/bracket delimiters (omit colons and new lines, though)
    # use end for commas (which are default) and any closing brackets (but omit new lines, still)
    @staticmethod
    def write_line (outfile, indent : int, key, value, end = ','):
        outfile.write(indent * '  ' + key + ": " + value + end + '\n')
    
    # useful for dealing with commas and stuff
    @staticmethod
    def build_line (indent : int, key, value, end = ','):
        return indent * '  ' + key + ": " + value + end + '\n'
    
    def save_timer (self, path):
        with open(path, 'w') as outfile:
            outfile.write("{\n")
            File_saver.write_line(outfile, 1, '"precision"', str(self._va._timer.get_precision()))
            File_saver.write_line(outfile, 1, '"splits_on_screen"', str(self._va.splits_on_screen))
            File_saver.write_line(outfile, 1, '"prev_splits_on_screen"', str(self._va.num_prev))
            File_saver.write_line(outfile, 1, '"include_last_split"', 'true' if self._va.include_last_split else 'false')

            File_saver.write_line(outfile, 1, '"colors"', '', '{')
            self.save_colors(outfile)

            File_saver.write_line(outfile, 1, '"fonts"', '', '{')
            self.save_fonts(outfile)

            File_saver.write_line(outfile, 1, '"hotkeys"', '', '{')
            self.save_hotkeys(outfile)

            outfile.write("}")
    
    def save_run (self, path):
        with open(path, 'w') as outfile:
            outfile.write("{\n")
            File_saver.write_line(outfile, 1, '"title"', '"' + self._va._timer.get_title() + '"')
            File_saver.write_line(outfile, 1, '"desc"', '"' + self._va._timer.get_description() + '"')
            File_saver.write_line(outfile, 1, '"offset"', str(self._va._timer.get_offset()))
            
            File_saver.write_line(outfile, 1, '"splits"', '', '[')
            self.save_splits(outfile)
            outfile.write("  ]\n")
            
            outfile.write("}")
        
    def save_colors (self, outfile):
        # I sure hope none of these will be Nones
        File_saver.write_line(outfile, 2, '"bg"', '"' + self._va.bg_color + '"')
        File_saver.write_line(outfile, 2, '"mid"', '"' + self._va.mid_color + '"')
        File_saver.write_line(outfile, 2, '"accent"', '"' + self._va.accent_color + '"')
        File_saver.write_line(outfile, 2, '"title"', '"' + self._va.title_color + '"')
        File_saver.write_line(outfile, 2, '"desc"', '"' + self._va.desc_color + '"')
        File_saver.write_line(outfile, 2, '"split"', '"' + self._va.split_text_color + '"')
        File_saver.write_line(outfile, 2, '"lower"', '"' + self._va.lower_text_color + '"')
        File_saver.write_line(outfile, 2, '"time"', '"' + self._va.time_color + '"')
        File_saver.write_line(outfile, 2, '"ahead"', '"' + self._va.ahead + '"')
        File_saver.write_line(outfile, 2, '"behind"', '"' + self._va.behind + '"')
        File_saver.write_line(outfile, 2, '"best"', '"' + self._va.best_color + '"', '},')
        
    def save_fonts (self, outfile):
        File_saver.write_line(outfile, 2, '"title"', '"' + self._va.title_font + '"')
        File_saver.write_line(outfile, 2, '"desc"', '"' + self._va.desc_font + '"')
        File_saver.write_line(outfile, 2, '"split"', '"' + self._va.split_font + '"')
        File_saver.write_line(outfile, 2, '"big_time"', '"' + self._va.big_time_font + '"')
        File_saver.write_line(outfile, 2, '"small_time"', '"' + self._va.small_time_font + '"', '},')
        
    def save_hotkeys (self, outfile):
        to_write = ''
        bindings = self._va._binder._bindings
        for key, value in bindings.items():
            if type(key) is int:
                to_write += File_saver.build_line(2, '"' + value[0] + '"', '[' + str(key) + ', "' + str(value[1]) + '"' + ']')
                
        to_write = to_write[:-2] # omit the ending newline, the penultimate char (comma)
        to_write += '}\n' # basically replace the comma with a curly 
        
        outfile.write(to_write)
        
    @staticmethod
    def translate_none (obj):
        if obj is None:
            return 'null'
        elif type(obj) is str:
            return '"' + obj + '"'
        else: # type(obj) in (int, float)
            return str(obj)
        
    def save_splits (self, outfile):
        splits = self._va._timer._splits
        for i, split in enumerate(splits, 1):
            to_write = '    {\n'
            
            to_write += File_saver.build_line(3, '"name"', File_saver.translate_none(split.get_name()))
            to_write += File_saver.build_line(3, '"last"', File_saver.translate_none(split.get_last_time()))
            to_write += File_saver.build_line(3, '"last_c"', File_saver.translate_none(split.get_last_c_time()))
            to_write += File_saver.build_line(3, '"best"', File_saver.translate_none(split.get_best()), '')
            
            to_write += '    }'
            if i != len(splits):
                to_write += ','
            to_write += '\n'
            
            outfile.write(to_write)
                