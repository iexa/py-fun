import tkinter as tk
from tkinter import ttk


class HelloView(tk.Frame):
  """ geco kis tk cucc """

  def __init__(self, parent, *args, **kwargs):
    super().__init__(parent, *args, **kwargs)

    self.name = tk.StringVar()
    self.hello_str = tk.StringVar()
    self.hello_str.set("Hello Gecccco")

    name_lbl = ttk.Label(self, text="Name:")
    name_entry = ttk.Entry(self, textvariable=self.name)
    change_btn = ttk.Button(self, text='Change', command=self.on_change)
    hello_lbl = ttk.Label(self, textvariable=self.hello_str,
                  font=('TkDefaultFont', 64), wraplength=600)

    # layout
    name_lbl.grid(row=0, column=0, sticky=tk.W)
    name_entry.grid(row=0, column=1, sticky=(tk.W + tk.E))
    change_btn.grid(row=0, column=2, sticky=tk.E)
    hello_lbl.grid(row=1, column=0, columnspan=3)
    self.columnconfigure(1, weight=1)

  def on_change(self):
    if self.name.get().strip():
      self.hello_str.set("Hellllo " + self.name.get())
    else:
      self.hello_str.set("Hello ?!")

# ----------


class MyApp(tk.Tk):
  """ Main Tk code """

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.title('Hello TkInter')
    self.geometry('500x300')
    # self.resizable(width=False, height=False)

    HelloView(self).grid(sticky='ewns')
    self.columnconfigure(0, weight=1)


if __name__ == '__main__':
  app = MyApp()
  app.mainloop()
