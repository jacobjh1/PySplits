from tkinter import Toplevel, Text, Button, Label, N, S, E, W

def confirm_pb (menu, timer):
    if menu._layer1: # kind of a redundant check bc if menu is not None, then layer1 needs to be false anyway, but whatever
        menu._root.bell()
        return
    menu._layer1 = True

    ##########
    # other TODO: can use a MessageBox instead - is a lot easier bc it's built into Tkinter
    # and huh - there's other dialogue box features available with Toplevel that let you have a little more control
    # over what can/can't be interacted with while the dialog is open https://tkdocs.com/tutorial/windows.html
    # tbh I'm fairly comfortable with what I currently have
    # the nice thing about these is they might be able to give a little more native-looking/OS specific dialog boxes 
    #
    ########## need to add a cancel option - wouldn't need to change much: just do a destroy() without the finish_reset() part
    #    bc the first part of reset() that calls confirm() doesn't change any instance variables of the timer
    # actually that's a lie: we'd need to change both _pbed and _exists_best to False (just in case) 
    def destroy ():
        menu._layer1 = False
        window.destroy()
        #print(timer._pbed)
    
    def y ():
        destroy()
        # what a hack lol
        timer.finish_reset(menu) # assume if you want to save pb, you also want to set bests; note that here, menu isn't None for sure
        # timer.mid_reset(menu)
    
    def n ():
        timer._pbed = False
        # timer._exist_bests = False
        destroy()
        # timer.finish_reset()
        timer.mid_reset(menu) # if you don't want to save pb, that has no bearing on setting bests from that run
    
    window = Toplevel(menu._root)
    window.title('Congratulations!')
    window.protocol('WM_DELETE_WINDOW', n)
    
    txt = Label(window) # justify 'center' or anchor 'e' or grid.sticky??
    txt.configure(text = "You've achieved a PB!\nWould you like to save these times over your previous PB?")
        
    yes = Button(window, text = 'Yes', command = y)
    no = Button(window, text = 'No', command = n)
    
    txt.grid(row = 0, column = 0, columnspan = 2)
    no.grid(row = 1, column = 0, sticky = E)
    yes.grid(row = 1, column = 1, sticky = W)
    
    window.columnconfigure(0, weight = 1)
    window.columnconfigure(1, weight = 1)
    window.rowconfigure(0, weight = 1)
    window.rowconfigure(1, weight = 1)
    
def confirm_best (menu, timer):
    if menu._layer1: # again kind of a redundant check bc if menu is not None, then layer1 needs to be false anyway, but whatever
        menu._root.bell()
        return
    menu._layer1 = True

    def destroy ():
        menu._layer1 = False
        window.destroy()
    
    def y ():
        destroy()
        # timer.finish_reset(lambda : File_settings(menu).save_run(True))
        timer.finish_reset(menu) # do want to save for sure
    
    def n ():
        timer._exist_bests = False
        destroy()
        # timer.finish_reset(None if not timer._pbed else (lambda : File_settings(menu).save_run(True)))
        # don't want to save, and it's logically impossible for pbed to be True but exist_bests to be False in this n() function
        timer.finish_reset()  
    
    window = Toplevel(menu._root)
    window.title('Congratulations!')
    window.protocol('WM_DELETE_WINDOW', n)
    
    txt = Label(window) # justify 'center' or anchor 'e' or grid.sticky??
    txt.configure(text = "You've achieved one or more best splits!\nWould you like to save these times over your previous best times?")
        
    yes = Button(window, text = 'Yes', command = y)
    no = Button(window, text = 'No', command = n)
    
    txt.grid(row = 0, column = 0, columnspan = 2)
    no.grid(row = 1, column = 0, sticky = E)
    yes.grid(row = 1, column = 1, sticky = W)
    
    window.columnconfigure(0, weight = 1)
    window.columnconfigure(1, weight = 1)
    window.rowconfigure(0, weight = 1)
    window.rowconfigure(1, weight = 1)