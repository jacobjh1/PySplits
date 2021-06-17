'''
Created on Nov 10, 2019

Edited 11/12/19, 12/19/2020

@author: Jacob H.

Given the main root window, associate functions with keypresses

keyboard_listener.py
'''

from tkinter import Toplevel, StringVar, Label, Button

class Binder ():
    def __init__ (self, root, timer):
        self._root = root
        self._timer = timer # (why do i need timer with keyboard?)
        
        # _bindings is a dict, there are 2 entries per action (e.g. split, reset, etc.)
        #    keycode --> (action, keysym)
        #    action --> keycode
        #
        # e.g. (space = 32)
        #    32 --> ('split', 'space')
        #    'split' --> 32
        self._bindings = dict()
        
        ################# for debugging purposes only:
        # self._bindings = {32: ('split', 'space'), 'split': 32, 'unsplit': 8320768, 8320768: ('unsplit', 'Up'), 
        #                  8255233: ('skip_split', 'Down'), 'skip_split': 8255233, 
        #                  91: ('pause', 'bracketleft'), 'pause': 91, 
        #                  96: ('reset', 'quoteleft'), 'reset': 96}

    
    def set_binding (self, action, menu, stringvars):
        def click_to_close():
            top.unbind("<Key>", func_id)
            top.destroy()
            # clean up related to there only being 1 menu open at a time
            menu._layerbind = False
            #print(self._bindings)
        
        def update_menu (act, keysym):
            old = stringvars[act].get().split()
            old[-1] = keysym
            stringvars[act].set(" ".join(old))
        
        def bind_to (event):
            #key_pressed.set('Key pressed: ' + event.keysym)
            
            # this is here bc if you change your mind, you don't want the previous keypress to still be there 
            if action in self._bindings:
                del self._bindings[self._bindings[action]]
            # this is designed to prevent the same key from having bindings to multiple actions 
            if event.keycode in self._bindings:
                old_action = self._bindings[event.keycode][0]
                del self._bindings[old_action]
                update_menu (old_action, 'None')
            self._bindings[event.keycode] = (action, event.keysym)
            self._bindings[action] = event.keycode
            
            # update the hotkey value in the Menu also
            update_menu(action, event.keysym)
            
            click_to_close()
            
        top = Toplevel(self._root, bg = 'white')
        top.geometry('200x100') # 200 width, 100 height  
        top.title('Hotkey: ' + action)
        top.protocol('WM_DELETE_WINDOW', click_to_close)
        
        #key_pressed = StringVar()
        #key_pressed.set('No Key Pressed Yet')
        instr = Label(top, text = 'Press a key')
        #instr = Label(top, textvariable = key_pressed)
        
        # make the Toplevel sensitive to event "key" and then do bind_to() if/when there's a key press
        func_id = top.bind("<Key>", bind_to)
        
        close = Button(top, text = 'Cancel', command = click_to_close)
        
        def unbinding ():
            if action in self._bindings:
                old_key = self._bindings[action]
                del self._bindings[action]
                del self._bindings[old_key]
                update_menu(action, 'None')
            # else it's already unbound
            click_to_close()
        
        unbind = Button(top, text = 'Unbind ' + action, command = unbinding)
        
        top.rowconfigure(0, weight = 1)
        top.rowconfigure(1, weight = 1)
        top.columnconfigure(0, weight = 1)
        top.columnconfigure(1, weight = 1)
        
        # no sticky is kinda a yikes bc i can't see what's going on w all that white screen...
        instr.grid(row = 0, column = 0, columnspan = 2)
        unbind.grid(row = 1, column = 0)
        close.grid(row = 1, column = 1)
        
    def get_bindings_dict (self):
        return self._bindings
    
    def debug_keypress (self):
        self._root.bind("<Key>", lambda e: print("key press", e.char, e.keysym, e.keycode))
        ##################################################################
        # given event e:
        # e.char    e.keysym    e.keycode            (Actual)
        # ----------------------------------------------------------------
        # ""        space        32
        # ""        Meta_L       1048840(592)      command (left, right)
        # ""        Alt_L        524320(2)         alt (left, right)
        #         Up           8320768            up arrow
        #         Left         8124162            left arrow
        #         Down         8255233            down arrow
        #         Right        8189699            right arrow
        # ----------------------------------------------------------------
        # 0        0            48
        # ... 
        # 9        9            57
        # ----------------------------------------------------------------
        # A        A            65
        # ...
        # Z        Z            90
        # ----------------------------------------------------------------
        # a        a            97                
        # ...
        # z        z            122
        # ----------------------------------------------------------------
        # and so it goes