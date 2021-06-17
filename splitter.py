'''
Created on Nov 1, 2019

Small edits 11/13/19, 11/14

@author: jacobhuang
splitter.py
'''

from stopwatch import Stopwatch
from split import Split
import helpers
import misc_menuing
from file_menu import File_settings

class SplitOutOfBounds (Exception):
    '''
    Raised when trying to split or unsplit when 1) there are no splits or 2) current is at the end or beginning (respectively)
    '''
    pass
        
        
class Splitter(Stopwatch):
    '''
    Represents the speedrun splitter object that is a collection of split objects. Handles keeping track of time
    with a stopwatch and manages/processes/outputs splits
    '''

    def __init__ (self, visual_assembly = None, size : int = 1, title : str = 'Title', descr : str = 'Description', \
                  precision : int = 1, offset : float = 0.0):
        '''
        Constructor:
            precision and offset are the same as for the Stopwatch constructor

            size is the number of initial splits            
            title is typically going to be the game name
            descr (description) is typically going to be the category
        '''
        Stopwatch.__init__(self, precision, offset)
        # stays constant
        self._original_offset = offset
        # unfortunate, but finish_reset really does need this due to TopLevel async OTHERSTUFF
        # I make it default None just so Splitter works without needing a GUI
        self._va = visual_assembly 
        
        # set title and description
        self._title = title
        self._description = descr
        
        # global time is the sum of all the splits before the current one
        #     since the inherited stopwatch starts "off", global time can be set to 0 (with the proper precision)
        self._global_time = float() if precision > 0 else int()
        # local time is the time of the current split
        self._local_time = offset
        # run time is always _global_time + _local_time
        
        # creates a list of size Splits (with basic/default names)
        #    cannot legally be empty based on what I do in the GUI
        ##### For debugging, create a non-empty _splits list
        self._splits = [Split('Split ' + str(i+1)) for i in range(size)]
        # debug: self._splits[0] = Split('Split 1', 1.0, 1.0, 0.5) # last time, last c time, best time
        
        # index keeping track of which split is the current one; _current is None if there are no splits (which is no longer possible)
        self._current = 0 if size > 0 else None
        
        # set to True when the last split is completed --> time stops updating 
        self._done = False
        
        self._pbed = False
        self._exist_bests = False
        
    
    ######################################################
    # Getters
    ######################################################
    
    def get_title (self):
        return self._title
    
    def set_title(self, title):
        self._title = title
    
    def get_description (self):
        return self._description
        
    def set_description (self, desc):
        self._description = desc
        
    def get_offset (self):
        return self._original_offset
    
    def set_offset (self, off):
        self._original_offset = off # hopefully setting a new offset doesn't break anything... theoretically it shouldn't, I'm sure of the theory
        
    # gets current split from the splits list
    ## maybe consider returning [-1] if current == len (bc that's how ._done becomes True) (also, this would affect VA in that a try-except
    #    isn't needed anymore
    def current_split (self):
        if self._current is not None and self._current <= len(self._splits):
            if self._current == len(self._splits):
                return None
            return self._splits[self._current]
        raise SplitOutOfBounds
    
    def current_index (self):
        return self._current
        
    # get the list of all splits
    def get_all_splits (self):
        return self._splits
    
    # gets split of specified index (This may not actually get used)
    def get_split (self, index : int):
        return self._splits[index]
    
    # answers: "How long have the previous splits taken?"
    def get_global_time (self):
        return self._global_time
    
    # answers: "How long has the current split been running?"
    def get_local_time (self):
        self.update()
        return self._local_time
    
    # answers: "How long has this current split been going, but with nice hrs-mins-secs formatting and required precision?"
    def get_disp_local_time (self):
        self.update()
        if self._done:
            return helpers.s_to_hms(self[-1].get_time(), self._precision)
        return helpers.s_to_hms(self._local_time, self._precision)
    
    # answers: "How long has the whole run been going?"
    def get_run_time (self):
        self.update()
        return self._local_time + self._global_time
    
    # answers: "How long has the whole run been going, but with nice hrs-mins-secs formatting and required precision?"
    def get_disp_run_time (self):
        self.update()
        return helpers.s_to_hms(self._local_time + self._global_time, self._precision)
    
    # answers: "What is the best possible time?"
    #     specifically, get the cumulative time of the splits you've already completed, then add the best splits of all futures splits"
    def get_disp_best_poss (self):
        total = self.get_global_time()
        for split in self._splits[self._current:]: # not a problem if current == len(splits) bc it's a slice
            time = split.get_best()
            if time is None:
                return '-'
            total += time
        
        return helpers.s_to_hms(total, self._precision) 
    
    # answers: "What is the sum of all best splits?"
    def get_disp_sum_best (self):
        # if there are missing best splits, then this value will be nonexistent
        total = 0
        for split in self._splits:
            time = split.get_best()
            if time is None:
                return '-'
            total += time
            
        return helpers.s_to_hms(total, self._precision)
        
    
    # answers: "Has start been pressed after a reset or initialization?"
    #      2020 question: uh... it seems this assumes offset is negative? bc there's a chance it may return true if offset > 0??
    #        idk for sure or not... idr the use cases of this function
    #        idk there's no use of is_reset in this source code file. it's used in splitter_interface fyi 
    #    I think maybe one way to make it 100% correct is to use another check for the _on flag == False (from Stopwatch)
    #        or... maybe this is okay and already works if we assume original_offset doesn't ever change
    #        bc it's like... if offset = 2, then it's not like you'll ever be able to start at 0 and go up to 2... bc you start at 2
    def is_reset (self):
        # 2021: i literally have a .is_on() check in the parent class..., why not just add an extra check? past me didn't see a reason not to 
        return self._original_offset == self.get_run_time() and not self.is_on()
    
    ######################################################
    # Setters/Mutators
    ######################################################
    
    # inherits Stopwatch.start, Stopwatch.pause, Stopwatch.get_time
    
    # rip run, should check for best splits as well
    def reset (self, menu = None):
        self._pbed = self._done and len(self._splits) and \
            (self._splits[-1].get_last_c_time() is None or self.get_run_time() < self._splits[-1].get_last_c_time())
        tied = self._done and len(self._splits) and self.get_run_time() == self._splits[-1].get_last_c_time() # lol tied 
        #############################################################################
        # probs should ask user if they want to replace prev run if tied, then just 
        # manually set pbed = True
        #############################################################################
        self._exist_bests = any(split.is_a_best() for split in self._splits)
        
        # don't assume if they PB'ed, they wanna adjust their best splits as well 
        if menu is not None and self._pbed:
            # misc menuing will call mid_reset if the user chooses no
            # misc menuing will skip to finish_reset if the user chooses yes
            misc_menuing.confirm_pb(menu, self) 
        # elif menu is not None and self._exist_bests:
        #    misc_menuing.confirm_best(menu, self)
        else:
            # self.finish_reset()
            self.mid_reset(menu)
        
    def mid_reset (self, menu):
        if menu is not None and self._exist_bests:
            # misc menuing will call finish_reset when the user closes the window
            misc_menuing.confirm_best(menu, self) 
        else:
            self.finish_reset()
        
    def finish_reset (self, menu_for_saving = None):
        for split in self._splits:
            if self._pbed:
                split.we_pbed()
            # also assume if you wanna save a PB you also wanna save your best splits from that run duh
            # things you can have: 
            #    both are False
            #    pbed is False, but exist_bests is True
            #    pbed is True (and exist_bests is implicitly True)
            # thing you can't have:
            #    pbed is True but exist_bests is False (i.e. if there are bests but you don't overwrite), logically doesn't make sense to allow
            #    (naturally you can pb without any best splits, that's fine and accounted for)
            elif self._exist_bests:
                split.set_time_as_best()
            split.set_time(None)
            split.set_c_time(None)
            
        Stopwatch.reset(self, self._original_offset)
        self._global_time = float() if self._precision > 0 else int()
        # this is wrong??
        # self._local_time = float() if self._precision > 0 else int()
        self._local_time = self._original_offset
        
        self._done = False
        self._pbed = False
        self._exist_bests = False
            
        self._current = 0 if len(self._splits) > 0 else None
        
        # I'm not too confident about when to save... that being said, this is closest to just a regular old
        # "I've hit reset already, and nothing's happening and now I want to save"
        if menu_for_saving is not None:
            File_settings(menu_for_saving).save_run(True)
        
        if self._va is not None:
            self._va.update_all()
    
    # reassigns local time, I think is what should happen?
    def update (self):
        if not self._done:
            self._local_time = self.get_time()
    
    # save the split time in the current split; go to the next split, if already on the last split, do nothing 
    #    overrides Stopwatch.split
    def split (self):
        if self._current is not None and self._current < len(self._splits): # current_split() doesn't quite check this, so it's now needed
            split_time = Stopwatch.split(self, 0.0) #I don't yet know if having a required offset argument is a good idea in any useful situation
            self.current_split().set_time(split_time)
            self.current_split().set_c_time(self._global_time + split_time)
            
            self._current += 1
            self._global_time += split_time
            self._local_time = float() if self._precision > 0 else int()
            if (self._current == len(self._splits)):
                self._done = True
        else:
            raise SplitOutOfBounds
            
    # goes back one split and adds the current split time to the previous split's recorded time
    def unsplit (self):
        if self._current is not None and self._current > 0:
            self._done = False
            self.update()
            self._current -= 1
            prev_time = self.current_split().get_time()
            # "splits" the Stopwatch by offsetting to the current split time + the previous split time (if it exists) and deleting the previous split time
            Stopwatch.split(self, self._local_time + (prev_time if prev_time is not None else 0))
            self.current_split().set_time(None)
            self.current_split().set_c_time(None)
            
            self._global_time -= prev_time if prev_time is not None else 0
            self._local_time += prev_time if prev_time is not None else 0
        else:
            raise SplitOutOfBounds
    
    # skips forward one split and adds the current split time to the next split
    def skip_split (self):
        # shouldn't be able to skip the last split
        if self._current is not None and self._current < len(self._splits) - 1:
            self._current += 1
            # Stopwatch.split(self, Stopwatch.get_time(self))
        else:
            raise SplitOutOfBounds
    
    # iterate through the list of splits (the only thing you can really even iterate through)
    def __iter__ (self):
        return iter(self._splits)

    def __len__ (self):
        return len(self._splits)
    
    def __getitem__ (self, index):
        return self._splits[index]
        
    # methods to check flags like "on a run" or "finished"?
    
    
    
    
    
