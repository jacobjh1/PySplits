from tkinter import Menu, Toplevel, Label, Entry, Button, Scrollbar, Frame, Canvas, StringVar, PhotoImage
from tkinter import VERTICAL, N, S, E, W
from tkinter import ttk
import re
import helpers
from split import Split
import os

class Run_settings ():
    def __init__ (self, parent):
        self._parent = parent
        self._run_menu = parent._run_menu
    
    def run (self):
        if self._parent._layer1:
            self._parent._root.bell()
            return 
        self._parent._layer1 = True
        
        def destroy ():
            self._parent._layer1 = False
            #print('header', header.winfo_width(), header.winfo_height())
            #print('footer', footer.winfo_width(), footer.winfo_height())
            #print('scrollbar', scrollbar.winfo_width())
            #print('splits', splits_canvas.winfo_width(), splits_canvas.winfo_height())
            #print('arrow', arrows[0][0].winfo_width())
            #print('name', n_ent.winfo_width()) // need to say n_ent = None somewhere
            #print('entry x3', splits_canvas.nametowidget(self._run_menu._ordered_entries[0][0]).winfo_width())
            #print('window', window.winfo_width(), window.winfo_height() - header.winfo_height() - footer.winfo_height())
            #print('window', window.winfo_width(), window.winfo_height())
            window.destroy()
            
        
        # uses self._parent._splits
        window = Toplevel(self._parent._root)
        window.title('Run')
        window.protocol('WM_DELETE_WINDOW', destroy)
        
        # dimensions
        w = 660 # arrow buttons are 40 wide apparently, then idk why but we +68 for the x and plus
        headerh = 100 # idk
        footerh = 42 # 22 (idk) + 10 (window padding) + 10 (button padding) 
        t_and_b = headerh + footerh # 112
        # 7 --> 412, 552
        # 6 --> 354, 474 --> 1 split = 58, 78
        # 1 --> 64, 84 --> +6 y-intercept still
        # 55x + 20x + 3(x+2) where 20 = arrow padding, x = number of splits, 3 is I guess the frame/entry/canvas padding? idk honestly
        inith = t_and_b + min(8, len(self._parent._splits)) * 78 + 6 # exclude the bottom split padding...?
        # same eqn present in rm(), so make sure to adjust that later on
        maxh = t_and_b + (len(self._parent._splits) * 78 + 6) # header + footer + sizeof splits
        window.geometry(str(w) + 'x' + str(inith))
        window.minsize(w, t_and_b)
        window.maxsize(w, maxh)
        
        # display run title, description; enable edits w/ Entry
        header = Frame(window)
        header.grid(row = 0, column = 0, sticky = (N, E, W))
        # window.rowconfigure(0, weight = 0)
        window.columnconfigure(0, weight = 1)
        
        title_label = Label(header, text = 'title:')
        title_txt = StringVar(value = self._parent._timer.get_title())
        title = Entry(header, textvar = title_txt)
        desc_label = Label(header, text = 'description:')
        desc_txt = StringVar(value = self._parent._timer.get_description())
        desc = Entry(header, textvar = desc_txt)
                    
        title_label.grid(row = 0, column = 0, sticky = E)
        desc_label.grid(row = 1, column = 0, sticky = E)
        title.grid(row = 0, column = 1, columnspan = 3, sticky = (E, W))
        desc.grid(row = 1, column = 1, columnspan = 3, sticky = (E, W))
        
        name = Label(header, text = '\tSplit Name', width = 16) #, bg = 'yellow')
        tot_time = Label(header, text = 'Total Time', width = 12) #, bg = 'pink')
        sp_time = Label(header, text = 'Split Time', width = 8) #, bg = 'red')
        best_time = Label(header, text = '  Best Time', width = 12) #, bg = 'grey')
        
        name.grid(row = 2, column = 1, sticky = E, pady = (20, 0))
        tot_time.grid(row = 2, column = 2, sticky = E, pady = (20, 0))
        sp_time.grid(row = 2, column = 3, sticky = E, pady = (20, 0))
        best_time.grid(row = 2, column = 4, sticky = E, pady = (20, 0))
        
        # very approximate in terms of weights
        #header.columnconfigure(0, weight = 3, pad = 0) # instead of weights 0, 1, 0, 0, 0
        #header.columnconfigure(1, weight = 20, pad = 0)
        #header.columnconfigure(2, weight = 10, pad = 0)
        #header.columnconfigure(3, weight = 10, pad = 0)
        #header.columnconfigure(4, weight = 10, pad = 0)
        
        header.columnconfigure(0, weight = 0, pad = 0)
        header.columnconfigure(1, weight = 1, pad = 10)
        header.columnconfigure(2, weight = 1, pad = 10)
        header.columnconfigure(3, weight = 1, pad = 10)
        header.columnconfigure(4, weight = 1, pad = 10)
        header.columnconfigure(5, weight = 10, pad = 10)
        header.columnconfigure(6, weight = 10, pad = 10)
        

        scrollbar = Scrollbar(window, orient = VERTICAL)
        scrollbar.grid(row = 1, column = 1, sticky = (N, S)) # make sure column 1's weight remains 0

        # size of canvas:
        # then, height can be # splits * 25, arbitrary 25, but i changed it to 50 and nothing seemed to change...
        #    I also have a configure(height) over in rm, so if 25 ever changes...
        splits_canvas = Canvas(window, width = w, height = 25 * len(self._parent._splits), yscrollcommand = scrollbar.set, bg = 'grey')
        splits_canvas.grid(row = 1, column = 0, sticky = (N, S, E, W))
        window.rowconfigure(1, weight = 1) # told ya, now just remember what this line does (i.e. consider that the other 2 rows have 0 wght)
        scrollbar.configure(command = splits_canvas.yview)
        
        splits_frame = Frame(splits_canvas)
        splits_canvas.create_window((0, 0), window = splits_frame, anchor = 'nw')
        splits_frame.bind('<Configure>', lambda event : splits_canvas.configure(scrollregion = splits_canvas.bbox('all')))


        # probably bad practice but idc at this point. validate is really annoying
        
        # this data structure is in the form of:
        #
        #    widget_name : [prev str, StringVar, index]
        #
        # bc the valid() fxn can get the widget_name, then use it as an index to access the previously valid string and .set the StrVar w/ it
        # (it also does double duty by storing the StringVar, which is needed bc of scope reasons - apself._parently ttk Entries
        # like things to not be local, but tk Entries don't care)
        self._run_menu._entries = {}
        
        # list of ordered entries, indexed 0, 1, 2, ...
        # the difference is that _entries is a dict, and it's indexed by widget name
        # this list is of the form:
        #
        #    index : (total_entry, split_entry, best_entry, name_entry) (i.e. entry = widget)
        # 
        # the values of the tuple can then go and index the _entries dict
        # (I don't think name is needed here...) 
        self._run_menu._ordered_entries = []

        p = self._parent._timer.get_precision()
        # tested at https://regex101.com/r/daenxT/3/
        time_str = re.compile(r'^(((-?\d+(:[0-5]\d){0,2})?(\.\d+)?)|(-\.\d+))$')
        no_minus = re.compile(r'^((\d+(:[0-5]\d){0,2})?(\.\d+)?)$')
        
        # logic: (idk if this is right anymore lol)
        #    if you edit cumulative time, then split time should change (and checked to be non-negative first)
        #        if split time changes, best time should be checked
        #    ordering:
        #        check would-be split first (update) --> (update best) --> actually update cumulative time
        #
        #    if you edit split time, then cumulative time should change (no extra validation needed)
        #        if split time changes, best time should be checked
        #    ordering:
        #        update split time --> (update best) --> update cumulative time
        # 
        #    if you edit best time, check that best is better than the split time also? But what if it's a fake best?
        #    ordering:
        #        update best
        #
        # and but also, you've gotta consider how changing a value affects future values...
        
        def check_best (index, split_time):
            best_ent = self._run_menu._ordered_entries[index][2]
            b_time = helpers.hms_to_s(self._run_menu._entries[best_ent][0])
            if b_time is None or split_time < b_time:
                valid_update(helpers.s_to_hms(split_time, p), 1, best_ent)
        
        def valid_cumulative (current, widget):
            # if input (current) isn't even good to begin with
            if time_str.match(current) is None:
                return valid_update(0, None, widget) # 0 is arbitrary, None is required 
            
            index = self._run_menu._entries[widget][2]
            
            if current == '':
                # just uh, go do what's done in valid_split when current == ""
                return valid_split(current, self._run_menu._ordered_entries[index][1])
            
            # go find the most recent, non-None c_time 
            #old_c = self._parent._timer.get_offset() # strange, but I think this works since we're just doing a comparison with old_c
            old_c = 0
            if index > 0: # index == 0 screws up the slicing
                for c_ent in self._run_menu._ordered_entries[index-1::-1]:
                    c_ent = c_ent[0] 
                    if self._run_menu._entries[c_ent][0] != "":
                        old_c = helpers.hms_to_s(self._run_menu._entries[c_ent][0])
                        break
            # go find the next, non-None c_time bc we need to sandwich the times... roughly speaking
            new_c = None
            for c_ent in self._run_menu._ordered_entries[index + 1:]:
                c_ent = c_ent[0]
                if self._run_menu._entries[c_ent][0] != "":
                    new_c = helpers.hms_to_s(self._run_menu._entries[c_ent][0])
                    index2 = self._run_menu._entries[c_ent][2]
                    break
            
            # check the diff of current - old_c >= 0 bc you can't have a negative split time... that's impossible
            # check the diff of the next_c - current >= 0
            current_s = helpers.hms_to_s(current)
            delta = current_s - old_c
            reverse_delta = None if new_c is None else new_c - current_s
            if delta < 0 or (reverse_delta is not None and reverse_delta < 0): # invalid 
                return valid_update(0, None, widget) # 0 arbitrary, None required
            else: # valid
                # update split times, check bests
                split_ent1 = self._run_menu._ordered_entries[index][1]
                valid_update(helpers.s_to_hms(delta, p), 1, split_ent1) # 1 is arbitrary so long as it's not None
                check_best(index, delta)
                
                if reverse_delta is not None:
                    split_ent2 = self._run_menu._ordered_entries[index2][1]
                    valid_update(helpers.s_to_hms(reverse_delta, p), 1, split_ent2)
                    check_best(index2, reverse_delta)
                    
                # update total time
                return valid_update(current, 1, widget) 
            
            

        def valid_split (current, widget):
            if no_minus.match(current) is None:
                return valid_update(0, None, widget)
            
            split_ent = self._run_menu._entries[widget]
            old_split = helpers.hms_to_s(split_ent[0]) # (float)secs (or None)
            index = split_ent[2]
            
            if current == "":
                # update cumulative
                valid_update(current, 1, self._run_menu._ordered_entries[index][0])
                # update split
                valid_update(current, 1, widget)
                # update next split by adding the old split value (assuming non-None)
                next_s = None
                for s_ent in self._run_menu._ordered_entries[index + 1:]:
                    s_ent = s_ent[1]
                    if self._run_menu._entries[s_ent][0] != "":
                        next_s = helpers.hms_to_s(self._run_menu._entries[s_ent][0])
                        break
                if old_split is not None and next_s is not None:
                    valid_update(helpers.s_to_hms(old_split + next_s, p), 1, s_ent) 
                return True
            
            # look for the next Entry w/ a time (s_time, specifically to see if current split time is valid)
            next_s = None
            for s_ent in self._run_menu._ordered_entries[index+1:]:
                s_ent = s_ent[1]
                if self._run_menu._entries[s_ent][0] != "":
                    next_s = helpers.hms_to_s(self._run_menu._entries[s_ent][0])
                    index2 = self._run_menu._entries[s_ent][2]
                    break
                
            current_s = helpers.hms_to_s(current)
            delta = current_s if old_split is None else (current_s - old_split)
            # split is too long, and would make the following split take negative time
            if next_s is not None and next_s - delta < 0:
                return valid_update(0, None, widget)
            
            # else: update is okay, so go do some more finangling with the data structures and data
            
            
            # now go update the following split by -delta
            
            if next_s is not None:
                s_time = helpers.s_to_hms(next_s - delta, p)
                valid_update(s_time, 1, s_ent)
                check_best(index2, next_s - delta)
            
            # figure out how to get the cumulative time:
            # add the split time to cumulative time, and if it's non-existent, find the most recent c_time                      
            cumulative_entry = self._run_menu._ordered_entries[index][0]
            c_time = self._run_menu._entries[cumulative_entry][0]
            
            if c_time == "":                    
                old_c = 0 # default 
                if index > 0:
                    for c_ent in self._run_menu._ordered_entries[index-1::-1]:
                        c_ent = c_ent[0]
                        if self._run_menu._entries[c_ent][0] != "":
                            old_c = helpers.hms_to_s(self._run_menu._entries[c_ent][0])
                            break
                c_time = helpers.s_to_hms(old_c + current_s, p)
                
            else:
                c_time = helpers.s_to_hms(helpers.hms_to_s(c_time) + current_s - old_split, p)
            
            valid_update(c_time, 1, cumulative_entry)
            
            
            # update the current split, doesn't really have to be last, just anywhere after the "update is okay" comment
            valid_update(current, 1, widget)
            check_best(index, current_s) # i'm mildly annoyed at myself._parent for making s = seconds or split in different contexts
            
            return True


        def valid_best (current, widget):
            if no_minus.match(current) is None:
                return valid_update(0, None, widget)
            
            index = self._run_menu._entries[widget][2]
            s_ent = self._run_menu._ordered_entries[index][1]
            s_time = self._run_menu._entries[s_ent][0]
            
            # make sure the current input is actually a best
            if current != "":
                if s_time != "" and helpers.hms_to_s(s_time) < helpers.hms_to_s(current):
                    return valid_update(0, None, widget)
                return valid_update(current, 1, widget)
                    
            else: # the current split time (if it exists) is necessarily the best split
                return valid_update(s_time, 1, widget)
        
        def valid_update (current, match, widget : str):
            s = self._run_menu._entries[widget]
            #print(widget, type(widget))
            if match is None:
                s[1].set(s[0])
                # plays the OS's error noise
                window.bell()
                return False
            else:
                s[0] = current
                #s[0] = s[1].get() subtle difference - the correct one doesn't necessarily use the StringVar value
                s[1].set(current)
                return True
            
            #widget = splits_canvas.nametowidget(widget)
            #print(widget, widget.winfo_width(), widget.winfo_height())
        
        val_c = (splits_frame.register(valid_cumulative), '%P', '%W')
        val_s = (splits_frame.register(valid_split), '%P', '%W')
        val_b = (splits_frame.register(valid_best), '%P', '%W')
    
        self._run_menu._up = PhotoImage(file = os.path.join('images', 'up.png'))
        self._run_menu._down = PhotoImage(file = os.path.join('images', 'down.png'))
        self._run_menu._x = PhotoImage(file = os.path.join('images', 'x.png'))
        self._run_menu._plus = PhotoImage(file = os.path.join('images', 'plus.png'))
        
        def swp (index, offset):
            # offset is -1 for swap above
            # offset is 1 for swap below
            def swap ():
                low = min(index, index + offset)    # i (below)    or     i-1 (above)
                high = max(index, index + offset)   # i+1          or     i
                # what to do:
                #    we have the low and high variables
                # adjust the self._run_menu._entries
                #    so uh, we need to adjust the indices (the [2] index of the tuple for each of the 3 widgets on the 2 (i and i±1) entries
                #    also need to possibly change the total time of the low: if low and high both exist, then get the diff for the split 
                #    times and do low total time, high total time = high total time, low total time + diff
                #    then otherwise, just do low total time, high total time = high total time, low total time
                #    
                # what to not do: 
                #    don't adjust the button placements themselves - no need
                #    don't reassign any variables - make sure to mutate things
                #
                # then maybe fix update() bc I'm messing w/ indices, so idk if the get_children_widgets thingie reversed is adequate still
                
                # out of bounds, easier than removing the top arrow from the first entry and bottom arrow from the last entry
                #     why? bc the update function is so much easier when you're able to use % without worrying about first/last edges
                if low < 0 or high == len(self._run_menu._ordered_entries):
                    return 
                
                for i, (widget_l, widget_h) in enumerate(zip(self._run_menu._ordered_entries[low], self._run_menu._ordered_entries[high])):
                    str_l = self._run_menu._entries[widget_l][0] 
                    str_h = self._run_menu._entries[widget_h][0] 
                    
                    if i == 0 and str_l != "" and str_h != "": # then it's total time
                        another_widget_l = self._run_menu._ordered_entries[low][1] 
                        split_l = helpers.hms_to_s(self._run_menu._entries[another_widget_l][0]) 
                        another_widget_h = self._run_menu._ordered_entries[high][1] 
                        split_h = helpers.hms_to_s(self._run_menu._entries[another_widget_h][0]) 
                        diff = split_h - split_l 
                        
                        str_l = helpers.s_to_hms(helpers.hms_to_s(str_l) + diff, p) 
                        valid_update(str_l, 1, widget_l)
                        #valid_update(str_h, 1, widget_h) # would be redundant
                    
                    else:        
                        valid_update(str_h, 1, widget_l)  
                        valid_update(str_l, 1, widget_h) 
                
            return swap

            
        def arrow (direction, index): # 'u' for up ('d' for down)
            if direction == 'u':
                return Button(splits_frame, image = self._run_menu._up, command = swp(index, -1))
            elif direction == 'd':
                return Button(splits_frame, image = self._run_menu._down, command = swp(index, 1))
                
        def rm (index):
            ################# major issue: deleting a split means you might need to merge some split times together
            ################# rn it works if the split is empty 
            ### it doesn't work if the split has a time and it really doesn't work if it's the last split
            #
            # pretty easy solution: just manually zero out the split time/total time row Entry and use whichever validation, and then remove it
            #    bc removing empty splits works fine.
            #    (ps: the best split is basically ignored in this case, so maybe if things change in the future, that might need addressing)
            #
            # uh... I got a KeyError for my _entries dict when I did the above algorithm, then tried to access the last split time
            #    I think I'm removing the wrong thing from the dict. Bc it's in valid_split, which gets the widget name from the Entry valid 
            #    and the widget name can't be wrong... so it must be the wrong thing being del'ed
            #
            # also, why isn't this the reverse of plus?? Like, plus appends a new row, then shifts the text down
            #     why does remove not shift the text up, then del the botton row? Or does it?
            #     imma do this, but first figure out what the logic mistake is/was
            #
            # wha?? it's only the total_time Entry that seems to cause key errors........ which is weird bc the call stack says it's valid_split
            # 
            # another consistent error: click plus, then minus, then plus again and the new split doesn't show up visibly
            #    but it is there in the underlying data structure or *something* bc the splits do update correctly after closing...
            # it's probably a silly omission where I need to update yet another data structure but forgot it
            #
            # I think the problem was the gridding... bc, say you remove row 3 (6 things total before). Visually, everything initially looks okay
            #     but then, the problem is that internally, things are gridded at rows 0, 1, 2, 4, 5 but since nothing's gridded at
            #     row 3, row 3 is essentially squashed to nothing
            #     but then, you go add a new row, pls() would attempt to grid at row 5, but that's wrong now
            #    solution: just do the reverse of pls()
            def remove ():    
                # must have at least 1 split, or else you're softlocked, basically -  you couldn't add another split
                if len(self._run_menu._ordered_entries) == 1:
                    for widget in self._run_menu._ordered_entries[0]: # index = 0 in this case anyway
                        valid_update('', 1, widget)
                    return
                else:
                    widget = self._run_menu._ordered_entries[index][0] # total time widget
                    valid_cumulative("", widget)
            
                                 
                new_ws = self._run_menu._ordered_entries[index]
                for old_ws in self._run_menu._ordered_entries[index + 1:]:
                    for new, old in zip(new_ws, old_ws):
                        valid_update(self._run_menu._entries[old][0], 1, new)
                        
                    new_ws = old_ws
                        
                for widget in self._run_menu._ordered_entries[-1]:
                    del self._run_menu._entries[widget]
                    widget = splits_frame.nametowidget(widget)
                    widget.grid_forget()
                    
                del self._run_menu._ordered_entries[-1]
                
                arrows[-1][0].grid_forget()
                arrows[-1][1].grid_forget()
                del arrows[-1]
                
                x_es[-1].grid_forget()
                del x_es[-1]
                
                plus_es[-1].grid_forget()
                del plus_es[-1]
                
                #for i, all_widgets in enumerate(self._run_menu._ordered_entries[index + 1:], index + 1):
                #    for widget in all_widgets:
                #        self._run_menu._entries[widget][2] -= 1
                #    arrows[i][0].configure(command = swp(i - 1, -1)) # maybe don't do this...
                #    arrows[i][1].configure(command = swp(i - 1, 1))
                #    x_es[i].configure(command = rm(i - 1))
                #    plus_es[i].configure(command = pls(i - 1))
                
                #for widget in self._run_menu._ordered_entries[index]:
                #    del self._run_menu._entries[widget]
                #    widget = splits_frame.nametowidget(widget)
                #    widget.grid_forget()
                
                #del self._run_menu._ordered_entries[index]
                
                #arrows[index][0].grid_forget()
                #arrows[index][1].grid_forget()
                #del arrows[index]
                
                #x_es[index].grid_forget()
                #del x_es[index]
                
                #plus_es[index].grid_forget()
                #del plus_es[index]
                
                splits_canvas.configure(height = 25 * len(self._run_menu._ordered_entries))
                maxh = t_and_b + (len(self._run_menu._ordered_entries) * 78 + 6)
                window.maxsize(w, maxh)
                
            return remove
        
        def pls (index):
            def plus ():
                # 2 approaches:
                # 1) insert a tuple of entries, then adjust all indices and stuff 
                # 2) append a tuple of entries, then shift everything down 1 (imma do this bc grid ends up annoying for method 1)
                
                length = len(self._run_menu._ordered_entries)
                
                arrows.append((arrow('u', length), arrow('d', length)))
                x_es.append(Button(splits_frame, image = self._run_menu._x, command = rm(length)))
                plus_es.append(Button(splits_frame, image = self._run_menu._plus, command = pls(length)))
                
                create_row(length, Split())
                  
                length += 1
                new_ws = self._run_menu._ordered_entries[-1]
                for old_ws in self._run_menu._ordered_entries[length - 2:index:-1]:
                    for new, old in zip(new_ws, old_ws):
                        valid_update(self._run_menu._entries[old][0], 1, new)
                        #self._run_menu._entries[new][2] += 1
                        
                    new_ws = old_ws
                        
                # go replace this index with Nones
                for widget in self._run_menu._ordered_entries[index + 1]:
                    valid_update('', 1, widget)
                
                splits_canvas.configure(height = 25 * length)
                maxh = t_and_b + (length * 78 + 6)
                inith = t_and_b + min(8, len(self._run_menu._ordered_entries)) * 78 + 6
                window.geometry(str(w) + 'x' + str(inith))
                window.maxsize(w, maxh)
                
            return plus
                
        # buttons for moving, removing, adding below
        
        # stored as tuples (up_button, down_button), 1 for each split
        arrows = [(arrow('u', i), arrow('d', i)) for i in range(len(self._parent._splits))]
        
        x_es = [Button(splits_frame, image = self._run_menu._x, command = rm(i)) for i in range(len(self._parent._splits))]
        
        plus_es = [Button(splits_frame, image = self._run_menu._plus, command = pls(i)) for i in range(len(self._parent._splits))]
                    
        def create_row (i, split):
            # ttk.Entry allows repeated validates w/o disabling
        
            arrows[i][0].grid(row = 2 * i, column = 0, pady = (10, 0)) # up
            arrows[i][1].grid(row = 2 * i + 1, column = 0, pady = (0, 10)) # down 
            
            n = StringVar(value = split.get_name()) # name 
            n_ent = Entry(splits_frame, textvar = n, justify = 'right') 
            n_ent.grid(row = 2 * i, column = 1, rowspan = 2, sticky = (E, W))
        
            t = StringVar(value = split.get_disp_last_c(p)) # total time
            t_ent = ttk.Entry(splits_frame, textvar = t, width = 10, # default 20
                      justify = 'right', validatecommand = val_c, validate = 'focusout') 
            t_ent.grid(row = 2 * i, column = 2, rowspan = 2)
        
            s = StringVar(value = split.get_disp_last(p)) # split time
            s_ent = ttk.Entry(splits_frame, textvar = s, width = 10, 
                      justify = 'right', validatecommand = val_s, validate = 'focusout') 
            s_ent.grid(row = 2 * i, column = 3, rowspan = 2)
        
            b = StringVar(value = split.get_disp_best(p)) # best time
            b_ent = ttk.Entry(splits_frame, textvar = b, width = 10,
                      justify = 'right', validatecommand = val_b, validate = 'focusout') 
            b_ent.grid(row = 2 * i, column = 4, rowspan = 2)
            
            plus_es[i].grid(row = 2 * i, column = 5, rowspan = 2)
            x_es[i].grid(row = 2 * i, column = 6, rowspan = 2)
            
            
            #print(str(n), str(t), str(s), str(b), type(n))
            self._run_menu._entries[str(n_ent)] = [n.get(), n, i] # i only need to store the StringVar; not used for valid
            self._run_menu._entries[str(t_ent)] = [t.get(), t, i]
            self._run_menu._entries[str(s_ent)] = [s.get(), s, i]
            self._run_menu._entries[str(b_ent)] = [b.get(), b, i]
            self._run_menu._ordered_entries.append((str(t_ent), str(s_ent), str(b_ent), str(n_ent))) # rip consistent ordering, but w/e
        
        for i, split in enumerate(self._parent._splits):
            create_row(i, split)
        
        splits_frame.columnconfigure(0, weight = 0, pad = 10)
        splits_frame.columnconfigure(1, weight = 1, pad = 10) 
        splits_frame.columnconfigure(2, weight = 0, pad = 10)
        splits_frame.columnconfigure(3, weight = 0, pad = 10)
        splits_frame.columnconfigure(4, weight = 0, pad = 10)
        splits_frame.columnconfigure(5, weight = 0, pad = 5)
        splits_frame.columnconfigure(6, weight = 0, pad = 5)
        
        def updating ():
            # it's majorly problematic that focusout means that failing to tab out of an Entry and clicking straight to updating() 
            #    means skipping the validation... bc then we don't know which widget was last touched
            for widgets in self._run_menu._ordered_entries:
                for i in range(3): # would be majorly problematic also if I edit these data structures to hold more info later on rip :(
                    wgt = self._run_menu._entries[widgets[i]]
                    if wgt[0] != wgt[1].get():
                        splits_frame.nametowidget(widgets[i]).validate() 
            
            self._parent._timer.set_title(title_txt.get())
            self._parent._timer.set_description(desc_txt.get())
            
            short = long = False
            
            while len(self._parent._splits) > len(self._run_menu._ordered_entries):
                del self._parent._splits[-1] # almost an issue if you del before remove_splits(), but I finagled it I think
                long = True
                
            if long:
                self._parent._va.remove_splits(len(self._run_menu._ordered_entries))
                
            while len(self._parent._splits) < len(self._run_menu._ordered_entries):
                self._parent._splits.append(Split())
                short = True
                
            if short:
                self._parent._va.add_splits(len(self._run_menu._ordered_entries))
            
            widgets_per_split = wps = 8
            for i, entry in enumerate(reversed(splits_frame.grid_slaves())):
                # goes up arrow, down arrow, name, cumulative, split, best, plus, x
                if i%wps == 2: # name
                    # dunno if i should use i//4 or self._run_menu[str(entry)][2] depends on rearranging works
                    self._parent._splits[i//wps].set_name(entry.get()) 
                elif i%wps == 3: # cumulative/total
                    self._parent._splits[i//wps].set_last_c_time(entry.get())
                elif i%wps == 4: # split
                    self._parent._splits[i//wps].set_last_time(entry.get())
                elif i%wps == 5: # best
                    self._parent._splits[i//wps].set_best(entry.get())
            
            destroy()
        
        footer = Frame(window)
        footer.grid(row = 2, column = 0, sticky = (S, E, W))
        window.rowconfigure(2, pad = 10)
        # window row 2 can remain 0 weight
    
        # save button, cancel button; place onto footer
        update = Button(footer, text = 'Update', command = updating)
        cancel = Button(footer, text = 'Cancel', command = destroy)
        
        cancel.grid(row = 0, column = 0, sticky = E, pady = (0, 10))
        update.grid(row = 0, column = 1, pady = (0, 10))
        footer.rowconfigure(0, weight = 1)
        footer.columnconfigure(0, weight = 1)
            
