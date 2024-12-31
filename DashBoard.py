from customtkinter import *
from tkinter import ttk, messagebox, Frame, PhotoImage
import db
from db import connect_db

# Define global labels to access them in the update function
total_emp_count_label = None
total_attend_count_label = None
total_task_count_label = None
total_complete_count_label = None


def update():
    cursor, connection = connect_db()
    if not cursor or not connection:
        return
    cursor.execute('use employee_data')

    # Update Total Employee count
    cursor.execute('Select * from data')
    records = cursor.fetchall()
    print(records)
    total_emp_count_label.config(text=len(records))


    # Update Total Attendance count
    cursor.execute('Select * from attendence_table')
    records = cursor.fetchall()
    print(records)
    total_attend_count_label.config(text=len(records))




def Dsh_form(window):
    global total_emp_count_label, total_attend_count_label, total_task_count_label, total_complete_count_label

    # DshFrame with .place() to fill the window
    DshFrame = CTkFrame(window, fg_color='#363C40', height=550, width=1150)
    DshFrame.place(relx=0, rely=0, relwidth=1, relheight=1)

    # Header Frame with grid to adjust dynamically
    header_frame = CTkFrame(DshFrame, fg_color='#7A94B6')
    header_frame.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=10, pady=(10, 5))

    # Title Label in header frame, with centering adjustment
    normal_label = CTkLabel(header_frame, text="DashBoard", font=("Arial", 40, "bold"), text_color="White")
    normal_label.grid(row=0, column=1, padx=(20, 10), pady=20, sticky="nsew")

    # Adjust row and column configurations for scaling
    DshFrame.grid_rowconfigure(0, weight=0)  # Ensure header row doesn't stretch too much
    DshFrame.grid_rowconfigure(1, weight=1)  # Content area expands to fill available space
    DshFrame.grid_columnconfigure(0, weight=1)  # Column 0 takes full width for proper alignment

    # Ensure the header frame also adjusts within the grid area
    header_frame.grid_columnconfigure(1, weight=1)  # Ensures the label is centered in the header frame

    # EmpFrame with .place() for consistent geometry management
    EmpFrame = Frame(DshFrame, bg='White', bd=3, relief=RIDGE)
    EmpFrame.place(x=400, y=135, height=190, width=280)  # Adjust these values for desired position and size

    total_emp_icon = PhotoImage(file='Emp.png')
    total_emp_icon_label = CTkLabel(EmpFrame, text='', image=total_emp_icon)
    total_emp_icon_label.image = total_emp_icon  # Keep a reference to the image
    total_emp_icon_label.pack(pady=10)

    total_emp_label = CTkLabel(EmpFrame, text='Total Employee', text_color='black', font=('arial', 18, 'bold'))
    total_emp_label.pack()

    total_emp_count_label = CTkLabel(EmpFrame, text='0', text_color='black', font=('arial', 18, 'bold'))
    total_emp_count_label.pack()

    # Attendance Frame
    attendFrame = Frame(DshFrame, bg='White', bd=3, relief=RIDGE)
    attendFrame.place(x=800, y=135, height=190, width=280)  # Adjust these values for desired position and size

    total_attend_icon = PhotoImage(file='attend.png')
    total_attend_icon_label = CTkLabel(attendFrame, text='', image=total_attend_icon)
    total_attend_icon_label.image = total_attend_icon  # Keep a reference to the image
    total_attend_icon_label.pack(pady=10)

    total_attend_label = CTkLabel(attendFrame, text='Total Attend Today', text_color='black',
                                  font=('arial', 18, 'bold'))
    total_attend_label.pack()

    total_attend_count_label = CTkLabel(attendFrame, text='0', text_color='black', font=('arial', 18, 'bold'))
    total_attend_count_label.pack()

    # Task Frame
    taskFrame = Frame(DshFrame, bg='White', bd=3, relief=RIDGE)
    taskFrame.place(x=400, y=340, height=190, width=280)

    total_task_icon = PhotoImage(file='task.png')
    total_task_icon_label = CTkLabel(taskFrame, text='', image=total_task_icon)
    total_task_icon_label.image = total_task_icon  # Keep a reference to the image
    total_task_icon_label.pack(pady=10)

    total_task_label = CTkLabel(taskFrame, text='Total Tasks Today', text_color='black', font=('arial', 18, 'bold'))
    total_task_label.pack()

    total_task_count_label = CTkLabel(taskFrame, text='0', text_color='black', font=('arial', 18, 'bold'))
    total_task_count_label.pack()

    # Complete Frame
    completeFrame = Frame(DshFrame, bg='White', bd=3, relief=RIDGE)
    completeFrame.place(x=800, y=340, height=190, width=280)  # Adjust these values for desired position and size

    total_complete_icon = PhotoImage(file='goal.png')
    total_complete_icon_label = CTkLabel(completeFrame, text='', image=total_complete_icon)
    total_complete_icon_label.image = total_complete_icon  # Keep a reference to the image
    total_complete_icon_label.pack(pady=10)

    total_complete_label = CTkLabel(completeFrame, text='Complete Tasks Today', text_color='black',
                                    font=('arial', 18, 'bold'))
    total_complete_label.pack()

    total_complete_count_label = CTkLabel(completeFrame, text='0', text_color='black', font=('arial', 18, 'bold'))
    total_complete_count_label.pack()

# Call the update function to refresh the dashboard values
# Ensure you call update() somewhere in the program after the window is created