# testing/debug
if __name__ == '__main__':

    def all_times (splitter):
        print ('global time =', str(splitter.get_global_time()))
        print ('local time =', str(splitter.get_local_time()))
        print ('run time =', str(splitter.get_run_time()))
        print()
        
    print('\n==================\n= test title/desc/basic splits\n==================')
    splitter = Splitter(3, 'OoT', 'hundo', 2, -2.0)
    print(splitter.get_title() + ":", splitter.get_description(), end = '\n\n')
    for split in splitter:
        print(split.get_name())
    
    print('\n==================\n= test negative offset and initialization\n==================')
    splitter.start()
    all_times(splitter)         # glob = 0 local = -2 run = -2
    
    print ('==================\n= test start and Splitter update\n==================')
    while (splitter.get_run_time() < 0):
        pass
    all_times(splitter)         # glob = 0, local = 0, run = 0
    
    print('==================\n= test pause\n==================')
    splitter.pause()
    stopwatch = Stopwatch(on = True) # delay 1.5 s
    while (stopwatch.get_time() < 1.5):
        pass
    stopwatch.pause()
    all_times(splitter)         # glob = local = run = 0
    print('delay =', stopwatch.get_time(), 'sec') # delay = 1.5 sec
    
    print('\n==================\n= test split\n==================')
    splitter.start()
    while (splitter.get_run_time() < 1.5):
        pass
    all_times(splitter)         # glob = 0, local = 1.5, run = 1.5
    splitter.split()
    all_times(splitter)         # glob = 1.5, local = 0, run = 1.5
    
    while (splitter.get_run_time() < 2.0):
        pass
    splitter.split()
    all_times(splitter)         # glob = 2.0, local = 0, run = 2.0
    
    while (splitter.get_run_time() < 3.0):
        pass
    splitter.split()
    all_times(splitter)         # glob = 3.0, local = 0, run = 3.0
    
    try:
        splitter.split()
        print('whooops')
    except SplitOutOfBounds:
        print('can\'t split at the end')
        
    print('\n==================\n= test unsplit\n==================')
    splitter.unsplit()
    all_times(splitter)         # glob = 2.0, local = 1.0, run = 3.0
    splitter.unsplit()
    all_times(splitter)         # glob = 1.5, local = 1.5, run = 3.0
    splitter.unsplit()
    all_times(splitter)         # glob = 0, local = 3.0, run = 3.0
    try:
        splitter.unsplit()
        print('whoops')
    except SplitOutOfBounds:
        print('can\'t unsplit at the beginning\n')
        
    while (splitter.get_run_time() < 4.0):
        pass
    splitter.split()
    all_times(splitter)         # glob = 4.0, local = 0.0, run = 4.0
    
    print('==================\n= test skip split\n==================')
    splitter.skip_split()
    all_times(splitter)         # glob = 4.0, local = 0.0, run = 4.0
    while (splitter.get_run_time() < 4.51):
        pass
    try: 
        splitter.skip_split()
        print('whoops')
    except SplitOutOfBounds:
        print('can\'t skip last split\n')
    splitter.split()
    all_times(splitter)         # glob = 4.51, local = 0.0, run = 4.51

    try:
        splitter.split()
        print('whoops')
    except SplitOutOfBounds:
        print('can\'t split at the end')
        