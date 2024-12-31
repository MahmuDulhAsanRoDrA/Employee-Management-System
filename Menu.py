from customtkinter import *
import time
from datetime import datetime
import db
from Employee import Ems_form


from tasks import Task_form
from payroll import Payroll_Form
from tkinter import ttk, messagebox, Frame, PhotoImage


############################# Functions #############################
# Function to update digital clock
def update_clock():
    """Update the clock and date display."""
    current_time = time.strftime("%H:%M:%S")
    current_date = datetime.now().strftime("%A, %B %d, %Y")
    clock_label.configure(text=f"{current_time} | {current_date}")
    clock_label.after(1000, update_clock)


def logout():
    menu.destroy()
    import Login1
def attend():
    menu.destroy()
    import Attendence


########################## GUI Setup ##############################
# Main window setup
menu = CTk()
menu.title("Employee Management System")
app_w = 1280
app_h = 594
s_w = menu.winfo_screenwidth()
s_h = menu.winfo_screenheight()
x = (s_w / 2) - (app_w / 2)
y = (s_h / 2) - (app_h / 2)
menu.geometry(f'{app_w}x{app_h}+{int(x)}+{int(y)}')
menu.resizable(0, 0)

# Configure main grid layout
menu.grid_columnconfigure(0, weight=1)  # Ensure the layout takes full width
menu.grid_rowconfigure(0, weight=0)     # Header frame row
menu.grid_rowconfigure(1, weight=1)     # Main content area

# Header Frame with Digital Clock and Date
header_frame = CTkFrame(menu, fg_color='#088F8F', height=100)
header_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=(10, 5))

# Greeting Message
greeting_label = CTkLabel(header_frame, text="Welcome, Admin!", font=("Arial", 24, "bold"), text_color="White")
greeting_label.grid(row=0, column=0, padx=(20, 10), pady=20, sticky="w")

# Clock and Date Display
clock_label = CTkLabel(header_frame, font=("Arial", 20, "bold"), text_color="white")
clock_label.grid(row=0, column=1, padx=(10, 20), pady=20, sticky="e")
update_clock()

# Mainframe to hold Navigation Bar and Feature Frame
mainframe1 = CTkFrame(menu, fg_color="#1E7C72")  # Container frame
mainframe1.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

# Configure grid for `mainframe1`
mainframe1.grid_columnconfigure(0, weight=0)  # Fixed width for the navigation bar
mainframe1.grid_columnconfigure(1, weight=1)  # Feature frame takes remaining space
mainframe1.grid_rowconfigure(0, weight=1)     # Full height for both frames

# Left Frame for Navigation Bar
nav_bar_frame = CTkFrame(mainframe1, fg_color="#9FE2BF", width=150)
nav_bar_frame.grid(row=0, column=0, sticky="nsew", padx=(10, 5), pady=10)

global total_emp_count_label, total_attend_count_label, total_task_count_label, total_complete_count_label

# DshFrame with .place() to fill the window
DshFrame = CTkFrame(mainframe1, fg_color='#9FE2BF', height=550, width=1150)
DshFrame.grid(row=0,column=1,sticky='nsew', padx=(10, 5), pady=10)

# Header Frame with grid to adjust dynamically
header_frame = CTkFrame(DshFrame, fg_color='#088F8F')
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
EmpFrame.place(x=50, y=250, height=190, width=280)  # Adjust these values for desired position and size

total_emp_icon = PhotoImage(file='Emp.png')
total_emp_icon_label = CTkLabel(EmpFrame, text='', image=total_emp_icon)
total_emp_icon_label.image = total_emp_icon  # Keep a reference to the image
total_emp_icon_label.pack(pady=10)

total_emp_label = CTkLabel(EmpFrame, text='Total Employee', text_color='black', font=('arial', 18, 'bold'))
total_emp_label.pack()

emp_count=db.id_count()
total_emp_count_label = CTkLabel(EmpFrame, text=emp_count, text_color='black', font=('arial', 18, 'bold'))
total_emp_count_label.pack()

# Attendance Frame
attendFrame = Frame(DshFrame, bg='White', bd=3, relief=RIDGE)
attendFrame.place(x=400, y=135, height=190, width=280)  # Adjust these values for desired position and size

