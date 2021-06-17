# PySplits
A speedrun timer for Macs that uses Python. Version 1.0
 
tl;dr run visual_assembly.py to get a working version.

Motivation:

Clearly, this timer is based on LiveSplit because LS is really, really good. However, as a casual speedrun enthusiast, I've always been
disappointed that Macs don't have easy access to speedrun timers. (So there might also been some obvious Llanfair influence also.)
Thus, I've long been wanting to use Python to make one, and over the past few months, I've gotten PySplits (a work in progress name) to a pretty good place.

Other Comments:

I figure in this day and age, Python being interpreted (read: slow) isn't that big of a deal?
Sure, a timer runs constantly and "constant" implies that it uses a bunch of resources, but computers have gigabytes of RAM.
My code's GUI loop only runs once a ms (I'm pretty sure?) and for a non-PC gamer like myself, I'm not doing much else on my computer 
when I have a timer open. So, maybe if you're playing a PC game and have this timer open, it might cause performance issues?
But I kind of doubt that.

On the Progress of This Version:

In v1.0, this program is usable by running visual_assembly.py
I have all the major features I want: color customization, saving/loading past runs and settings, robustness (as far as I can tell from my testing)

I still have other quality of life things I want to add but was too lazy to include immediately, for example:
	if there's a JSON syntax error, I surpressed the error message, and I should probably add a message box with it instead
	I also surpressed file not found exceptions, so i also probably want to add a message box for that
		and in general, a lot of problems just silently failed (not literally, bc I do call bell(), but that's not enough I think)
	adding a reset counter/completed run counter 
	separating scrolling and splitting as different keypresses
