from customtkinter import *
from tkinter import ttk, messagebox
import pymysql as sql
import datetime


# Database Connection
def connect_db():
    try:
        conn = sql.connect(host="localhost", user="root", password="", database="employee_data")
        return conn
    except sql.MySQLError as e:
        messagebox.showerror("Database Error", f"Error connecting to database: {e}")
        return None


# Fetch payroll details for a specific month and year
def fetch_payroll_by_month_year(month, year):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.Payment_Year, p.Payment_Month, d.ID, d.Salary, IFNULL(p.Paid, 'No')
            FROM data d
            LEFT JOIN payroll p ON d.ID = p.ID AND p.Payment_Month = %s AND p.Payment_Year = %s
        """, (month, year))
        payroll_data = cursor.fetchall()
        conn.close()
        return payroll_data
    return []


# Fetch payroll details for the current month and year
def fetch_current_month_payroll():
    current_date = datetime.date.today()
    current_month = current_date.strftime("%B")
    current_year = current_date.year
    return fetch_payroll_by_month_year(current_month, current_year)

def fetch_payroll_by_id(emp_id):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.Payment_Year, p.Payment_Month, d.ID, d.Salary, IFNULL(p.Paid, 'No')
            FROM payroll p
            LEFT JOIN data d ON d.ID = p.ID
            WHERE p.ID = %s
        """, (emp_id,))
        payroll_data = cursor.fetchall()
        conn.close()
        return payroll_data
    return []

# Fetch employee details by ID
def fetch_employee_by_id(emp_id):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT ID, Salary FROM data WHERE ID = %s", (emp_id,))
        data = cursor.fetchone()
        conn.close()
        return data


# Pay salary for the current month
# def pay_salary(emp_id, salary):
#     current_date = datetime.date.today()
#     current_month = current_date.strftime("%B")
#     current_year = current_date.year
#
#     conn = connect_db()
#     if conn:
#         cursor = conn.cursor()
#         try:
#             cursor.execute("""
#                 INSERT INTO payroll (ID, Salary, Payment_Month, Payment_Year, Paid)
#                 VALUES (%s, %s, %s, %s, 'Yes')
#                 ON DUPLICATE KEY UPDATE Paid = 'Yes'
#             """, (emp_id, salary, current_month, current_year))
#             conn.commit()
#             messagebox.showinfo("Success", f"Salary paid for {current_month}, {current_year}")
#         except sql.MySQLError as e:
#             messagebox.showerror("Error", f"Failed to pay salary: {e}")
#         finally:
#             conn.close()


