"""Transport page"""

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
"""Heading label"""
label1= Label(root, text="Hi! I'm E@rth, Happy Walking ", font="Head_font", fg="#069000", bg="#fcf5cc").place(x=650, y=20)
Head_font=font.Font(family="Helvetica", weight="bold", size="500")
"""second heading label"""
label11= Label(root, text="Hi,there!! which one you prefer today ", fg='#069000', bg="#fcf5cc", font="label11_font",).place(x=620,y=100)

"""Check buttins for transport"""
c1=Checkbutton(root, text="Walk",fg='#069000', bg="#fcf5cc").place(x=720,y=200)
c2=Checkbutton(root, text="Bicycle",fg='#069000', bg="#fcf5cc").place(x=720,y=250)
c3=Checkbutton(root, text="Scooter",fg='#069000', bg="#fcf5cc").place(x=720,y=300)
c4=Checkbutton(root, text="Car",fg='#069000', bg="#fcf5cc").place(x=720,y=350)


def onclick():
    label=Label(root,text="Wow!! will go ahead and calculate emissions ", fg="green", font=("Helvetica", "20")).place(x=540,y=450)


"""Submit button"""
label6=Button(root, text="Submit", command=onclick).place(x=720, y=400)
root.mainloop()