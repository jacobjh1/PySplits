'''
Created on Nov 1, 2019

Minor Edits 11/14/19

@author: jacobhuang
split.py
'''

import helpers

class Split:
    '''
    Represents a split object with a name, best_time, and time; can access/mutate all instance variables
    '''

    def __init__(self, name : str = '<No name>', 
                 last_time : 'float or int' = None, last_cumulative_time : 'float or int' = None,
                 best_time : 'float or int' = None):
        
        '''
        Constructor: creates a named Split with an optional best_time parameter  
        Note that times are either int or float, but Split doesn't really care because Stopwatch does all that work 
        Also note that times are in seconds, and are only converted to h:m:s.xxx via s_to_hms_string()
        '''
        
        ##########################################################################################
        # Ok so...
        # the only really important thing is _time and maybe last_c_time?
        # 
        # my question's this: what values actually get displayed?
        #    last_c_time is displayed by default - before the split is completed
        #        just a - if last_c_time DNE (i.e. is None)
        #    (c_time - last_c_time) is displayed after splitting
        #        just c_time is last_c_time DNE
        # 
        ##########################################################################################
        
        # name of the split
        self._name = name
        
        # the time from the last run (PB/whatever) to compare against (for this split)
        self._last_time = last_time
        
        # the time from the last run (PB/whatever) to compare against (cumulative up to this point) 
        self._last_c_time = last_cumulative_time
        
        # the best ever time that this split was completed in
        self._best_time = best_time
        
        # so this one's a bit weird... in order to do some calculations (in menu, notably), we need the most recent, non-None cumulative time
        #     it does require a notion of split ordering, so Splitter'll have to take care of it
        # I do set the default to 0 and not None bc initial offset tends to be 0, and the offset is a good default, say, if you have an
        # empty timer
        #
        # of course, with ordering means lots of annoying O(N) traversals to update all future splits with the same last_existing as this one
        # (when you update this one's last_existing)
        #
        # and this value is only useful when _last_c_time == None
        #
        # course, idk if this'll actually be useful now that I think about it. But I'll leave it here, w/o getters or setters for the time being
        # self._last_existing_c = last_existing_last_c_time
        
        # the time it took to finish this split; while the split is in progress/hasn't been reached, self._time is None
        self._time = None
        
        # cumulative time (i.e. total time up until this point)
        self._c_time = None
        
        
    # whole bunch of getters and setters is really all Split needs
    def set_name (self, new_name : str):
        self._name = new_name
        
    def get_name (self):
        return self._name
    
    def set_time (self, time): #not just float/int, it's also str in hh:mm:ss.x format
        # assume any str is in the proper format
        # tho I dunno if set_time() will ever receive a string argument in practice... this and set_c_time()
        if type(time) is str:
            self._time = helpers.hms_to_s(time)
        else:
            self._time = time
        
    def get_time (self):
        return self._time
    
    def set_c_time (self, time):
        if type(time) is str:
            self._c_time = helpers.hms_to_s(time)
        else:
            self._c_time = time
        
    def get_c_time (self):
        return self._c_time
    
    def set_last_time (self, time):
        if type(time) is str:
            self._last_time = helpers.hms_to_s(time)
        else:
            self._last_time = time
        
    def get_last_time (self):
        return self._last_time
    
    def set_last_c_time (self, time):
        if type(time) is str:
            self._last_c_time = helpers.hms_to_s(time)
        else:
            self._last_c_time = time
        
    def get_last_c_time (self):
        return self._last_c_time
    
    # oops i have 2 setters for best w slightly different functionality
    #     this one's for when you manually overwrite a best time
    #     the one below (set time as best) is for taking the current split time and overwriting it
    def set_best (self, best):
        if type(best) is str:
            self._best_time = helpers.hms_to_s(best)
        else:
            self._best_time = best
        
    def get_best (self):
        return self._best_time
    
    def is_a_best (self):
        return (self._best_time is None and self._time is not None) or (self._time is not None and self._time < self._best_time)
    
    #### display versions of times, not really sure if the regular getters are ever used...
    
    def get_disp_last (self, precision):
        return None if self._last_time is None else helpers.s_to_hms(self._last_time, precision)
    
    def get_disp_last_c (self, precision):
        return None if self._last_c_time is None else helpers.s_to_hms(self._last_c_time, precision)
    
    def get_disp_best (self, precision):
        return None if self._best_time is None else helpers.s_to_hms(self._best_time, precision)
    
    # get the possible time save for this split: it's the PB split time - best time
    def get_disp_poss_time_save (self, precision):
        if self._last_time is None: # if last_time isn't None, then best_time must be a number
            return None
        else: 
            return helpers.s_to_hms(self._last_time - self._best_time, precision)
    
    # get the time saved/lost on just the split (generally some prev split, but this function is a general one)
    def get_disp_prev_delta (self, precision):
        if self._time is None:
            return '-'
        elif self._last_time is None:
            return '-'
        else:
            behind = '+' if self._time >= self._last_time else ''
            return behind + helpers.s_to_hms(self._time - self._last_time, precision)

    # get the time saved/lost overall (cumulative times)
    #     to be called by visual assembly, see the big red bold comment for comments about display time
    #    this is practically identical to get_disp_prev_delta()
    def get_disp_delta (self, precision):
        # haven't split yet or missed the split
        if self._time is None: 
            return '-'
        # no comparison to be had
        elif self._last_c_time is None: 
            return '-'
        # split, show delta
        else: 
            behind = '+' if self._c_time >= self._last_c_time else ''
            return '[ ' + behind + helpers.s_to_hms(self._c_time - self._last_c_time, precision) + ' ]'
    
    # get the display time - a cumulative time - either the previous run or the current run time (or '-' if some data is missing)
    #     also for VA
    def get_disp_time (self, precision, future):
        # haven't split yet 
        if future: # implies self._time is None as well # also applies to the current split 
            string = self.get_disp_last_c(precision)
            return '-' if string is None else string
        # missed the split
        elif self._time is None:
            return '-'
        # split
        else:
            return helpers.s_to_hms(self._c_time, precision)

    # checks if the current time is faster than the listed best time and changes best if true
    def set_time_as_best (self):
        if self.is_a_best():
            self._best_time = self._time
            
    # we PB'ed, so set the current _time as the _last_time (and same with cumulative time)
    def we_pbed (self):
        self._last_time = self._time
        self._last_c_time = self._c_time
        self.set_time_as_best()
            
        
    
    # not really sure what else could be needed. Maybe a method that returns whether the split is complete or not
    # based on whether self._time is None
    
    # also maybe operators like __add__ to add 2 splits more easily?? __getitem__ is probably for splitter, not split
    