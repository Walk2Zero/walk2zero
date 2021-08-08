"""Login page"""
"""Importing modules"""
from tkinter import *
import tkinter.font as font
from PIL import ImageTk, Image

root=Tk()
root.geometry("200x200+600+200")
root.title("Walk2Zero")
"""Bckground image"""
img = ImageTk.PhotoImage(Image.open("walk2zeo2.jpg"))
label_image=Label(root, image=img)
label_image.place(x=0,y=0,relwidth=1,relheight=1)

"""Top Heading"""

label1= Label(root, text="Hi! I'm E@rth, Happy Walking ", fg='black', font="Head_font",bg="#fcf5cc").place(x=600, y=20)
Head_font=font.Font(family="Helvetica", weight="bold", size="500")
""" Second heading-login"""
label11= Label(root, text="Already registered!!! Please login ", fg='#069000', bg="#fcf5cc",font="label11_font").place(x=620,y=200)
label11_font=font.Font(weight="bold", size="100")
""" Text entry boxes"""
label2= Entry(root,justify="center",bd='4px', font = ('Helvetica',10,'bold')).place(x=750, y=260)
label3= Entry(root, justify="center",show='*',bd='4px', font = ('Helvetica',10,'bold')).place(x=750, y=300)
"""Labels for entry boxes"""
label_1=Label(root,text="Enter Username",fg='#069000', bg="#fcf5cc").place(x=620, y=260)
label_2=Label(root,text="Enter Password",fg='#069000', bg="#fcf5cc").place(x=620, y=300)

"""Submit button"""
label6=Button(root, text="Submit").place(x=730, y=350)

root.mainloop()