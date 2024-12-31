from customtkinter import *
from tkinter import messagebox
from PIL import Image
from customtkinter import CTkImage

# Function part
def login():
    if userEntry.get() == '' or passEntry.get() == '':
        messagebox.showerror('Error', 'Fields Cannot be empty')
    elif userEntry.get() == 'attender' and passEntry.get() == '2001':
        messagebox.showinfo('Success', 'Login is successful')
        Attend.destroy()
        import Attendence
    else:
        messagebox.showerror('Error', 'Wrong user and password')

# GUI Part
Attend = CTk()
app_w, app_h = 550, 500
s_w = Attend.winfo_screenwidth()
s_h = Attend.winfo_screenheight()
x = (s_w / 2) - (app_w / 2)
y = (s_h / 2) - (app_h / 2)
Attend.geometry(f'{app_w}x{app_h}+{int(x)}+{int(y)}')
Attend.resizable(0, 0)
Attend.title('Attender Login Page')

# Load the background image and set its size
image = CTkImage(Image.open('attend.jpg'), size=(app_w, app_h))
imageLabel = CTkLabel(Attend, image=image, text='')
imageLabel.place(x=0, y=0)

# Center widgets dynamically
center_x = app_w // 2
headinglabel = CTkLabel(Attend, text='Enter Your Id \n And Pass', font=('Arial', 25, 'bold'), text_color='Black', bg_color='White')
headinglabel.place(relx=0.5, y=50, anchor='center')

userEntry = CTkEntry(Attend, placeholder_text='Enter Your User Name', width=250, bg_color='White')
userEntry.place(relx=0.5, y=150, anchor='center')

passEntry = CTkEntry(Attend, placeholder_text='Enter Your Password', width=250, show='*', bg_color='White')
passEntry.place(relx=0.5, y=200, anchor='center')

login = CTkButton(Attend, text='Login', cursor='hand2', command=login, bg_color='White')
login.place(relx=0.5, y=250, anchor='center')

Attend.mainloop()