# GUI Function for Payroll Form
def Payroll_Form(window):
    def clear():
        id_entry.delete(0, END)
        salary_entry.delete(0, END)
        search_entry.delete(0, END)

    def select(event):
        search_entry.delete(0, END)
        selected = tree.selection()
        if selected:
            row = tree.item(selected)['values']
            clear()
            id_entry.insert(0, row[2])
            salary_entry.insert(0, row[3])

    def refresh_treeview(data=None):
        if data is None:
            data = fetch_current_month_payroll()

        tree.delete(*tree.get_children())
        for record in data:
            tree.insert('', 'end', values=record)
    def clear1():
        id_entry.delete(0, END)
        month_combobox.set('Select Month')
        year_entry.delete(0, END)

    def search_employee():
        emp_id = search_entry.get()
        if not emp_id:
            messagebox.showerror("Error", "Enter Employee ID to search.")
            return

        emp_data = fetch_employee_by_id(emp_id)
        if emp_data:
            id_entry.delete(0, END)
            salary_entry.delete(0, END)
            id_entry.insert(0, emp_data[0])
            salary_entry.insert(0, emp_data[1])
        else:
            messagebox.showerror("Error", "Employee not found.")

    def search_by_month_year():
        emp_id = id_entry_search.get().strip()
        selected_month = month_combobox.get()
        year = year_entry.get().strip()

        if emp_id:
            payroll_data = fetch_payroll_by_id(emp_id)

        else:
            if selected_month == "Select Month" or not year:
                messagebox.showerror("Error", "Select a valid month and enter a year.")
                return
            payroll_data = fetch_payroll_by_month_year(selected_month, year)

        if payroll_data:
            refresh_treeview(payroll_data)
        else:
            tree.delete(*tree.get_children())
            messagebox.showinfo("No Data", f"No payroll records found for {selected_month}, {year}.")
        clear1()
    def pay():
        emp_id = id_entry.get()
        salary = salary_entry.get()

        if not emp_id or not salary:
            messagebox.showerror("Error", "Complete the details before paying.")
            return

        # Get current month and year
        current_date = datetime.date.today()
        current_month = current_date.strftime("%B")
        current_year = current_date.year

        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            try:
                # Check if payment is already made for the current month and year
                cursor.execute("""
                    SELECT COUNT(*) 
                    FROM payroll 
                    WHERE ID = %s AND Payment_Month = %s AND Payment_Year = %s AND Paid = 'Yes';
                """, (emp_id, current_month, current_year))
                result = cursor.fetchone()

                if result[0] > 0:  # Payment already exists
                    messagebox.showinfo("Info", f"Payment for {current_month}, {current_year} has already been made.")
                    clear()
                else:
                    # Proceed to pay salary
                    cursor.execute("""
                        INSERT INTO payroll (ID, Salary, Payment_Month, Payment_Year, Paid)
                        VALUES (%s, %s, %s, %s, 'Yes')
                        ON DUPLICATE KEY UPDATE Paid = 'Yes';
                    """, (emp_id, salary, current_month, current_year))
                    conn.commit()
                    messagebox.showinfo("Success", f"Salary paid for {current_month}, {current_year}")

                    refresh_treeview()

            except sql.MySQLError as e:
                messagebox.showerror("Error", f"Failed to pay salary: {e}")
            finally:
                conn.close()

    def go_back():
        payrollFrame.place_forget()

    # Main Frame
    payrollFrame = CTkFrame(window, fg_color='#9FE2BF')
    payrollFrame.place(relx=0, rely=0, relwidth=1, relheight=1)

    # Header Frame
    header_frame = CTkFrame(payrollFrame, fg_color='#5F9EA0', height=80)
    header_frame.pack(fill=X, padx=10, pady=(10, 5))

    back_button = CTkButton(header_frame, text="Back", font=("Arial", 16), fg_color="#FF6F61", height=50, width=120,
                            command=go_back)
    back_button.pack(side=LEFT, padx=10, pady=10)

    header_label = CTkLabel(header_frame, text="Pay Salary of Employees", font=("Arial", 24, "bold"),
                            text_color="white")
    header_label.pack(side=LEFT, padx=(20, 10), pady=10)

    # Treeview Frame
    tree_frame = CTkFrame(payrollFrame, fg_color="#363C40")
    tree_frame.pack(fill=BOTH, expand=True, padx=10, pady=5)

    tree = ttk.Treeview(tree_frame, columns=("Year", "Month", "ID", "Salary", "Paid"), show='headings')
    tree.heading("Year", text="Year")
    tree.heading("Month", text="Month")
    tree.heading("ID", text="ID")
    tree.heading("Salary", text="Salary")
    tree.heading("Paid", text="Paid")

    tree.column("Year", anchor="center", width=100)
    tree.column("Month", anchor="center", width=100)
    tree.column("ID", anchor="center", width=100)
    tree.column("Salary", anchor="center", width=100)
    tree.column("Paid", anchor="center", width=100)

    style = ttk.Style()
    style.configure('Treeview.Heading', font=('arial', 18, 'bold'))
    style.configure('Treeview', font=('arial', 13, 'bold'), rowheight=20, background='#363C40', foreground='#F2F2F2')
    tree.pack(fill=BOTH, expand=True)
    refresh_treeview()

    # Control Panel
    control_frame = CTkFrame(payrollFrame, fg_color="#088F8F")
    control_frame.pack(fill=X, padx=10, pady=10)

    # Employee Search Section
    employee_search_frame = CTkFrame(control_frame, fg_color="#088F8F")
    employee_search_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    Emp_search = CTkLabel(employee_search_frame, text="Search ID To Pay", font=("Arial", 16, "bold"),
                          text_color="white")
    Emp_search.grid(row=0, column=0, columnspan=2, pady=(0, 10))
    Id = CTkLabel(employee_search_frame, text="Search ID:", text_color="white")
    Id.grid(row=1, column=0, padx=10, pady=5)
    search_entry = CTkEntry(employee_search_frame, width=150)
    search_entry.grid(row=1, column=1, padx=10, pady=5)
    serch_button=CTkButton(employee_search_frame, text="Search", command=search_employee)
    serch_button.grid(row=1, column=2, padx=10, pady=5)

    id_label=CTkLabel(employee_search_frame, text="ID:", text_color="white")
    id_label.grid(row=2, column=0, padx=10, pady=5)
    id_entry = CTkEntry(employee_search_frame, width=150)
    id_entry.grid(row=2, column=1, padx=10, pady=5)

    salary_label=CTkLabel(employee_search_frame, text="Salary:", text_color="white")
    salary_label.grid(row=3, column=0, padx=10, pady=5)
    salary_entry = CTkEntry(employee_search_frame, width=150)
    salary_entry.grid(row=3, column=1, padx=10, pady=5)
    pay_button=CTkButton(employee_search_frame, text="Pay", command=pay)
    pay_button.grid(row=3, column=2, padx=10, pady=5)

    # Search Section
    search_frame = CTkFrame(control_frame, fg_color="#088F8F")
    search_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

    Search = CTkLabel(search_frame, text="Search Payroll Data", font=("Arial", 16, "bold"), text_color="white")
    Search.grid(row=0, column=0, columnspan=3, pady=(0, 10))

    # ID label and entry
    CTkLabel(search_frame, text="Employee ID:", text_color="white").grid(row=1, column=0, padx=10, pady=5)
    id_entry_search = CTkEntry(search_frame, width=150)
    id_entry_search.grid(row=1, column=1, padx=10, pady=5)

    # Month label and combobox
    month = CTkLabel(search_frame, text="Month:", text_color="white")
    month.grid(row=2, column=0, padx=10, pady=5)
    month_combobox = CTkComboBox(search_frame, values=["January", "February", "March", "April", "May", "June",
                                                       "July", "August", "September", "October", "November",
                                                       "December"],
                                 width=150, state="readonly")
    month_combobox.grid(row=2, column=1, padx=10, pady=5)
    month_combobox.set("Select Month")

    # Year label and entry
    CTkLabel(search_frame, text="Year:", text_color="white").grid(row=3, column=0, padx=10, pady=5)
    year_entry = CTkEntry(search_frame, width=150)
    year_entry.grid(row=3, column=1, padx=10, pady=5)

    # Search button
    search_r = CTkButton(search_frame, text="Search", command=search_by_month_year, height=30, width=120,
                         corner_radius=15)
    search_r.grid(row=2, column=2, columnspan=3, pady=15)

    tree.bind('<ButtonRelease>', select)


# Main Application Window
def main():
    root = CTk()
    root.title("Task Management System")
    root.geometry("1200x700")
    Payroll_Form(root)
    root.mainloop()


if __name__ == "__main__":
    main()
