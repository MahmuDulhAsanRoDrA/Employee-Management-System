from customtkinter import *
from  PIL import Image
from tkinter import ttk, messagebox
import db
import re

#Funtions

def delete_all_emp():
    results=messagebox.askyesno('Confirm',"Do you really want to delete all records")
    if results:
        db.delete_all()
def search_emp():
    if searchentry.get()=='':
        messagebox.showerror('Error','Enter value to search')
    elif searchbox.get() =='Search By' :
        messagebox.showerror('Error', 'Select a Role')
    else:
        searched_data=db.search(searchbox.get(),searchentry.get())
        tree.delete(*tree.get_children())
        for employee in searched_data:
            tree.insert('', END, values=employee)
def delete_emp():
    selected=tree.selection()
    if not selected:
        messagebox.showerror('Error', 'Select Data to Delete')
    else:
        db.delete(idEntry.get())
        treeview_data()
        clear()
        messagebox.showinfo('Deleted',"Employee data have been deleted")
def select(event):

    selected=tree.selection()
    if selected:
        row =  tree.item(selected)['values']
        clear()
        idEntry.insert(0, row[0])
        nameEntry.insert(0,row[1])
        #phoneEntry.insert(0,row[2])
        contact_number = str(row[2])
        #if not contact_number.startswith("0"):
        contact_number = "0" + contact_number
        phoneEntry.insert(0, contact_number)
        roleBox.set(row[3])
        genderbox.set(row[4])
        salaryEntry.insert(0,row[5])
        emailEntry.insert(0,row[6])
def clear(value = False):
    if value:
        tree.selection_remove(tree.focus())
    idEntry.delete(0,END)
    nameEntry.delete(0,END)
    phoneEntry.delete(0,END)
    roleBox.set('Select Here')
    genderbox.set('Select Here')
    salaryEntry.delete(0,END)
    emailEntry.delete(0,END)
def treeview_data():
    employees = db.fetch_employees()
    tree.delete(*tree.get_children())
    for employee in employees:
        tree.insert('',END,values=employee)
# Validation function
def validate_phone_number(phone):

    if re.fullmatch(r'^(017|018|019|016|014|015|013)\d{8}$', phone):
        return True
    else:
        return False
# Validation function for specific email domains with lowercase requirement before @
def validate_email(email):

    if re.fullmatch(r'^[a-z\d\.-]+@(gmail.com|yahoo.com|hotmail.com)$', email):
        return True
    else:
        return False

def add_employ():
    if idEntry.get() == '' or phoneEntry.get() == '' or nameEntry.get() == '' or salaryEntry.get() == '' or emailEntry.get()== '':
        messagebox.showerror('Error', 'Fill all Fields')
    elif not validate_phone_number(phoneEntry.get()):
        messagebox.showerror('Error', 'Enter a valid phone number)')
    elif not validate_email(emailEntry.get()):
        messagebox.showerror('Error', 'Enter a valid email address')
    elif db.id_exist(idEntry.get()):
        messagebox.showerror('Error', 'ID already exists')
    elif db.phone_exist(phoneEntry.get()):
        messagebox.showerror('Error', 'Phone Number already exists')
    elif db.email_exist(emailEntry.get()):
        messagebox.showerror('Error', 'Email already exists')
    else:
        db.insert(idEntry.get(), nameEntry.get(), phoneEntry.get(), roleBox.get(), genderbox.get(), salaryEntry.get(), emailEntry.get())
        treeview_data()
        clear()
        messagebox.showinfo('Success', 'Data is added')

def update_Employee():
    selected = tree.selection()
    if not selected:
        messagebox.showerror('Error', 'Select Data to update')
    elif not validate_phone_number(phoneEntry.get()):
        messagebox.showerror('Error', 'Enter a valid phone number ')
    elif not validate_email(emailEntry.get()):
        messagebox.showerror('Error', 'Enter a valid email address ')

    else:
        db.update( nameEntry.get(), phoneEntry.get(), roleBox.get(), genderbox.get(), salaryEntry.get(), emailEntry.get())
        messagebox.showerror('Success','Your Data Is Updated')
        treeview_data()


#Gui part

window=CTk()
app_w=1280
app_h=594
s_w=window.winfo_screenwidth()
s_h=window.winfo_screenheight()
x=(s_w/2)-(app_w/2)
y=(s_h/2)-(app_h/2)
window.geometry(f'{app_w}x{app_h}+{int(x)}+{int(y)}')
window.resizable(False,False)
window.title('Employ Management System')
window.configure(fg_color='#363C40')


logo=CTkImage(Image.open('bg.png'),size=(1280,150))
logoLabel=CTkLabel(window,image=logo,text='')
logoLabel.grid(row=0,column=0,columnspan=2)

leftFrame=CTkFrame(window,fg_color='#363C40')
leftFrame.grid(row=1,column=0)

idLabel=CTkLabel(leftFrame,text='ID',font=('arial',18,'bold'),text_color='white')
idLabel.grid(row=0,column=0,padx=20,pady=10,sticky='w')

idEntry=CTkEntry(leftFrame,font=('arial',15,'bold'),width=180)
idEntry.grid(row=0,column=1)

nameLabel=CTkLabel(leftFrame,text='Name',font=('arial',18,'bold'),text_color='white')
nameLabel.grid(row=1,column=0,padx=20,pady=10,sticky='w')

nameEntry=CTkEntry(leftFrame,font=('arial',15,'bold'),width=180)
nameEntry.grid(row=1,column=1)