total_attend_icon = PhotoImage(file='attend.png')
total_attend_icon_label = CTkLabel(attendFrame, text='', image=total_attend_icon)
total_attend_icon_label.image = total_attend_icon  # Keep a reference to the image
total_attend_icon_label.pack(pady=10)

total_attend_label = CTkLabel(attendFrame, text='Total Attend Today', text_color='black',
                                  font=('arial', 18, 'bold'))
total_attend_label.pack()
att_count=db.Attend_count()
total_attend_count_label = CTkLabel(attendFrame, text=att_count, text_color='black', font=('arial', 18, 'bold'))
total_attend_count_label.pack()

# Task Frame
taskFrame = Frame(DshFrame, bg='White', bd=3, relief=RIDGE)
taskFrame.place(x=800, y=135, height=190, width=280)

total_task_icon = PhotoImage(file='task.png')
total_task_icon_label = CTkLabel(taskFrame, text='', image=total_task_icon)
total_task_icon_label.image = total_task_icon  # Keep a reference to the image
total_task_icon_label.pack(pady=10)

total_task_label = CTkLabel(taskFrame, text='Total Tasks Today', text_color='black', font=('arial', 18, 'bold'))
total_task_label.pack()
task_count=db.task_count()
total_task_count_label = CTkLabel(taskFrame, text=task_count, text_color='black', font=('arial', 18, 'bold'))
total_task_count_label.pack()

# Complete Frame
completeFrame = Frame(DshFrame, bg='White', bd=3, relief=RIDGE)
completeFrame.place(x=400, y=340, height=190, width=280)  # Adjust these values for desired position and size

total_complete_icon = PhotoImage(file='goal.png')
total_complete_icon_label = CTkLabel(completeFrame, text='', image=total_complete_icon)
total_complete_icon_label.image = total_complete_icon  # Keep a reference to the image
total_complete_icon_label.pack(pady=10)

total_complete_label = CTkLabel(completeFrame, text='Complete Tasks Today', text_color='black',
                                    font=('arial', 18, 'bold'))
total_complete_label.pack()
comp_count=db.complete_count()
total_complete_count_label = CTkLabel(completeFrame, text=comp_count, text_color='black', font=('arial', 18, 'bold'))
total_complete_count_label.pack()

DueFrame = Frame(DshFrame, bg='White', bd=3, relief=RIDGE)
DueFrame.place(x=800, y=340, height=190, width=280)  # Adjust these values for desired position and size

total_due_icon = PhotoImage(file='due.png')
total_due_icon_label = CTkLabel(DueFrame, text='',image=total_due_icon)
total_due_icon_label.image = total_due_icon  # Keep a reference to the image
total_due_icon_label.pack(pady=10)

total_due_label = CTkLabel(DueFrame, text='Due tasks', text_color='black', font=('arial', 18, 'bold'))
total_due_label.pack()

due_count=db.due_count()
total_due_count_label = CTkLabel(DueFrame, text=due_count, text_color='black', font=('arial', 18, 'bold'))
total_due_count_label.pack()


# Add navigation bar heading
heading_label = CTkLabel(nav_bar_frame, text='Menu', font=('Arial', 25, 'bold'), text_color='White')
heading_label.grid(row=0, column=0, pady=(10, 10))  # Adjusted padding for the heading label

# Add buttons to the navigation bar
menu_buttons = [
    CTkButton(nav_bar_frame, text="Employee", font=("Arial", 20), fg_color="#088F8F", height=60, command=lambda: Ems_form(mainframe1)),
    CTkButton(nav_bar_frame, text="Payroll", font=("Arial", 20), fg_color="#088F8F", height=60, command=lambda: Payroll_Form(mainframe1)),
    CTkButton(nav_bar_frame, text="Reports", font=("Arial", 20), fg_color="#088F8F", height=60, command=lambda: Task_form(mainframe1)),
    CTkButton(nav_bar_frame, text="Attendence", font=("Arial", 20), fg_color="#088F8F", height=60, command=attend),
    CTkButton(nav_bar_frame, text="Logout", font=("Arial", 20), fg_color="#088F8F", height=60, command=logout)

]

# Place buttons in the navigation frame using grid
for idx, btn in enumerate(menu_buttons, start=1):
    btn.grid(row=idx, column=0, padx=10, pady=(10, 10), sticky="ew")  # Reduced pady for smaller gaps



# Run the main loop
menu.mainloop()
