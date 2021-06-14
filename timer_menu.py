from tkinter import Toplevel, Label, StringVar, BooleanVar, Entry, Button, Frame, Radiobutton, Checkbutton
from tkinter import ttk
from tkinter import N, S, E, W
import re
import helpers

class Timer_settings ():
    
    def __init__ (self, parent):
        ''' class to:
        edit timer precision, splits to display at once, previous splits to see on screen, show best/sum of best,
        add an initial offset, and probably more later
        '''
        
        self._parent = parent
        
    def timer (self):
        if self._parent._layer1:
            self._parent._root.bell()
            return
        self._parent._layer1 = True
    
        def destroy ():
            self._parent._layer1 = False
            window.destroy() 
            
        window = Toplevel(self._parent._root)
        window.title('Timer')
        window.protocol('WM_DELETE_WINDOW', destroy)
        
        frame = Frame(window)
        frame.grid(row = 0, column = 0, columnspan = 2)
        
        # Entry widgets:
        
        # Row 0
        # num splits on screen 
        on_screen_l = Label(frame, text = 'splits on screen:')
        self.on_screen_s = StringVar(value = self._parent._va.splits_on_screen)
        on_screen_e = ttk.Entry(frame, textvar = self.on_screen_s, width = 6, justify = 'right', validate = 'focusout')
        
        on_screen_l.grid(row = 0, column = 0, sticky = E)
        on_screen_e.grid(row = 0, column = 1)
        
        # Row 1
        # num previous splits
        #        previous splits + (1 if show last split else 0) + 1 <= splits on screen (else things look funny)
        prev_l = Label(frame, text = 'number of past splits shown:')
        self.prev_s = StringVar(value = self._parent._va.num_prev)
        prev_e = ttk.Entry(frame, textvar = self.prev_s, width = 6, justify = 'right', validate = 'focusout')
        
        prev_l.grid(row = 1, column = 0, sticky = E)
        prev_e.grid(row = 1, column = 1)
        
        def valid_int (current):
            # or just do current == '' or current.isdigit()
            if re.match(r'^\d*$', current):
                # number of previous splits shown + possible last split + current split <= number of splits on screen
                if self.prev_s.get() == '':
                    self.prev_s.set('0')
                pv = int(self.prev_s.get())
                if self.on_screen_s.get() == '':
                    on_scr = pv + 2 # worst case/safest thing to do
                    self.on_screen_s.set(str(on_scr))
                else:
                    on_scr = int(self.on_screen_s.get())
            
                minimum = pv + (1 if self._parent._va.include_last_split else 0) + 1
                if minimum > on_scr:
                    self.on_screen_s.set(str(minimum))
                    
            else:
                # plays the OS's error noise
                frame.bell()
                if self.prev_s.get() == current:
                    self.prev_s.set('0')
                else:
                    pv = int(self.prev_s.get())
                    self.on_screen_s.set(str(pv + 2))
                    
            return True
            
        val_int = (frame.register(valid_int), '%P')
        on_screen_e.configure(validatecommand = val_int)
        prev_e.configure(validatecommand = val_int)
        
        # Row 2
        # Checkbutton widget:
        # Always show last split?
        self.last_b = BooleanVar(value = self._parent._va.include_last_split)
        last_cbtn = Checkbutton(frame, text = 'always show last split?', variable = self.last_b, onvalue = True, offvalue = False)
        
        last_cbtn.grid(row = 2, column = 0, columnspan = 2, sticky = E, pady = (0, 10))
        
        # Row 3
        ########## TBH i don't really know why this belongs here... shouldn't it be in run_menu??
        # initial offset 
        #     can technically be positive, but negative values make more sense
        # also 2021 note: so I'm not sure which other functions rely on the hard coded row #s, so it's probably 
        #    safest to just make this row 3 have 0 height/0 weight or w/e instead of shifting rows 4-5 down 1
        timer = self._parent._timer #um good thing this fxn isn't recursive
        time_str = re.compile(r'^(((-?\d+(:[0-5]\d){0,2})?(\.\d+)?)|(-\.\d+))$') # idr how to make this not accept empty strings lol 
        def valid_time (current):
            if time_str.match(current) and current != '':
                return True
            frame.bell()
            self.off_s.set('0')
            return True 
        val_time = (frame.register(valid_time), '%P')
        
        off_l = Label(frame, text = 'initial offset:')
        self.off_s = StringVar(value = helpers.s_to_hms(timer.get_offset(), timer.get_precision()))
        off_e = ttk.Entry(frame, textvar = self.off_s, width = 6, justify = 'right', validate = 'focusout', validatecommand = val_time)
        
        off_l.grid(row = 3, column = 0, sticky = E, pady = (0, 10))
        off_e.grid(row = 3, column = 1, pady = (0, 10))
        
        # Row 4-5
        # Radiobutton widget:
        # precision (0 to 3 bc why the heck do you need more precision? and what does it mean to have less than 0 decimal precision?)
        prec_l = Label(frame, text = 'decimal precision:')
        self.prec_s = StringVar(value = timer.get_precision())
        prec_rb0 = Radiobutton(frame, text = '0', variable = self.prec_s, value = '0')
        prec_rb1 = Radiobutton(frame, text = '1', variable = self.prec_s, value = '1')
        prec_rb2 = Radiobutton(frame, text = '2', variable = self.prec_s, value = '2')
        prec_rb3 = Radiobutton(frame, text = '3', variable = self.prec_s, value = '3')
        
        prec_l.grid(row = 4, column = 0, sticky = E)
        prec_rb0.grid(row = 4, column = 1)
        prec_rb1.grid(row = 4, column = 2, padx = (0, 10))
        prec_rb2.grid(row = 5, column = 1)
        prec_rb3.grid(row = 5, column = 2, padx = (0, 10))
        
        
        # ALSO: MIGHT NOT BE USING THIS AFTER ALL
        # check if the va._splits_slice starts at >= 0 and stops at <= len(timer)
        #     if one of those is not the case, then this function makes it so (with priority to start >= 0 if both are false simultaneously)
        #def check_valid_slice (va):
        #    if va._splits_slice.stop > len(va._timer):
        #        diff = va._splits_slice.stop - len(va._timer)
        #        va.set_splits_slice(va._splits_slice.start - diff, va._splits_slice.stop - diff)
        #    if va._splits_slice.start < 0:
        #        diff = -va._splits_slice.start
        #        va.set_splits_slice(va._splits_slice.start + diff, va._splits_slice.stop + diff)
        
        def updating ():
            va = self._parent._va
            interface = va._splitter_interface
            timer = va._timer
            
            ########## deal with show last split first; might as well deal with the easy stuff too
            va.include_last_split = self.last_b.get()
            
            # precision
            timer.set_precision(int(self.prec_s.get()))
            
            # offset
            off_e.validate()
            reset = timer.is_reset() # this check is based on the old offset, so it needs to come before set_offset()
            timer.set_offset(helpers.hms_to_s(self.off_s.get()))
            if reset:
                va._splitter_interface.reset(True)
            
            
            # splits on screen and number of previous splits
            
            new_sos = int(self.on_screen_s.get())
            prev = int(self.prev_s.get())
            
            # check again if prev + 1 + maybe 1 <= sos (bc that maybe 1 could appear with the new changes)
            #     of course, this all assumes that you want to see the current split at all times as well. idk what scenario wouldn't want this.
            pv = int(self.prev_s.get())
            on_scr = int(self.on_screen_s.get())
            
            minimum = pv + (1 if self._parent._va.include_last_split else 0) + 1
            if minimum > on_scr:
                new_sos = minimum
                #self.on_screen_s.set(str(minimum))
            
            
            # adjust the number of widgets on screen
            if new_sos < va.splits_on_screen:
                va.splits_on_screen = new_sos
                va.remove_splits(new_sos)
            elif new_sos > va.splits_on_screen:
                va.splits_on_screen = new_sos
                va.add_splits(new_sos)
            
            # then adjust the underlying data (namely the slice over in VA that controls which splits appear in the widgets)
            interface.rest_of_pause()
            va.set_splits_slice(0, new_sos)
            va.num_prev = prev
            # this is probably the most sus thing I've ever done until now
            # but 's too dang hard to figure out the logic of "show previous x" combined with "splits on screen"
            current = timer.current_index()
            timer._current = 0
            for _ in range(current):
                # these 2 lines with _current in particular are super duper sketchy bc _current really shouldn't be manually adjusted
                timer._current += 1 
                interface.increment_slice() # bc it's too dang hard to figure out the logic w/o just manually doing this
            
            # actually reflect changes in root window
            self._parent._va.update_all()
            
            # clean up
            destroy()
        
        # save button, cancel button
        update = Button(window, text = 'Update', command = updating)
        cancel = Button(window, text = 'Cancel', command = destroy)
        
        cancel.grid(row = 1, column = 0, sticky = E)#, pady = (0, 10))
        update.grid(row = 1, column = 1, sticky = W)#, pady = (0, 10))
        window.rowconfigure(1, weight = 1, pad = 20)
        window.columnconfigure(0, weight = 1)
        window.columnconfigure(1, weight = 1)
        # footer.columnconfigure(0, weight = 1)
        
        
        
        # Figure out colors, whether we get a fancy color picker, or just a listbox of a few colors...
        # actually no this would go in the fonts and colors menu
        
        
        
        # then all kinds of Checkbuttons related to
        #     - show current split previous time (old PB)
        #     - show current split best time
        #     - add a split timer to go along w the global timer - I literally have this value already - splitter.local_time or w/e
        # 
        #     - show previous split (old PB) time (and the delta)
        #     - show previous split best time (and the delta)
        #
        #     - possible time save (i.e. current split from PB - best split)
        #     - maybe later: sum of best segments (and also best possible time)
        #
        #     - show run counter
        
        # and sooner or later, a listbox to select:
        #     - times to compare against (sum of best vs. last PB vs. something else? (balanced/avg?)
        #        (might have to add some fields to the split class for this... idk)
        #        (bc I only have cumulative times for the PB times...)