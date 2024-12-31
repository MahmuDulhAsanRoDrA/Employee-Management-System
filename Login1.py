from customtkinter import *
from PIL import Image
from customtkinter import CTkImage
from tkinter import  messagebox

#Function part
def login():
    if userEntry.get()=='' or passEntry.get()=='':
        messagebox.showerror('Error','Fields Cannot be empty')
    elif userEntry.get()=='admin' and passEntry.get()=='1234':
        messagebox.showinfo('Success','Login is successful')
        root.destroy()
        import Menu

    elif userEntry.get()=='attender' and passEntry.get()=='2001':
        messagebox.showinfo('Success','Login is successful')
        root.destroy()
        import Attendence
    else:
       messagebox.showerror('Error', 'Wrong user and password')


#Gui Part
root=CTk()
app_w=1280
app_h=594
s_w=root.winfo_screenwidth()
s_h=root.winfo_screenheight()
x=(s_w/2)-(app_w/2)
y=(s_h/2)-(app_h/2)
root.geometry(f'{app_w}x{app_h}+{int(x)}+{int(y)}')
root.resizable(0,0)
root.title('Login page')
image=CTkImage(Image.open('Ctrl.png'),size=(app_w,app_h))
imageLabel=CTkLabel(root,image=image,text='')
imageLabel.place(x=0,y=0)
headinglabel=CTkLabel(root,text='Login using user \n name and password ',font=('Arial',25,'bold'),text_color='Black',bg_color='White')
headinglabel.place(x=50,y=50)

userEntry=CTkEntry(root,placeholder_text='Enter Your User Name',width=180,bg_color='white')
userEntry.place(x=50,y=150)

passEntry=CTkEntry(root,placeholder_text='Enter Your Password',width=180,show='*',bg_color='White')
passEntry.place(x=50,y=200)

login=CTkButton(root,text='Login',cursor='hand2',command=login,bg_color='White')
login.place(x=70,y=250)

root.mainloop()
