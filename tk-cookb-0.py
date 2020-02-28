#!/usr/bin/env python3
"""Python cookbook test #0."""
import tkinter as tk
from tkinter import ttk


def handler():
  """Handle clicks."""
  act.configure(text="Hello " + name.get() + ' ' + nmr.get())
  # a_lbl.configure(foreground='red', text='miafasz?')


win = tk.Tk()
win.title("faszom téká #1")
win.resizable(0, 0)
win.configure(background="red")


tk.Label(win, text="neved, gecc: ") \
    .grid(column=0, row=0)
name = tk.StringVar()
name_entered = ttk.Entry(win, width=12, textvariable=name)
name_entered.grid(column=0, row=1)
name_entered.focus()

act = tk.Button(win, text="madzagoljá!", command=handler)
act.grid(column=2, row=1)
# act.configure(state='disabled')

tk.Label(win, text="szam, he: ") \
    .grid(column=1, row=0)
nmr = tk.StringVar()
nmr_pick = ttk.Combobox(win, width=12, state='readonly', textvariable=nmr)
nmr_pick['values'] = (1, 2, 4, 42, 88, 100)
nmr_pick.grid(column=1, row=1)
nmr_pick.current(0)


win.mainloop()
