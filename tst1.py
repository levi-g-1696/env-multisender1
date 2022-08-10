from  tkinter import *

window = Tk()
window.title("Guessing Game")

welcome = Label(window, text="Welcome To The Guessing Game!", background="blue", foreground="white")
welcome.grid(row=0, column=0, columnspan=3)

def Rules():
   rule_window = Toplevel(window)
   rule_window.title("The Rules")
   the_rules = Label(rule_window, text="Here are the rules...", foreground="red")
   the_rules.grid(row=0, column=0, columnspan=3)

rules = Button(window, text="Rules", command=Rules)
rules.grid(row=1, column=0, columnspan=1)

window.mainloop()