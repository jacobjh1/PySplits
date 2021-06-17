'''
Created on Nov 13, 2019

Edited 11/14/19, 12/19/2020

@author: Jacob H.

Given a splitter, a dictionary of key bindings, the root to bind keys to: operate the splitter
(the visual assembly also needs to be passed bc of instance variables that are needed)

splitter_interface.py
'''

from splitter import SplitOutOfBounds

class SplitterInterface:
    
    def __init__ (self, timer, bindings, root, visual_assembly, menu):
        '''
        ok so i'm pretty sure that the purpose of this class is to just adjust the _splits_slice variable (of the VA class)
        it just takes consideration of both pause/unpause state
        '''
        self._timer = timer
        self._bindings = bindings
        self._root = root
        self._va = visual_assembly
        self._menu = menu
        self._pause_movement = 0
        # so iirc, there's the timer._current_index(), which is the current split index
        # then there's the pseudo_current, which is usually == current, but sometimes might get desynced when the timer is paused
        #    e.g. you pause the timer, and then arrow up/down, and that is psudo adjustment bc you want to change the visuals w/o 
        #    changing the underlying splits' data
        # um no... pseudo_current + current_index() = whatever I was thinking above and note that this RHS can == len(timer) in certain cases 
        self._pseudo_current = 0
                
        def choose_action(event):
            if event.keycode in self._bindings:
                # ban hotkey actions if a menu is up, simplest just to do a wholesale ban
                # a second option would be to only ban actions if _timer.is_on() and the menus are open
                #     but that would also have some nuance that I don't really care about dealing with
                # a third option is to add some more flags for menus, and only ban keys for the Run (splits) menu
                if self._menu._layer1 or self._menu._layerbind:
                    self._va._root.bell()
                    return 
                
                action = self._bindings[event.keycode][0]
                # if I someday really, really care about performance, then this if/else should be arranged from most common 
                # event to least common event
                if action == 'split':
                    self.split()
                elif action == 'unsplit':
                    self.unsplit()
                elif action == 'skip_split':
                    self.skip_split()
                elif action == 'pause':
                    self.pause()
                elif action == 'reset':
                    self.reset()
                # problem occurs when there's a TopLevel window i.e. if upon reset, there are best splits/PB
                #    then update_all is called before splits are updated, 
                # solution: misc_menuing's 2 destroy()s also need to have an update_all()
                #    correction: update_all in splitter.finish_reset, not in misc_menuing
                self._va.update_all()
                    
        self._root.bind("<Key>", choose_action)
        
        
    ##################################################
    # do not allow the timer to start when the splits menu is open
    #     probably some other safeties to add as well
    # probably okay to allow the hotkeys menu to be open, though
    ##################################################
    
    def split (self):
        # this assumes 'split' == 'start'
        # also later on, that 'pause' != 'start'
        # that being said, 'pause' == 'unpause' != 'start' so yeah
        try:
            if not self._timer.is_on():
                self._timer.start()
                self._va.set_splits_slice(self._va._splits_slice.start - self._pause_movement, self._va._splits_slice.stop - self._pause_movement)
                self._pause_movement = 0
                self._pseudo_current = 0
            else:
                self._timer.split()
                # change the > 2 to show more splits at the top of the screen (same with skip_split/unsplit) (5 places total)
                #     big if true. hallelujah if my past self really made it this easy to implement "previous splits on screen" lmao
                # I know I moved it to the helper, but it's still only 5 instances all throughout
                self.increment_slice()
        except SplitOutOfBounds:
            # this except needs to be here bc (maybe not so broadly, but somewhere, there ought to be a try/except)
            #    there can always be cases of "split when there are no splits left" or "unsplit at the first split" 
            pass 
            #print('split exception')  
        # finally:
            # print(self._va._splits_slice.start, self._va._splits_slice.stop)
            
    def increment_slice (self):
        if self._timer.current_index() > self._va.num_prev and self._va._splits_slice.stop < len(self._timer.get_all_splits()):
            self._va.set_splits_slice(self._va._splits_slice.start + 1, self._va._splits_slice.stop + 1)
            
    def unsplit (self):
        try:
            if self._timer.is_on():
                self._timer.unsplit()
                # change the < 2 to show more splits at the top of the screen (constant is the same as split())
                if self._timer.current_index() - self._va._splits_slice.start < self._va.num_prev and self._va._splits_slice.start > 0:
                    self._va.set_splits_slice(self._va._splits_slice.start - 1, self._va._splits_slice.stop - 1)
            else:
                #self._pseudo_current -= 1 if self._va._splits_slice.start > 0 else 0
                self._pseudo_current -= 1 if (self._timer.current_index() + self._pseudo_current > 0) else 0 ##################
                if self._timer.current_index() + self._pseudo_current - self._va._splits_slice.start < self._va.num_prev and self._va._splits_slice.start > 0:
                    #print('good')
                    self._pause_movement -= 1
                    self._va.set_splits_slice(self._va._splits_slice.start - 1, self._va._splits_slice.stop - 1)
                #print('up', self._pseudo_current, self._pause_movement)
        except SplitOutOfBounds:
            pass
            #print('unsplit exception')
        # finally:
            # print(self._va._splits_slice.start, self._va._splits_slice.stop)
    
    def skip_split (self):
        try:
            if self._timer.is_on():
                self._timer.skip_split()
                #if len(self._timer.get_all_splits()) - self._timer.current_index() + 1 > self._va.splits_on_screen \
                        #and self._timer.current_index() != 2:
                self.increment_slice()
            else:
                #self._pseudo_current += 1 if self._va._splits_slice.stop < len(self._timer) else 0
                # maybe minor issue in that current_index might() be == len bc that's how splitter knows a run is done
                #    so maybe it should be len(self._timer) - 1?
                self._pseudo_current += 1 if (self._timer.current_index() + self._pseudo_current < len(self._timer)) else 0 #################
                if self._timer.current_index() + self._pseudo_current > self._va.num_prev and self._va._splits_slice.stop < len(self._timer.get_all_splits()):
                    #print('good')
                    self._pause_movement += 1
                    self._va.set_splits_slice(self._va._splits_slice.start + 1, self._va._splits_slice.stop + 1)
                #print('down', self._pseudo_current, self._pause_movement)
        except SplitOutOfBounds:
            pass
            #print('skip split exception')
        # finally:
            # print(self._va._splits_slice.start, self._va._splits_slice.stop)    
    
    def pause (self):
        if self._timer.is_on():
            self._timer.pause()
        # else : timer is off
        #     elif timer was paused with some key, then the same key can unpause it
        #        if the timer was reset, pause/unpause cannot start it
        #
        #     this seems janky. why not just use another flag for is_paused?
        elif not self._timer.is_reset():
            self._timer.start()
            self.rest_of_pause()
            
    def rest_of_pause (self):
        self._va.set_splits_slice(self._va._splits_slice.start - self._pause_movement, self._va._splits_slice.stop - self._pause_movement)
        self._pause_movement = 0
        self._pseudo_current = 0
        
    # override=True is done in run_menu bc we want to forcibly override times based on what the user inputted
    def reset (self, override = False):
        # added both those = 0 lines bc I'm 95% sure they're necessary, but it's also been over a year since I've touched this code
        # so just adding this note in case something breaks later on related to this 
        if not override and self._menu._layer1:
            self._menu._root.bell()
            return
        
        self._pause_movement = 0
        self._pseudo_current = 0
        self._timer.reset(self._menu if not override else None)
        self._va.set_splits_slice(0, self._va.splits_on_screen)