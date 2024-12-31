from customtkinter import *
from tkinter import ttk
import db
import datetime
from tkinter import messagebox
def select(event):
    selected = tree.selection()
    if selected:
        row = tree.item(selected)['values']
        clear()
        idEntry2.insert(0,row[0])
        task = db.fetch_today_task(row[0])
        Given_taskEntry2.insert("1.0", task[0])

def Task_form(window):
    # Main Frame for the entire window
    #taskFrame = CTkFrame(window, fg_color='#363C40')
    #taskFrame.grid(row=0, column=0, sticky="nsew")
    # Using place geometry manager for taskFrame
    taskFrame = CTkFrame(window, fg_color='#1E7C72')
    taskFrame.place(relx=0, rely=0, relwidth=1, relheight=1)  # Makes the frame fill the entire window

    # Configure row and column weights for resizing
    taskFrame.grid_rowconfigure(0, weight=0)  # Header does not expand
    taskFrame.grid_rowconfigure(1, weight=1)  # Content area expands
    taskFrame.grid_columnconfigure(0, weight=0)  # Left frame has fixed width
    taskFrame.grid_columnconfigure(1, weight=1)  # Right frame expands

    # Create the header frame (spans both columns)
    header_frame = CTkFrame(taskFrame, fg_color='#5F9EA0', height=100)
    header_frame.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=10, pady=(10, 5))

    # Back Button in header
    backbutton = CTkButton(header_frame, text='Back', font=('arial', 15, 'bold'), height=50, width=120,
                           corner_radius=15, fg_color="#FF6F61", command=lambda: taskFrame.place_forget())
    backbutton.grid(row=0, column=0, padx=2, pady=5, sticky="w")

    # Title Label in header
    normal_label = CTkLabel(header_frame, text="Task Allocation Of Employee's", font=("Arial", 24, "bold"), text_color="White")
    normal_label.grid(row=0, column=1, padx=(20, 10), pady=20, sticky="w")

    # Left Frame for specific input fields
    leftFrame = CTkFrame(taskFrame, fg_color='#9FE2BF', width=350)
    leftFrame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

    # Configure Left Frame to be resizable
    leftFrame.grid_rowconfigure(0, weight=1)
    leftFrame.grid_columnconfigure(0, weight=1)
    global idEntry,DeadlineEntry,Given_taskEntry
    # Fields in Left Frame
    idLabel = CTkLabel(leftFrame, text='ID', font=('arial', 18, 'bold'), text_color='Black')
    idLabel.grid(row=1, column=0, padx=20, pady=10, sticky='w')

    idEntry = CTkEntry(leftFrame, font=('arial', 15, 'bold'), width=200)
    idEntry.grid(row=1, column=1, padx=20, pady=5)

    DeadlineLabel = CTkLabel(leftFrame, text='Deadline', font=('arial', 18, 'bold'), text_color='Black')
    DeadlineLabel.grid(row=2, column=0, padx=20, pady=10, sticky='w')

    DeadlineEntry = CTkEntry(leftFrame, font=('arial', 15, 'bold'), width=200)
    DeadlineEntry.grid(row=2, column=1, padx=20, pady=5)

    Given_taskLabel = CTkLabel(leftFrame, text='Given Task', font=('arial', 18, 'bold'), text_color='Black')
    Given_taskLabel.grid(row=3, column=0, padx=20, pady=10, sticky='w')

    Given_taskEntry = CTkTextbox(leftFrame, font=('arial', 15, 'bold'), width=200, height=150)
    Given_taskEntry.grid(row=3, column=1, padx=20, pady=5)

    assignButton = CTkButton(leftFrame, text='Assign', font=('arial', 15, 'bold'),fg_color="#088F8F", height=40, width=160, corner_radius=15,
                             command=add_task)
    assignButton.grid(row=4, column=1, padx=20, pady=15)

    # Right Frame for Treeview and additional controls
    rightFrame = CTkFrame(taskFrame, fg_color='#9FE2BF')
    rightFrame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

    # Configure Right Frame to be resizable
    rightFrame.grid_rowconfigure(0, weight=1)
    rightFrame.grid_columnconfigure(0, weight=1)

    # Treeview with Scrollbar
    global tree
    tree = ttk.Treeview(rightFrame, height=10)
    tree.grid(row=0, column=0, sticky="nsew", padx=10, pady=5)

    scroll = ttk.Scrollbar(rightFrame, orient=VERTICAL, command=tree.yview)
    scroll.grid(row=0, column=1, sticky="ns")
    tree.configure(yscrollcommand=scroll.set)

    tree['columns'] = ('ID', 'Role',  'Deadline', 'Within_Deadline', 'Rate', 'Complete')
    tree.heading('ID', text='ID')
    tree.heading('Role', text='Role')
    tree.heading('Deadline', text='Deadline')
    tree.heading('Within_Deadline', text='Within Deadline')
    tree.heading('Rate', text='Rate')
    tree.heading('Complete', text='Complete')

    tree.column('ID', width=50)
    tree.column('Role', width=100)
    tree.column('Deadline', width=100)
    tree.column('Within_Deadline', width=120)
    tree.column('Rate', width=70)
    tree.column('Complete', width=70)
    tree['show'] = 'headings'

    style = ttk.Style()
    style.configure('Treeview.Heading', font=('arial', 18, 'bold'))
    style.configure('Treeview', font=('arial', 13, 'bold'), rowheight=30, background='#363C40', foreground='#F2F2F2')

    # Lower Frame for additional controls
    lowerFrame = CTkFrame(rightFrame, fg_color='#21A698', height=200)
    lowerFrame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

    # ID, Within Deadline, and Rate Section
    global idEntry2,withinDeadlineBox,rateBox,Given_taskEntry2

    idLabel = CTkLabel(lowerFrame, text='ID', font=('arial', 14, 'bold'), text_color='white')
    idLabel.grid(row=0, column=0, padx=10, pady=5, sticky='w')

    idEntry2 = CTkEntry(lowerFrame, font=('arial', 13), width=150)
    idEntry2.grid(row=0, column=1, padx=10, pady=5)

    withinDeadlineLabel = CTkLabel(lowerFrame, text='Within Deadline', font=('arial', 14, 'bold'), text_color='white')
    withinDeadlineLabel.grid(row=1, column=0, padx=10, pady=5, sticky='w')

    withinDeadlineBox = CTkComboBox(lowerFrame, values=['Yes', 'No'], width=150, font=('arial', 13), state='readonly')
    withinDeadlineBox.grid(row=1, column=1, padx=10, pady=5)
    withinDeadlineBox.set('Select Here')

    rateLabel = CTkLabel(lowerFrame, text='Rate', font=('arial', 14, 'bold'), text_color='white')
    rateLabel.grid(row=2, column=0, padx=10, pady=5, sticky='w')

    rateBox = CTkComboBox(lowerFrame, values=['*', '**', '***', '****', '*****'], width=150, font=('arial', 13), state='readonly')
    rateBox.grid(row=2, column=1, padx=10, pady=5)
    rateBox.set('Select Here')

    # Given Task and Complete Section
    Given_taskLabel = CTkLabel(lowerFrame, text='Given Task', font=('arial', 14, 'bold'), text_color='white')
    Given_taskLabel.grid(row=0, column=2, padx=10, pady=5, sticky='w')

    Given_taskEntry2 = CTkTextbox(lowerFrame, font=('arial', 13), width=200, height=80)
    Given_taskEntry2.grid(row=0, column=3, rowspan=3, padx=10, pady=5)

    CompleteButton = CTkButton(lowerFrame, text='Complete', font=('arial', 13, 'bold'), height=40, width=120, corner_radius=15,command=comp_up)
    CompleteButton.grid(row=0, column=4, padx=10, pady=15)

    tree.bind('<ButtonRelease>', select)

    info = db.fetch_task_data()
    tree_view(info)
    deadline_insert()