phoneLabel=CTkLabel(leftFrame,text='Phone NO',font=('arial',18,'bold'),text_color='white')
phoneLabel.grid(row=2,column=0,padx=20,pady=10,sticky='w')

phoneEntry=CTkEntry(leftFrame,font=('arial',15,'bold'),width=180)
phoneEntry.grid(row=2,column=1)

roleLabel=CTkLabel(leftFrame,text='Role',font=('arial',18,'bold'),text_color='white')
roleLabel.grid(row=3,column=0,padx=20,pady=10,sticky='w')
role_options=['Web Developer','Technical Writer','Network Engineer','Data Scientist','ux/ui Designer']
roleBox=CTkComboBox(leftFrame,values=role_options,width=180,font=('arial',15,'bold'),state='readonly')
roleBox.grid(row=3,column=1)
roleBox.set('Select Here')

genderLabel=CTkLabel(leftFrame,text='Gender',font=('arial',18,'bold'),text_color='white')
genderLabel.grid(row=4,column=0,padx=20,pady=10,sticky='w')
gender_options=['Male','Female']

genderbox=CTkComboBox(leftFrame,values=gender_options,width=180,font=('arial',15,'bold'),state='readonly')
genderbox.grid(row=4,column=1)
genderbox.set('Select Here')

salarylabel=CTkLabel(leftFrame,text='Salary',font=('arial',18,'bold'),text_color='white')
salarylabel.grid(row=5,column=0,padx=20,pady=10,sticky='w')

salaryEntry=CTkEntry(leftFrame,font=('arial',15,'bold'),width=180)
salaryEntry.grid(row=5,column=1)

emaillabel=CTkLabel(leftFrame,text='Email',font=('arial',18,'bold'),text_color='white')
emaillabel.grid(row=6,column=0,padx=20,pady=10,sticky='w')

emailEntry=CTkEntry(leftFrame,font=('arial',15,'bold'),width=180)
emailEntry.grid(row=6,column=1)

rightframe=CTkFrame(window,fg_color='#21A698')
rightframe.grid(row=1,column=1)

search_options=['ID','Name','Phone No','Role','Gender','Salary','Email']
searchbox=CTkComboBox(rightframe,values=search_options,state='readonly')
searchbox.grid(row=0,column=0)
searchbox.set('Search By')

searchentry=CTkEntry(rightframe,placeholder_text='Enter ',width=180)
searchentry.grid(row=0,column=1)


searchButton=CTkButton(rightframe,text='Search',width=100,command=search_emp)
searchButton.grid(row=0,column=2)

showallButton=CTkButton(rightframe,text='Show All',width=100,command=treeview_data)
showallButton.grid(row=0,column=3,pady=5)

tree=ttk.Treeview(rightframe,height=9)
tree.grid(row=1,column=0,columnspan=4,)

tree['column']=('ID','Name','Phone No','Role','Gender','Salary','Email')
tree.heading('ID',text='Id')
tree.heading('Name',text='Name')
tree.heading('Phone No',text='Phone')
tree.heading('Role',text='Role')
tree.heading('Gender',text='Gender')
tree.heading('Salary',text='Salary')
tree.heading('Email',text='Email')

tree.config(show='headings')
tree.column('ID',width=50)
tree.column('Name',width=160)
tree.column('Phone No',width=110)
tree.column('Role',width=100)
tree.column('Gender',width=100)
tree.column('Salary',width=120)
tree.column('Email',width=140)

style=ttk.Style()
style.configure('Treeview.Heading',font=('arial',18,'bold'))
style.configure('Treeview',font=('arial',13,'bold'),rowheight=30,background='#363C40',foreground='#F2F2F2')

scroll1=ttk.Scrollbar(rightframe,orient=VERTICAL)
scroll1.grid(row=1,column=4,sticky='ns')
scroll2=ttk.Scrollbar(rightframe,orient=HORIZONTAL)
scroll2.grid(row=2,column=0,columnspan=5,sticky='ew')


buttonframe=CTkFrame(window,fg_color='#363C40')
buttonframe.grid(row=2,column=0,columnspan=2)

newbutton=CTkButton(buttonframe,text='Clear Entries',font=('arial',15,'bold'),height=50,width=160,corner_radius=15,command=lambda: clear(True))
newbutton.grid(row=0,column=0,padx=5,pady=10)

addbutton=CTkButton(buttonframe,text='Add Employee',font=('arial',15,'bold'),height=50,width=160,corner_radius=15,command=add_employ)
addbutton.grid(row=0,column=1,padx=5)

updatebutton=CTkButton(buttonframe,text='Update Employee',font=('arial',15,'bold'),height=50,width=160,corner_radius=15,command= update_Employee)
updatebutton.grid(row=0,column=2,padx=5)

deletebutton=CTkButton(buttonframe,text='Delete Employee',font=('arial',15,'bold'),height=50,width=160,corner_radius=15,command=delete_emp)
deletebutton.grid(row=0,column=3,padx=5)

deleteallbutton=CTkButton(buttonframe,text='Delete All',font=('arial',15,'bold'),height=50,width=160,corner_radius=15,command=delete_all_emp)
deleteallbutton.grid(row=0,column=4,padx=5)

returnButton=CTkButton(window,text='<--',font=('arial',30,'bold'))
returnButton.place(x=2,y=2)


treeview_data()

window.bind('<ButtonRelease>', select)


window.mainloop()