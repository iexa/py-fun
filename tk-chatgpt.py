"""" small tkinter gui app - using chatgpt api
	
	You need to register and get a chatgpt api key to use this.
	The key is deliberately not saved anywhere as it is a small app.
	I also know that its structure is crappy, again small poc app.
	
"""
import tkinter as tk
import customtkinter as ctk
import openai
from openai.error import AuthenticationError
import os
import string
from async_tkinter_loop import async_handler, async_mainloop

# async_tkinter_loop does not check for closure of main window thus some errors
# when exiting the app... not critical, leave it for now

class GPT():
	_apikey = ''
	
	@classmethod
	async def speak(cls, event=None):
		#print(cls._apikey)
		if not cls.is_api_set():
			cls.clear()
			tmain.insert(tk.END, "\n\nAPI key not set - I can't chat until you've set it!\n\n")
			return
		#print(entry.get())
		tmain.insert(tk.END, f"\n ⏳ {entry.get()}")
		tmain.see(tk.END)  # scroll to end always
		cls.clear_entry()
		openai.api_key = cls._apikey
		try:
			resp = await openai.Completion.acreate(
				model='text-davinci-003', prompt=entry.get(),
				temperature=0.8, max_tokens=40)
			tmain.insert(tk.END, f"\n{resp.choices[0].text.strip()}\n")
		except AuthenticationError:
			tmain.insert(tk.END, "\n\nAPI key is invalid! Check it or get a new one.\n\n")
		tmain.see(tk.END) 
		
	@classmethod
	def edit_api(cls, error_text=''):
		valid_chars = string.ascii_letters + string.digits + '+_-'
		argsextra = {}
		if error_text:
			argsextra = {"entry_fg_color": "red"}
		dialog = ctk.CTkInputDialog(
			text="Please type your personal chatgpt api key\n(it is saved until app closed):",
			title=f"{error_text} 🍕👀",
			**argsextra)
		key = dialog.get_input()
		if not key: #if empty then close
			btn_api.configure(fg_color='#1f538d')
			return
		if not all([x in valid_chars for x in key]): # if invalid, re-call itself
			btn_api.configure(fg_color='#1f538d')
			return cls.edit_api(error_text="Api key has invalid chars...")
		btn_api.configure(fg_color='darkgreen')
		cls._apikey = key
		
	@classmethod
	def is_api_set(cls):
		return 1 if cls._apikey else 0
		
	@classmethod	
	def clear(cls):
		tmain.delete(1.0, tk.END)
		cls.clear_entry()
	
	@staticmethod
	def clear_entry():
		entry.delete(0, tk.END)


root = ctk.CTk()
root.title("ChatGPT f-yeee")
root.geometry("700x480")
root.minsize(500, 380)
#root.iconbitmap("ai_lt.ico")

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")
font_main = ctk.CTkFont(family="Roboto", size=16)

tframe = ctk.CTkFrame(root)
tframe.pack(pady=10, padx=10, expand=True, fill=tk.BOTH) # how it's packed into parent
tframe.grid_columnconfigure(0, weight=1) # this is also the grid's parent
tframe.grid_rowconfigure(0, weight=1)

tmain = tk.Text(tframe, bg="#333333", fg="#d5d5d5", 
		bd=1, relief="flat",
		height=0, wrap=tk.WORD,
		font=font_main,
		selectbackground="#1f558f", insertbackground='gray')
tmain.grid(row=0, column=0, sticky='nsew')

tscroll = ctk.CTkScrollbar(tframe, command=tmain.yview)
tscroll.grid(row=0, column=1, sticky=tk.NS + tk.W)
tmain.configure(yscrollcommand=tscroll.set)

# input entry box
entry = ctk.CTkEntry(root, placeholder_text="Say Hi to chatGPT!",
		width=60, height=50, border_width=1)
entry.bind("<KeyPress-Return>", async_handler(GPT.speak)) #if enter hit also call GPT.speak
entry.pack(pady=10, padx=15, fill=tk.X)


# buttons: submit text, clear scr, edit api key 
frm_buttons = ctk.CTkFrame(root, fg_color="#333333")
frm_buttons.pack(pady=10, side=tk.BOTTOM)

btn_submit = ctk.CTkButton(frm_buttons, text="Send to chatGPT", command=async_handler(GPT.speak))
btn_submit.grid(row=0, column=0, pady=10, padx=10)
btn_clear = ctk.CTkButton(frm_buttons, text="Clear text", command=GPT.clear)
btn_clear.grid(row=0, column=1, padx=10)
btn_api = ctk.CTkButton(frm_buttons, text="Edit API key", command=GPT.edit_api)
btn_api.grid(row=0, column=2, padx=10)


if __name__ == '__main__':
	async_mainloop(root)

		
		