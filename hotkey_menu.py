from tkinter import Toplevel, Button, Label, StringVar, N, S, E, W
    
    
class Hotkey_settings ():
    
    def __init__ (self, parent):
        self._parent = parent
    
    def hotkeys (self):
        # TODO:
        # 1) spice it up with colors and stuff
        
        if self._parent._layer1:
            self._parent._root.bell()
            return
        self._parent._layer1 = True
         
        def destroy ():
            self._parent._layer1 = False
            window.destroy() 
        
        window = Toplevel(self._parent._root)
        window.title('Hotkeys')
        window.protocol('WM_DELETE_WINDOW', destroy)
        
        # split, unsplit, skip_split, pause, reset (order matters)
        bindings = self._parent._binder.get_bindings_dict()
        
        def get_bind (action):
            return bindings[bindings[action]][1] if action in bindings else 'None'
        
        # lbls invariant: the keysym (via get_bind) must be last, i.e. when you do .split(), then index [-1] is the keysym
        lbls_txt = {'split': StringVar(value = 'Split: ' + get_bind('split')), 
                    'unsplit': StringVar(value = 'Unsplit: ' + get_bind('unsplit')),
                    'skip_split': StringVar(value = 'Skip split: ' + get_bind('skip_split')),
                    'pause': StringVar(value = 'Pause: ' + get_bind('pause')),
                    'reset': StringVar(value = 'Reset: ' + get_bind('reset'))}
        
        # split, unsplit, skip_split, pause, reset (order probably matters bc the buttons are hard coded in that order)
        
        def bind_handler (action):
            if self._parent._layerbind:
                self._parent._root.bell()
                return
            self._parent._layerbind = True
            self._parent._binder.set_binding(action, self._parent, lbls_txt)
        
        # create the 5 labels and buttons
        all_labels = [Label(window, textvar = lbls_txt[a]) for a in ['split', 'unsplit', 'skip_split', 'pause', 'reset']]
        # buttons must use literals in lambda... just doing for action in [...]: doesn't work bc action ends by pointing to 'reset'
        #    this was actually the worst part of this project to this point, it's just dumb
        all_buttons = [Button(window, text = 'Edit', command = lambda : bind_handler('split')),
                       Button(window, text = 'Edit', command = lambda : bind_handler('unsplit')),
                       Button(window, text = 'Edit', command = lambda : bind_handler('skip_split')),
                       Button(window, text = 'Edit', command = lambda : bind_handler('pause')),
                       Button(window, text = 'Edit', command = lambda : bind_handler('reset'))]
        
        # let window resizing look nicer (via weight)
        for i in range(len(all_labels)):
            window.rowconfigure(i, weight = 1, minsize = 40)
        window.columnconfigure(0, weight = 1)
        window.columnconfigure(1, weight = 1)
        
        # place the labels/buttons
        for i in range(len(all_labels)):
            all_labels[i].grid(row = i, column = 0, sticky = E)
            all_buttons[i].grid(row = i, column = 1, sticky = W, padx = 10)