#!/usr/bin/python
from Tkinter import *
import tkFileDialog
import sys
import re

eo = 'eo.txt'

def chelp():
    print "Usage:"
    print "\"-\" is a main item for the checklist."
    print "\"+\" is a sub item for the item above it."
    print "\"*\" is a warning for the item above it."
    print "* = green, ** = orange, ***=red"

class Parser(object):
    '''Class to parse xml files and place into checklist.
reads a text file:  '-' Item   '+' sub item   '*'warning'''
    def __init__(self):
        pass

    def readFile(self, f):
        of = open (f, 'r')
        li = []
        item = None
        i = re.compile('^-')
        s = re.compile('^\+')
        w = re.compile('^\*')
        for line in of:
            line.strip()
            line = line[:-1]
            if i.match(line):
                if item:
                    li.append(item)
                item = [line[2:], [], '']
            elif s.match(line):
                item[1].append(line[2:])
            elif w.match(line):
                item[2] = line
            else:
                print 'The line: ' + line + ", is not correctly formated"
                chelp()
        li.append(item)
        return li
            

    def writeFile(self, f, l):
        pass

class Item(object):
    '''The basic object that makes up the checklist.
Can take a list of sub items and a warning.'''
    def __init__(self, g, f, n, l):
        '''Needs GuiChk, frame, text'''
        self.gui = g         #guichk
        self.pf = f          #parent frame 
        self.item = l[0]     #text for item
        self.num = n         #the index number for ease of use.
        self.sub = None
        if l[1]:
            self.sub = l[1]      #List of sub items
        self.warn = None
        if l[2]:
            self.warn = l[2]     #Text of warnings
        self._fill()

    def _fill(self):
        self.f = Frame(self.pf, relief=RAISED, borderwidth=2)
        if self.warn:
            color = None
            if self.warn.count('*') >= 3:
                color = 'red'
            elif self.warn.count('*') == 2:
                color = 'orange'
            else:
                color = 'green'
            self.warn = Label(self.f, text=self.warn, background=color)
        if self.sub:
            for i in range(len(self.sub)):
                var = IntVar()
                self.sub[i] = Checkbutton(self.f, text=self.sub[i],
                                          variable=var, command=self._subcheck)
                self.sub[i].var = var
        var = IntVar()
        self.item = Checkbutton(self.f, text=self.item, variable=var,
                                command=self._check, state=DISABLED,
                                disabledforeground='white', width=80,
                                justify=LEFT)
        self.item.var = var
        self.item.pack(side=TOP)
        self.f.pack(side=TOP)

    def _check(self, event=None):
        self.disable()
        self.gui.check(self.num)

    def _subcheck(self, event=None):
        for e in self.sub:        #if all checked, enable item
            if e.var.get() == 0:
                return
        self.item.config(state=ACTIVE)

    def enable(self):
        self.item.pack_forget()
        if self.warn:
            self.warn.pack(side=TOP)
        if self.sub:
            for e in self.sub:
                e.pack(side=TOP)
        else:
            self.item.config(state=ACTIVE)
        self.item.pack(side=TOP)
        

    def disable(self):
        if self.warn:
            self.warn.pack_forget()
        if self.sub:
            for e in self.sub:
                e.pack_forget()
        self.item.config(state=DISABLED)

    def reset(self):
        if self.sub:
            for e in self.sub:
                e.var.set(0)
        self.item.var.set(0)

    def destroy(self):
        '''unpacks and forgets'''
        if self.warn:
            self.warn.pack_forget()
        if self.sub:
            for e in self.sub:
                e.pack_forget()
        self.item.pack_forget()
        self.f.pack_forget()

#*************************************************************************

class GuiChk(Tk):
    '''A gui that displays the list created by parser, hopefully will edit.'''
    def __init__(self, parent=None, f=None):
        Tk.__init__(self,parent)
        self.parent = parent
        self.parser = Parser()
        self.lio = []             #list of item objects
        self.f = None   #The frame.
        self._fill(f) #Loads if file was specified
        

    def _load(self, f):
        return self.parser.readFile(f) #will have output

    def _fill(self, f=None):
        menubar = Menu(self)
        filemenu = Menu(menubar, tearoff=0)
        #filemenu.add_command(label="Save", command=self.save)
        #filemenu.add_command(label="New", command=self.nproject)
        filemenu.add_command(label="Open", command=self.openf)
        menubar.add_cascade(label="File", menu=filemenu)
        menubar.add_command(label='Reset', command=self.reset)
        #menubar.add_command(label='Time', command=self.time)
        self.config(menu=menubar)
        d = 0
        if not self.f:
            self.f = Frame(self, width=550)
        if f:
            d = self._load(f)
            for i in range(len(d)):
                self.lio.append(Item(self, self.f, i, d[i]))
            self.lio[0].enable()
        self.f.pack(side=TOP)
        self.winfo_toplevel().wm_geometry("")

    def openf(self):
        fname = tkFileDialog.askopenfilename()
        if fname:
            self.clear()
            self._fill(fname)

    def clear(self):
        '''Clears all data.'''
        for e in self.lio:
            e.destroy()
        self.lio = []

    def reset(self):
        '''Resets all checks'''
        for e in self.lio:
            e.reset()
            e.disable()
        self.lio[0].enable()        

    def check(self, n):
        if len(self.lio)-1 >= n+1:
            self.lio[n+1].enable()

fname = None
if len(sys.argv) > 1:
    if sys.argv.index('-eo'):
        print "using: " + eo
        fname = eo
    
app = GuiChk(None, fname)
app.title('Gui Check')
app.mainloop()