def tree_view(info):
    tree.delete(*tree.get_children())
    for data in info:
        tree.insert('',END,values=data)
# def add_task():
#     id=idEntry.get()
#     assign = db.check_comp(id)
#     if assign == "Yes":
#         deadline = DeadlineEntry.get()
#         task = Given_taskEntry.get("1.0", "end-1c")
#         db.update_task(id, deadline, task)
#         info = db.fetch_task_data()
#         tree_view(info)
#         clear_assign()
#     else:
#         messagebox.showerror("Error", "Previous task is incomplete.")

def add_task():
    """
    Adds or updates a task for an employee if eligible.
    """
    id = idEntry.get()
    assign_status = db.check_comp(id)

    if assign_status == "No":
        messagebox.showerror("Error", "Previous task is incomplete.")
        return

    deadline = DeadlineEntry.get()
    task = Given_taskEntry.get("1.0", "end-1c")

    if not deadline.strip() or not task.strip():
        messagebox.showerror("Error", "Task and deadline cannot be empty.")
        return

    try:
        # Update task in the database
        db.update_task(id, deadline, task)

        # Refresh the Treeview with updated data
        info = db.fetch_task_data()
        if info:  # Ensure data is not empty
            tree_view(info)
        else:
            messagebox.showwarning("No Data", "No task data found after update.")

        # Clear input fields
        clear_assign()

        messagebox.showinfo("Success", "Task successfully assigned!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


def tree_view(info):
    """
    Clears and updates the Treeview with fresh data.
    """
    try:
        tree.delete(*tree.get_children())  # Clear all rows
        for data in info:
            tree.insert('', 'end', values=data)  # Add new data to the Treeview
    except Exception as e:
        messagebox.showerror("Error", f"Failed to update Treeview: {e}")

def clear_assign():
    idEntry.delete(0,END)
    DeadlineEntry.delete(0,END)
    Given_taskEntry.delete("1.0",END)
    deadline_insert()


def clear():
    idEntry2.delete(0, END)
    Given_taskEntry2.delete("1.0", END)
    withinDeadlineBox.set('Select Here')
    rateBox.set('Select Here')
def comp_up():

    id=idEntry2.get()
    w_d_line=withinDeadlineBox.get()
    rBox=rateBox.get()
    db.complete(id,w_d_line,rBox)
    info = db.fetch_task_data()
    tree_view(info)
    clear()

def deadline_insert():
    current_date = datetime.date.today()
    DeadlineEntry.insert(0,current_date)

def main():
    root = CTk()
    root.title("Task Management System")
    root.geometry("1200x594")

    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    Task_form(root)
    root.mainloop()

if __name__ == "__main__":
    main()
