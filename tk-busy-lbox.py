"""Tkinter listbox ex. p.47. from modern tkinter for busy python devs."""
import tkinter as tk
from tkinter import ttk

root = tk.Tk() # this needs to be set before any stringvar or other tk vars defined/used

ctrcodes = ('ar', 'au', 'be', 'br', 'ca', 'cn', 'dk', 'fi', 'fr', 'gr', 'in', 'it', 'jp', 'mx', 'nl', 'no', 'es', 'se', 'ch')
ctrnames = ('Argentina', 'Australia', 'Belgium', 'Brazil', 'Canada', 'China', 'Denmark', 'Finland', \
  'France', 'Greece', 'India', 'Italy', 'Japan', 'Mexico', 'Netherlands', 'Norway', 'Spain', 'Sweden', 'Switzerland')

cnames = tk.StringVar(value=ctrnames)

popul = {'ar':41000000, 'au':21179211, 'be':10584534, 'br':185971537, 'ca':33148682, 'cn':1323128240, 'dk':5457415,\
  'fi':5302000, 'fr':64102140, 'gr':11147000, 'in':1131043000, 'it':59206382, 'jp':127718000, 'mx':106535000, \
  'nl':16402414, 'no':4738085, 'es':45116894, 'se':9174082, 'ch':7508700 }

gifts = {'card':'Greeting Card', 'flowers':'Flowerz', 'nastygram':'Nastygram'}

# states
gift = tk.StringVar()
sentmsg = tk.StringVar()
statusmsg = tk.StringVar()


def showPopul(*args):
  """Called when listbox sel. changes. update status + clear sentmsg."""
  idxs = lbox.curselection()
  if len(idxs) == 1:
    i = int(idxs[0])
    statusmsg.set(f'Da population of {ctrnames[i]} ({ctrcodes[i]}) is {popul[ctrcodes[i]]}')
  sentmsg.set('')


def sendGift(*args):
  """Called when dbl click on list item, use of send gift btn or press return in listbox -
    .see() scrolls sel. item into view. & Also set sentmsg message."""
  idxs = lbox.curselection()
  if len(idxs) == 1:
    i = int(idxs[0])
    lbox.see(i)
    sentmsg.set(f'Sent {gifts[gift.get()]} to leader of {ctrnames[i]}')


# main
c = ttk.Frame(root, padding=(5, 5, 12, 0))
c.grid(column=0, row=0, sticky='nwes') # fit inside
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)

# wdgts
lbox = tk.Listbox(c, listvariable=cnames, height=5)
lbl = ttk.Label(c, text='Send to country\'s leader:')
g1 = ttk.Radiobutton(c, variable=gift, text=gifts['card'], value='card')
g2 = ttk.Radiobutton(c, variable=gift, text=gifts['flowers'], value='flowers')
g3 = ttk.Radiobutton(c, variable=gift, text=gifts['nastygram'], value='nastygram')
send = ttk.Button(c, text='Send gift', command=sendGift, default='active')
sentlbl = ttk.Label(c, textvariable=sentmsg, anchor='center')
status = ttk.Label(c, textvariable=statusmsg, anchor='w')

# grid all
lbox.grid(column=0, row=0, rowspan=6, sticky='nsew')
lbl.grid(column=1, row=0, padx=10, pady=5)
g1.grid(column=1, row=1, sticky='w', padx=20)
g2.grid(column=1, row=2, sticky='w', padx=20)
g3.grid(column=1, row=3, sticky='w', padx=20)
send.grid(column=2, row=4, sticky='e')
sentlbl.grid(column=1, row=5, columnspan=2, sticky='n', padx=5, pady=5)
status.grid(column=0, row=6, columnspan=2, sticky='we')
c.grid_columnconfigure(0, weight=1)
c.grid_rowconfigure(5, weight=1)

# event bindings listbox + gift sending dbl click + enter
lbox.bind('<<ListboxSelect>>', showPopul)
lbox.bind('<Double-1>', sendGift)
root.bind('<Return>', sendGift)

# colorize listbox items
for i in range(0, len(ctrnames), 2):
  lbox.itemconfigure(i, bg='lightgray')

# initialize
gift.set('card')
sentmsg.set('')
statusmsg.set('')
lbox.selection_set(0)
showPopul()
root.mainloop()
