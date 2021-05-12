from tkinter import Toplevel, Text, Button, Label, N, S, E, W

def confirm_pb (menu, timer):
    if menu._layer1: # kind of a redundant check bc if menu is not None, then layer1 needs to be false anyway, but whatever
        menu._root.bell()
        return
    menu._layer1 = True

    ########## need to add a cancel option - wouldn't need to change much: just do a destroy() without the finish_reset() part
    #    bc the first part of reset() that calls confirm() doesn't change any instance variables of the timer
    # actually that's a lie: we'd need to change both _pbed and _exists_best to False (just in case) 
    def destroy ():
        menu._layer1 = False
        window.destroy()
        #print(timer._pbed)
        timer.finish_reset()
    
    window = Toplevel(menu._root)
    window.title('Congratulations!')
    window.protocol('WM_DELETE_WINDOW', destroy)
    
    txt = Label(window) # justify 'center' or anchor 'e' or grid.sticky??
    txt.configure(text = "You've achieved a PB!\nWould you like to overwrite the times from your previous PB?")
    
    def n ():
        timer._pbed = False
        destroy()
        
    yes = Button(window, text = 'Yes', command = destroy) # sidenote, this means clicking the red x to close the window will save the PB
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
        timer.finish_reset()
    
    window = Toplevel(menu._root)
    window.title('Congratulations!')
    window.protocol('WM_DELETE_WINDOW', destroy)
    
    txt = Label(window) # justify 'center' or anchor 'e' or grid.sticky??
    txt.configure(text = "You've achieved one or more best splits!\nWould you like to overwrite the previous best times?")
    
    def n ():
        timer._exist_bests = False
        destroy()
        
    yes = Button(window, text = 'Yes', command = destroy) # sidenote, this means clicking the red x to close the window will save the PB
    no = Button(window, text = 'No', command = n)
    
    txt.grid(row = 0, column = 0, columnspan = 2)
    no.grid(row = 1, column = 0, sticky = E)
    yes.grid(row = 1, column = 1, sticky = W)
    
    window.columnconfigure(0, weight = 1)
    window.columnconfigure(1, weight = 1)
    window.rowconfigure(0, weight = 1)
    window.rowconfigure(1, weight = 1)