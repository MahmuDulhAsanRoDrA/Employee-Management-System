from tkinter import ttk, messagebox
from customtkinter import *
import datetime
import db

# Main window setup
def setup_main_window():
    main_frame = CTk()
    app_w, app_h = 550, 500
    s_w, s_h = main_frame.winfo_screenwidth(), main_frame.winfo_screenheight()
    x, y = (s_w / 2) - (app_w / 2), (s_h / 2) - (app_h / 2)
    main_frame.geometry(f'{app_w}x{app_h}+{int(x)}+{int(y)}')
    main_frame.resizable(0, 0)
    main_frame.title("Attendance System")
    return main_frame

# Populate Treeview with IDs from database
def id_list_view():
    id_list = db.fetch_ID()
    for record_id in id_list:
        id_tree.insert('', 'end', values=record_id)

# Function to search for an employee and update the entry box

def clr():
    sBox.delete(0,END)
def upd():
    ans=messagebox.askyesno('Warning',"Do you want to update today's \n Date and ID?")
    if ans:
        db.update_info()
def search_id(ID):
    id=ID
    idCheck=db.id_exist(id)
    if idCheck:
        idPcheck=db.p_check(id)
        print(idPcheck)
        if idPcheck == 1:
            stat=db.stat(id)
            statLabel.configure(text=f"Status: {str(stat)}")
            pT=db.p_T(id)
            p_Time.configure(text=f"Present Time: {pT}")
            lT=db.l_T(id)
            l_Time.configure(text=f"leave Time: {lT}")
        else:
            stat = db.stat(id)
            statLabel.configure(text=f"Status: {str(stat)}")
            pT = db.p_T(id)
            p_Time.configure(text=f"Present Time: {pT}")
            lT = db.l_T(id)
            l_Time.configure(text=f"leave Time: {lT}")

    else:
         messagebox.showerror('Error', 'No ID found')
# Function to handle marking attendance
def mark_present():
    employee_id = sBox.get()
    if employee_id:
        date, time = db.mark_present(employee_id)
        statLabel.configure(text="Status: Present")
        p_Time.configure(text=f"Present Time: {time}")
        messagebox.showinfo("Marked Present", f"Employee {employee_id} marked as present on \n {date} at {time}.")
    else:
        messagebox.showerror("Error", "Please enter or select an Employee ID")
def mark_leave():
    employee_id = sBox.get()
    if employee_id:
        date, time = db.mark_leave(employee_id)
        statLabel.configure(text="Status: Present")
        l_Time.configure(text=f"Leave Time: {time}")
        messagebox.showinfo("Marked Present", f"Employee {employee_id} marked as leave on \n{date} at {time}.")
    else:
        messagebox.showerror("Error", "Please enter or select an Employee ID")

# Left frame for date and ID list
def create_left_frame(main_frame):
    left_frame = CTkFrame(main_frame, fg_color='#2C3E50', corner_radius=10)
    left_frame.pack(side='left', expand=True, fill='both', padx=5, pady=5)

    # Date Display
    today = datetime.date.today()
    date_frame = CTkFrame(left_frame, fg_color='#34495E', height=60, corner_radius=10)
    date_frame.pack(side='top', fill='x', padx=10, pady=10)
    date_label = CTkLabel(date_frame, text=f'DATE: {today}', font=('Arial', 20, 'bold'), text_color='white')
    date_label.pack(pady=10)

    # ID List Display
    id_list_frame = CTkFrame(left_frame, fg_color='#3C6E71', corner_radius=10)
    id_list_frame.pack(side='top', expand=True, fill='both', padx=10, pady=10)

    global id_tree
    id_tree = ttk.Treeview(id_list_frame, columns=('ID',), show='headings', height=8)
    id_tree.heading('ID', text='Employee ID')
    id_tree.column('ID', anchor='center', width=100)
    id_tree.pack(padx=10, pady=10, expand=True, fill='both')


    # Treeview Styling
    id_style = ttk.Style()
    id_style.configure('Treeview.Heading', font=('arial', 18, 'bold'),background='#34495E', foreground='black')
    id_style.configure('Treeview', font=('arial', 13, 'bold'), rowheight=30, background='#363C40', foreground='#F2F2F2')



    return left_frame
def on_tree_select():

    selected_item = id_tree.selection()
    if selected_item:
        emp_id = id_tree.item(selected_item)['values'][0]
        sBox.delete(0, 'end')
        sBox.insert(0, emp_id)
        search_id(emp_id)

def create_right_frame(main_frame):
    right_frame = CTkFrame(main_frame, fg_color='#EAEDED', corner_radius=10)
    right_frame.pack(side='left', expand=True, fill='both', padx=5, pady=5)

    # Search Box
    global sBox
    sBox = CTkEntry(right_frame, placeholder_text='Enter Your ID', height=48, font=('Arial', 18), border_width=1)
    sBox.pack(padx=15, pady=(15, 5), fill='x')

    buttonGrid=CTkFrame(right_frame,fg_color='#EAEDED')
    buttonGrid.pack(side='top')
    # Search Button
    search_button = CTkButton(buttonGrid, text='Search', font=('Arial', 18, 'bold'), width=100, command=lambda :search_id(sBox.get()))
    search_button.grid(row=0,column=0,padx=10)

    clear_button = CTkButton(buttonGrid, text='clear', font=('Arial', 18, 'bold'), width=100,command=clr)
    clear_button.grid(row=0,column=1,padx=10)
    id_tree.bind("<<TreeviewSelect>>", lambda e: on_tree_select())

    # Status Frame
    global statLabel, p_Time , l_Time
    status_frame = CTkFrame(right_frame, fg_color='#F4D03F', height=80, corner_radius=10)
    status_frame.pack(side='top', padx=15, pady=10, fill='x')
    statLabel = CTkLabel(status_frame, text=f"Status: ", font=('Arial', 24, 'bold'))
    statLabel.pack(pady=10)

    # Present Frame

    present_frame = CTkFrame(right_frame, fg_color='#58D68D', height=80, corner_radius=10)
    present_frame.pack(side='top', padx=15, pady=10, fill='x')
    p_button=CTkButton(present_frame, text='Mark Present', font=('Arial', 20, 'bold'),command=mark_present)
    p_button.pack(side='top',fill='x')
    p_Time = CTkLabel(present_frame, text='Present Time: -', font=('Arial', 16))
    p_Time.pack()

    leave_frame = CTkFrame(right_frame, fg_color='#58D68D', height=80, corner_radius=10)
    leave_frame.pack(side='top', padx=15, pady=10, fill='x')
    l_button=CTkButton(leave_frame,text='Mark leave',font=('Arial',20,'bold'),command=mark_leave)
    l_button.pack(side='top',fill='x')

    l_Time = CTkLabel(leave_frame, text='Leave Time: -', font=('Arial', 16))
    l_Time.pack()


    updateButton=CTkButton(right_frame,text='Update',font=('Arial',20),height=25,command=upd)
    updateButton.pack(anchor='n',pady=30,side='top')
    updatelabel = CTkLabel(right_frame, text='Note-Click Update Button \n Starting Of The Day', font=('Arial', 20, 'bold'),text_color='Red')
    updatelabel.pack(padx=10,pady=10,side='top')
    return right_frame

# Initialize application
main_frame = setup_main_window()
create_left_frame(main_frame)
create_right_frame(main_frame)
id_list_view()

main_frame.mainloop()
