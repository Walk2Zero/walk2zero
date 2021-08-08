from tkinter import *
import tkinter.font as font
from PIL import ImageTk, Image

root=Tk()
root.geometry("200x200+600+200")
"""Titles"""
root.title("Walk2Zero")
img = ImageTk.PhotoImage(Image.open("walk2zero1.jpg"))
label_image=Label(root, image=img)
label_image.place(x=0,y=0,relwidth=1,relheight=1)

"""Text head"""
label1= Label(root, text="Hi! I'm E@rth, Happy Walking ", fg='black', font="Head_font",bg="#e28743").place(x=600, y=20)
Head_font=font.Font(family="Helvetica", weight="bold", size="500")
"""Second heading-registration"""
label11= Label(root, text="New User Registration ", fg='Black', font="label11_font", bg="#e28743").place(x=640,y=100)
label11_font=font.Font(weight="bold", size="100")
"""Text entry"""
label2= Entry(root,justify="center",bd='4px', font = ('Helvetica',10,'bold')).place(x=750, y=160)
label3= Entry(root, justify="center",bd='4px', font = ('Helvetica',10,'bold')).place(x=750, y=200)
label4= Entry(root,show='*', justify="center",bd='4px', font = ('Helvetica',10,'bold')).place(x=750, y=240)
label5= Entry(root, show='*', justify="center",bd='4px', font = ('Helvetica',10,'bold')).place(x=750, y=280)

"""Submit button"""
label6=Button(root, text="Submit", bg="#eeeee4").place(x=750, y=320)

"""label names"""

label_1=Label(root,text="Enter Username",bg="#e28743",fg="black").place(x=620, y=160)
label_2=Label(root,text="Enter Email Address", bg="#e28743",fg="black").place(x=620, y=200)
label_3=Label(root,text="New Password",bg="#e28743",fg="black").place(x=620, y=240)
label_4=Label(root,text="Confirm password",bg="#e28743",fg="black").place(x=620, y=280)
root.mainloop()
