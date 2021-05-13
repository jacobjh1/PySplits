# PySplits
A speedrun timer for Macs that uses Python. Version 0.9. Currently has about 90% of features I want for a solid 1.0 version

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

In its "version 0.9" form, this program is usable by running visual_assembly.py. 
That being said, there are 2 main features that I want to add before I call this project an adequate 1.0 version:
  saving/loading splits from a file and adding the ability to customize various colors in the GUI
