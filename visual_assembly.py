'''
Created on Nov 9, 2019
Edited 11/10/19, 11/12
Minor Edits 11/14
Edited 12/19/2020, 12/20 (changed from .pack (see old_versions) to .grid)
Been working on and off, maybe every other day on average up to 1/3/21 (last day of winter break)
Edited 6/14/2021 (summer break rn, just did some minor cosmetic changes to menu logic)

@author: Jacob H.

Given the various [widget]_variants.py files, construct, assemble, and update the widgets on a root (or other) window

visual_assembly.py
'''

#############################################################################
# TODO (non-exhaustive)
# 1) saving (JSON format??) - timer settings separate from run settings??
# 2) colors
# 3) attempt counter
#
# 3) consider allowing certain Run menu functions to occur while the timer is not reset
#    and consider allowing some key presses while certain menus are open
# 4) go look at the comment box over in splitter.reset about PB/best splits
#
# ∞) graphs
#############################################################################

from tkinter import Tk, Frame, Label, StringVar
from tkinter.font import Font
from tkinter import TOP, BOTTOM, LEFT, RIGHT, BOTH, X, Y, N, S, E, W

from splitter import Splitter
from key_binding import Binder
from splitter_interface import SplitterInterface
from menus import MenuSystem

# VA for VisualAssembly
class VA:
    
    '''
    Set Up all the variables... except uh... if I want to have the potential for > 1 Splitter at once w/ independent settings...
    these might need to become instance variables, not class variables
    '''
        
    def __init__ (self):
        # assign constants
        self.splits_on_screen = 4
        self.num_prev = 2
        self.include_last_split = True
        self.bg_color = 'black'
        self.mid_color = 'white'
        self.app_color = 'grey'
        self.main_font_color = 'black'
        self.second_font_color = 'white'
        self.time_color = 'green'
        self.ahead = 'green'
        self.behind = 'red'
        self.best_color = 'blue'
        
        
        # Splitter(size, title, descr, precision, offset)
        # For debuggging, use a non-zero-argument Splitter 
        self._timer = Splitter(7, 'OoT', 'hundo', 2, 0.0, self)
        
        
        # what's being created      # what instance variables are being created/set 
        
        # root window        
        self.make_root()            # self._root
        # various frames
        self.put_header()           # self._header_frame and self._header
        self.put_splits()           # self._splits_frame and self._splits_slice
        self.put_clock()            # self._time_frame, self._total_time_str, and self._split_time_str
            # i think clock will end up being a bit of a misnomer - it's more like the clock + current split info probably
        self.put_stats()
        
        # allow hotkey bindings
        self._binder = Binder(self._root, self._timer)
        
        
        # make menus
        self._menus = MenuSystem(self._root, self._timer, self._timer.get_all_splits(), self._binder, self)
        # make menus visible
        self._root.config(menu=self._menus._menu_bar)
        self._root.option_add('*tearOff', False) # tkdocs highly recommends this
        
        # the menus might eventually need to come before this
        self._splitter_interface = SplitterInterface(self._timer, self._binder.get_bindings_dict(), self._root, self, self._menus)
        
    def make_root (self):
        self._root = Tk()
        #WIP
        self._root.title("PySplits")
        # probably will need to change the quit function to a more complicated clean-up function
        self._root.protocol('WM_DELETE_WINDOW', self._root.destroy)
        self._root['bg'] = self.bg_color
        # change default app dimensions/size here
        self._root.geometry('250x500') # width x height, rn it's arbitrary
    
    def put_header (self):
        # all these "put" functions set up the geometry of the rows/cols
        # then over in "update," the values are updated w/o much (if any) regard for the geometry. It's pretty nice this way
        #    I imagine in the future, with more toggle-able/configurable options, put can just be run again with everything the same
        #    except for those toggled values/constants
        
        self._header_frame = Frame(self._root, bg = self.app_color)
        self._header_frame.grid(row = 0, column = 0, sticky = (N, E, W), pady = (5, 10))
        
        # weight 0 is by default; header looks nicer when it has a constant height
        #self._root.rowconfigure(0, weight = 0)
        self._root.columnconfigure(0, weight = 1)
        
        # one row for title, one row for desc
        self._title = Label(self._header_frame, bg = self.app_color, fg = self.main_font_color)
        self._title.grid(row = 0, column = 0, sticky = (E, W))
        
        self._desc = Label(self._header_frame, bg = self.app_color, fg = self.main_font_color)
        self._desc.grid(row = 1, column = 0, sticky = (E, W))

        self._header_frame.rowconfigure(0, weight = 1)       
        self._header_frame.rowconfigure(1, weight = 1)
        self._header_frame.columnconfigure(0, weight = 1)
        
        self.update_header()
        
    def update_header (self):
        self._title['text'] = self._timer.get_title()
        self._desc['text'] = self._timer.get_description()
        self._title['bg'] = self._desc['bg'] = self.app_color
        self._title['fg'] = self._desc['fg'] = self.main_font_color
        
    def put_split(self, frame, rowi):
        name = Label(frame, bg = self.app_color, fg = self.main_font_color)
        delta = Label(frame, bg = self.app_color, fg = self.main_font_color)
        time = Label(frame, bg = self.app_color, fg = self.main_font_color)
        
        # don't technically need the pady here
        name.grid(row = rowi, column = 0, padx = (4, 0), pady = 2, sticky = (N, S, E, W))
        delta.grid(row = rowi, column = 1, padx = (0, 0), pady = 2, sticky = (N, S, E, W))
        time.grid(row = rowi, column = 2, padx = (0, 4), pady = 2, sticky = (N, S, E, W))
            
        frame.rowconfigure(rowi, weight = 1)    
    
    def put_splits (self):        
        self._splits_frame = Frame(self._root, bg = self.mid_color)
        self._splits_frame.grid(row = 1, column = 0, sticky = (N, S, E, W)) 
        self._root.rowconfigure(1, weight = 1)
        
        self._splits_slice = slice(0, self.splits_on_screen)
        # the comment off to the right referenced the fact that put_splits relies on the timer's splits syncing up with what's on screen/gridded
        #    bc sometimes put_splits might be run after a menu move involving splits
        maximum = min(self.splits_on_screen, len(self._timer)) # using _timer is ok here bc this fxn is only run once at start up
        #maximum = self.splits_on_screen
        for row in range(maximum):
            self.put_split(self._splits_frame, row)
   
        self._splits_frame.columnconfigure(0, weight = 1)
        self._splits_frame.columnconfigure(1, weight = 1)
        self._splits_frame.columnconfigure(2, weight = 1)
        
        self.update_splits()
        
    # used over in splitter_interface 
    def set_splits_slice (self, new_start, new_stop):
        self._splits_slice = slice(new_start, new_stop)
    
    def update_splits(self):
        current = self._timer.current_index()
            
        future = False
        p = self._timer.get_precision()
                        
        splits = self._timer[self._splits_slice]
        for i, split, name, delta, time in zip(range(self._splits_slice.start, self._splits_slice.stop), splits, 
                                     reversed(self._splits_frame.grid_slaves(column = 0)), # i literally hate this terminology no joke
                                     reversed(self._splits_frame.grid_slaves(column = 1)), # idk why it's reverse gridded/packed order...
                                     reversed(self._splits_frame.grid_slaves(column = 2))):
            if not future and i >= current:
                future = True
            
            delta_text = split.get_disp_delta(p)
            
            # i should probably make a helper function in split.py to get the color; I use it at least 3 times
            if len(delta_text) == 1:
                color = self.main_font_color
            elif delta_text[2] == '+':
                color = self.behind
            else: # delta_text[2] == '-':
                color = self.ahead
            if split.is_a_best():
                color = self.best_color
            
            name.configure(text = split.get_name())
            delta.configure(text = delta_text, fg = color)
            time.configure(text = split.get_disp_time(p, future))
            
            # even borders omg finally
            if i == self._splits_slice.start:
                name.grid(pady = (4, 2))
                delta.grid(pady = (4, 2))
                time.grid(pady = (4, 2))
            elif i == self._splits_slice.stop - 1:
                name.grid(pady = (2, 4))
                delta.grid(pady = (2, 4))
                time.grid(pady = (2, 4))
            else:
                name.grid(pady = 2)
                delta.grid(pady = 2)
                time.grid(pady = 2)
            
        if self.include_last_split:
            # again, another reason why splits need to be >0 in length (there was the reason in the menu GUI also)
            last_split = self._timer[-1]
            future = current != len(self._timer) # if current is length, then the run is finished, so future = False
            # split_name 
            self._splits_frame.grid_slaves(column = 0)[0].configure(text = last_split.get_name())
            
            # split_delta
            delta_text = last_split.get_disp_delta(p)
            if len(delta_text) == 1:
                color = self.main_font_color
            elif delta_text[2] == '+':
                color = self.behind
            else: # delta_text[2] == '-':
                color = self.ahead
            if last_split.is_a_best():
                color = self.best_color
            self._splits_frame.grid_slaves(column = 1)[0].configure(text = delta_text, fg = color)
            # split_time
            self._splits_frame.grid_slaves(column = 2)[0].configure(text = last_split.get_disp_time(p, future))
    
    # used if we need to ungrid some splits (used over in menus)
    # num = number of splits on screen
    def remove_splits (self, num):
        # no reversed() present actually means reversed order
        #maximum = min(self.splits_on_screen, len(self._splits_frame.grid_slaves(column = 0)))
        #r = range(maximum - num, 0, -1)
        #r = range(maximum - 1, num - 1, -1)
        current = len(self._splits_frame.grid_slaves(column = 0))
        r = range(current - 1, num - 1, -1)
        #print(maximum, num)
        for i, name, delta, time in zip(r, self._splits_frame.grid_slaves(column = 0), self._splits_frame.grid_slaves(column = 1),
                                        self._splits_frame.grid_slaves(column = 2)):
            #print(i, name['text'])
            name.grid_forget()
            delta.grid_forget()
            time.grid_forget()
            self._splits_frame.rowconfigure(i, weight = 0)
            
    # used if we need to grid some splits (used over in menus)
    # num = number of splits on screen
    def add_splits (self, num):
        #maximum = min(self.splits_on_screen, len(self._timer))
        #maximum = self.splits_on_screen
        current = len(self._splits_frame.grid_slaves(column = 0))
        while current < num and current < min(self.splits_on_screen, len(self._timer)):
            #print(current)
            self.put_split(self._splits_frame, current)
            current += 1
    
    def put_clock (self):        
        self._time_frame = Frame(self._root, bg = self.bg_color)
        self._time_frame.grid(row = 2, column = 0, sticky = (E, W), pady = 5)
        self._root.rowconfigure(2, pad = 5) # weight = 0 
        
        self._total_time_str = StringVar()
        f_big = Font(self._time_frame, size = 30)
        self._total_time_lbl = Label(self._time_frame, textvar = self._total_time_str, bg = self.bg_color, fg = self.time_color, font = f_big)
        self._total_time_lbl.grid(row = 0, column = 0, sticky = E)
        
        self._split_time_str = StringVar()
        f_small = Font(self._time_frame, size = 20)
        self._split_time_lbl = Label(self._time_frame, textvar = self._split_time_str, bg = self.bg_color, fg = self.time_color, font = f_small)
        self._split_time_lbl.grid(row = 1, column = 0, rowspan = 3, sticky = E)
        
        self._split_name_str = StringVar()
        self._split_name_lbl = Label(self._time_frame, textvar = self._split_name_str, bg = self.bg_color, fg = self.second_font_color)
        self._split_name_lbl.grid(row = 1, column = 0, sticky = W)
        
        self._split_pb_str = StringVar()
        self._split_pb_lbl = Label(self._time_frame, textvar = self._split_pb_str, bg = self.bg_color, fg = self.second_font_color)
        self._split_pb_lbl.grid(row = 2, column = 0, sticky = W)
        
        self._split_best_str = StringVar()
        self._split_best_lbl = Label(self._time_frame, textvar = self._split_best_str, bg = self.bg_color, fg = self.second_font_color)
        self._split_best_lbl.grid(row = 3, column = 0, sticky = W)
        
        self._time_frame.columnconfigure(0, weight = 1)
        
        self.update_clock()
    
    def update_clock (self):
        self._total_time_str.set(self._timer.get_disp_run_time())
        self._split_time_str.set(self._timer.get_disp_local_time())
        
        current = self._timer.current_split()
        if current is None:
            current = self._timer[-1] # just for now, idk what I want this case to be exactly # "this" being the case where 
            # you're at the end of the run and the current split little display thingie shows some kind of times
        
        self._split_name_str.set(current.get_name())
        
        prec = self._timer.get_precision()
        pb = current.get_disp_last(prec)
        if pb is None:
            pb = '-'
        self._split_pb_str.set('PB: ' + pb)
        
        best = current.get_disp_best(prec)
        if best is None:
            best = '-'
        self._split_best_str.set('Best: ' + best)
        
    def put_stats (self):
        self._stats_frame = Frame(self._root, bg = self.bg_color)
        self._stats_frame.grid(row = 3, column = 0, sticky = (E, W), pady = 5)
        self._root.rowconfigure(3, pad = 5)
        
        # What do I want here? Possible time save, Previous segment (delta), best possible and sum of best
        self._tsv = Label(self._stats_frame, text = 'possible time save: ', bg = self.bg_color, fg = self.second_font_color)
        self._tsv.grid(row = 0, column = 0, sticky = W)
        self._time_save_str = StringVar()
        self._time_save_lbl = Label(self._stats_frame, textvar = self._time_save_str, bg = self.bg_color, fg = self.second_font_color)
        self._time_save_lbl.grid(row = 0, column = 1, sticky = W)
        
        self._pdel = Label(self._stats_frame, text = 'previous segment: ', bg = self.bg_color, fg = self.second_font_color)
        self._pdel.grid(row = 1, column = 0, sticky = W)
        self._prev_delta_str = StringVar()
        self._prev_delta_lbl = Label(self._stats_frame, textvar = self._prev_delta_str, bg = self.bg_color, fg = self.second_font_color)
        self._prev_delta_lbl.grid(row = 1, column = 1, sticky = W)
        
        self._bpos = Label(self._stats_frame, text = 'best possible time: ', bg = self.bg_color, fg = self.second_font_color)
        self._bpos.grid(row = 2, column = 0, sticky = W)
        self._best_poss_str = StringVar()
        self._best_poss_lbl = Label(self._stats_frame, textvar=  self._best_poss_str, bg = self.bg_color, fg = self.second_font_color)
        self._best_poss_lbl.grid(row = 2, column = 1, sticky = W)
        
        self._sbest = Label(self._stats_frame, text = 'sum of best splits: ', bg = self.bg_color, fg = self.second_font_color)
        self._sbest.grid(row = 3, column = 0, sticky = W)
        self._sum_best_str = StringVar()
        self._sum_best_lbl = Label(self._stats_frame, textvar = self._sum_best_str, bg = self.bg_color, fg = self.second_font_color)
        self._sum_best_lbl.grid(row = 3, column = 1, sticky = W)
        
        #self._stats_frame.columnconfigure(0, weight = 1)
        self._stats_frame.columnconfigure(1, weight = 1)
        
        self.update_stats()
    
    def update_stats (self):
        prec = self._timer.get_precision()
        
        # possible time save
        current = self._timer.current_split()
        if current is None:
            secs = '-'
        else:
            secs = current.get_disp_poss_time_save(prec)
        if secs is None:
            secs = '-'
        self._time_save_str.set(secs)
        
        # previous segment diff/delta
        previous = self._timer.current_index() - 1
        if previous < 0:
            delta = '-'
        else:
            delta = self._timer[previous].get_disp_prev_delta(prec)
        if delta[0] == '+':
            color = self.behind
        elif len(delta) > 1 and delta[0] == '-':
            color = self.ahead
        else:
            color = self.second_font_color
        if self._timer[previous].is_a_best():
            color = self.best_color
        self._prev_delta_str.set(delta)
        self._prev_delta_lbl.configure(fg = color)
        
        # best possible time
        self._best_poss_str.set(self._timer.get_disp_best_poss())
        
        # sum of best splits
        self._sum_best_str.set(self._timer.get_disp_sum_best())

    def update_all (self):
        self.update_header()
        self.update_clock()
        self.update_splits()
        self.update_stats()

    def va_main_loop (self):
        # Update view based on controller stuff
        # self.update_header()
        
        # so I was kinda thinking... I don't really need to do all of these things once every 10 ms... right? I might
        #     be able to do update_header and update_splits only when they need to change. Might save a bunch of resources
        #     bc really, only the update_clock needs to constantly run, and everything else can be asynchronous.
        # would it really be that hard to find the various times the display needs to update? Wouldn't it just be after the various menu saves?
        # 
        # though I do think the init's put_X's ought to call update_X() if I do make the updates asynchronous  
        # 
        # I can also save resources by only doing update_clock while timer.on == True
        if self._timer.is_on():
            self.update_clock()
        # self.update_splits()
        # self.update_stats()
        
        # update visuals (view stuff i.e. working with _root now)
        ##### also, um... this could be part of the if... then I'd also need to add a root.update to update_all()
        ##### but idk how expensive root.update is so I'll just leave it like this for now 
        self._root.update()
        # parameters: every x ms, what fxn, what argument(??) (part of ** parameter I think)
        #    2021: pretty sure ** actually refers to potential args that are passed to this very va_main_loop fxn, not that I have any
        self._root.after(10, self.va_main_loop)
        
if __name__ == "__main__":
    v = VA()
    v.va_main_loop()
    v._root.mainloop()
