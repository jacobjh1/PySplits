'''
Created on Jul 4, 2019
Edited 8/30/19
mildly edited 11/1/19 and 11/12/19

@author: Jacob H.
stopwatch.py
'''

import time
import math

# add a change_precision?
class Stopwatch:
    '''
    Represents a stopwatch object; counts time up (as in 1, 2, 3, etc.) and reports elapsed time to a specified precision
    ''' 
    
    # a Stopwatch's default decimal place is the tenths place and default starting condition is "off" 
    def __init__ (self, precision : int = 1, offset : float = 0.0, on : bool = False):
        # variable to track the decimal precision of the timer; ranges from [0,3] [digits after the potential radix]
        self._precision = precision
        
        # variable to track whether the stopwatch should be counting up or not
        self._on = on
        
        # =========================================================================================================
        # time.perf_counter_ns() returns an int of the nanoseconds of the current processor time
        # time.perf_counter() returns a float with the seconds of the current processor time
        # time.perf_counter_ns() / 1_000_000 returns a float of the milliseconds of the current processor time
        # =========================================================================================================
        # variable that notes a time in seconds that the stopwatch starts on 
        self._start = time.perf_counter() if on else 0.0 
        
        # float; _time is the time elapsed while on, and is only updated when the timer is paused
        # self._time = 0.0
        self._time = offset
        
        # float; _offset is the time the stopwatch begins at; default is 0.0, but that could change
        #     i.e. offset < 0 indicates a countdown like 3, 2, 1, go
        # self._offset = offset
        self._offset = offset
        
    # split is overriden in the child class; Stopwatch.split resets both the start and offset values without changing the on value
    #     start is based on the processor clock, so no parameter for _start is needed
    # split() returns the time of the split
    def split (self, offset : float):
        split_time = self.get_time()
        self._start = time.perf_counter()
        self._offset = offset
        return split_time
    
    # pauses the stopwatch and assigns _time to _offset to account for the changed _start when start() is called
    def pause (self):
        Stopwatch.update(self)
        self._on = False
        self._offset = self._time
        
    # starts the stopwatch and sets the starting time value
    def start (self):
        # order matters?
        if not self._on:
            self._start = time.perf_counter()
        self._on = True
        
    # resets the times and turns the stopwatch off 
    def reset (self, offset : float = 0.0):
        # self._time = 0.0
        # self._offset = offset
        self._time = offset
        self._offset = offset
        self._on = False
        
    # adds to time the difference between time.perf_counter() and self._start 
    def update (self):
        if self._on:
            self._time = time.perf_counter() - self._start + self._offset
        
    # returns the time based on self._precision (number of decimals to include)
    #    get_time is the only place where self._precision matters
    # minor bug is that when precision > 1, trailing zeroes of floats are omitted (easy fix with str() and concatenation)
    def get_time (self):
        Stopwatch.update(self) # why did I do this? Couldn't I have just done self.update()?? whatever no big deal
        # algorithm to always round down
        t = math.floor(self._time * 10**self._precision) / 10**self._precision
        return t if self._precision > 0 else int(t)
    
    def get_precision (self):
        return self._precision
    
    def set_precision (self, p):
        self._precision = p
    
    def is_on (self):
        return self._on
    
# testing/debug shenanigans
if __name__ == '__main__':
    input('Enter/Return:\n')
    
    print('test start and update')
    timer5 = Stopwatch(2, on = True)
    timer = Stopwatch()
    timer.start()
    while timer.get_time() < 0.1:
        pass
    print(f'1: {timer.get_time()}')         # 0.1
    
    while timer.get_time() < 0.5:
        pass 
    print(f'1: {timer.get_time()}')         # 0.5
    
    print('\ntest pause(s)')
    timer.pause()
    timer2 = Stopwatch(on = True)
    while timer2.get_time() < 0.2:
        pass
    print(f'1: {timer.get_time()}')         # 0.5
    print(f'2: {timer2.get_time()}')        # 0.2
    timer.start()
    while timer2.get_time() < 0.3:
        pass
    print(f'2: {timer2.get_time()}')        # 0.3
    timer.pause()
    print(f'1: {timer.get_time()}')         # 0.6
    while timer2.get_time() < 0.6:
        pass
    print(f'1: {timer.get_time()}')         # 0.6
    print(f'2: {timer2.get_time()}')        # 0.6
    timer.start()
    
    print('\ntest precision')
    timer3 = Stopwatch(2, on = True)
    while timer3.get_time() < 0.15:
        pass
    print(f'3: {timer3.get_time()}')        # 0.15
    
    print('\ntest reset')
    timer2.reset()
    timer2.start()
    while timer2.get_time() < 0.2:
        pass
    print(f'1: {timer.get_time()}')         # > 0.6, probs 0.9
    print(f'2: {timer2.get_time()}')        # 0.2
    print(f'3: {timer3.get_time()}')        # 0.35 or so
    
    print('\ntest negative offset')
    timer4 = Stopwatch(2, -2.0, True)
    while timer4.get_time() < -1.0:
        pass
    print(f'4: {timer4.get_time()}')        # -1.0
    timer4.pause()                          
    while timer2.get_time() < 1.7: # 0.5 second pause
        pass
    print(f'2: {timer2.get_time()}')        # 1.7
    timer4.start()
    while timer4.get_time() < 0:
        pass
    print(f'4: {timer4.get_time()}')        # 0.0
    
    #while timer4.get_time() < 5.55:
        #pass
    
    input('\nEnter/Return:\n')
    print(f'actual time-keeping test\n4: {timer5.get_time()}')  # ≥ 3.95

    
    