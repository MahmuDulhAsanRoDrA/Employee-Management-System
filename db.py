import pymysql as sql
from tkinter import messagebox
import datetime
def connect_db():
     global MYCUR
     global conn
     try :
          conn = sql.connect(host="localhost",user="root",password="")
          MYCUR =conn.cursor()
     except:
          messagebox.showerror('Error',"something went wrong!!!!")
          return
     #MYCUR.execute('CREATE DATABASE if not exist employee_data')
     MYCUR.execute('USE employee_data')
     #MYCUR.execute('CREATE TABLE if not exist data(ID varchar(50),Name varchar(50),Role varchar(50),Phone varchar(50),Gender varchar(50), Salary varchar(50))')
def insert(id,name,role,phone,gender,salary,email):
     MYCUR.execute('INSERT INTO data VALUES (%s,%s,%s,%s,%s,%s,%s)',(id,name,role,phone,gender,salary,email))
     conn.commit()
def id_exist(id):
     MYCUR.execute('select count(*) from data where id = %s', id)
     result=MYCUR.fetchone()
     return result[0]>0
def phone_exist(phone):
    MYCUR.execute('select count(*) from data where phone = %s', phone)
    result = MYCUR.fetchone()
    return result[0] > 0
def email_exist(email):
     MYCUR.execute('select count(*) from data where email = %s', email)
     result=MYCUR.fetchone()
     return result[0]>0
def fetch_employees():
     MYCUR.execute('select * from data')
     result=MYCUR.fetchall()
     return result
def update(id,new_name,new_phone,new_role,new_gender,new_salary,new_email):
     MYCUR.execute('update data set name=%s,phone=%s,role=%s,gender=%s,salary=%s,email=%s where id=%s',(new_name,new_phone,new_role,new_gender,new_salary,new_email,id))
     conn.commit()
def delete(id):
     MYCUR.execute('delete from data where id = %s',(id))
     conn.commit()
def search(role,value):
     MYCUR.execute(f'select * from data where {role}=%s',(value))
     result = MYCUR.fetchall()
     return result


def delete_all():
     MYCUR.execute('delete from data')
     conn.commit()
def fetch_ID():
     MYCUR.execute('select Id from data;')
     result=MYCUR.fetchall()
     return result
def get_employee_by_id(id):
     MYCUR.execute('select Id from data where ID=%s;',(id))
     result = MYCUR.fetchall()
     return result
def fetch_id():
    """Fetches all employee IDs from the data table."""
    try:
        MYCUR.execute("SELECT ID FROM data")
        ids = MYCUR.fetchall()
        return [id[0] for id in ids]
    except sql.MySQLError as e:
        messagebox.showerror("Error", f"Error fetching IDs: {str(e)}")
        return []
def mark_present(employee_id):
    """Marks an employee as present by updating attendance_table."""
    try:
        current_date = datetime.date.today()
        current_time = datetime.datetime.now().strftime("%H:%M:%S")

        # Insert or update attendance for the given date and employee_id
        MYCUR.execute(
            """
            INSERT INTO attendance_table (Date, employee_Id, present_status, present_time)
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                present_status = VALUES(present_status),
                present_time = VALUES(present_time)
            """,
            (current_date, employee_id, 'Present', current_time)
        )
        conn.commit()
        return current_date, current_time
    except sql.MySQLError as e:
        messagebox.showerror("Error", f"Error marking present: {str(e)}")
        return None, None
def mark_leave(employee_id):
    """Marks an employee as present by updating attendance_table."""
    try:
        current_date = datetime.date.today()
        current_time = datetime.datetime.now().strftime("%H:%M:%S")

        # Insert or update attendance for the given date and employee_id
        MYCUR.execute(
            """
            INSERT INTO attendance_table (Date, employee_Id, leave_status, leave_time)
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                leave_status = VALUES(leave_status),
                leave_time = VALUES(leave_time)
            """,
            (current_date, employee_id, 'left', current_time)
        )
        conn.commit()
        return current_date, current_time
    except sql.MySQLError as e:
        messagebox.showerror("Error", f"Error marking leave: {str(e)}")
        return None, None
def update_info():

    current_date = datetime.date.today()
    employeeId=fetch_ID()
    # Insert or update attendance for the given date and employee_id
    for employee_id in employeeId:
        MYCUR.execute(
            """
            INSERT INTO attendance_table (Date, employee_Id)
            VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE
                present_status = VALUES(present_status),
                present_time = VALUES(present_time)
            """,
            (current_date, employee_id)
        )
        conn.commit()
def p_check(ID):
    current_date = str(datetime.date.today())
    MYCUR.execute(f"Select present_status from attendance_table where employee_id =%s  and Date =%s",(ID,current_date))
    result = MYCUR.fetchone()
    print(f"{result} {current_date} {ID}")
    if result[0] == "Present":
        return 1
    else:
        return 0
def p_T(ID):
    current_date = datetime.date.today()
    MYCUR.execute(f"Select present_time from attendance_table where employee_id = %s and Date = %s",(ID,current_date))
    result = MYCUR.fetchone()
    if result and isinstance(result[0], datetime.timedelta):
        total_seconds = int(result[0].total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        formatted_time = f"{hours:02}:{minutes:02}:{seconds:02}"
        print(formatted_time)
        return formatted_time
def l_T(ID):
    current_date = datetime.date.today()
    MYCUR.execute(f"Select leave_time from attendance_table where employee_id = %s and Date = %s",(ID,current_date))
    result = MYCUR.fetchone()
    if result and isinstance(result[0], datetime.timedelta):
        total_seconds = int(result[0].total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        formatted_time = f"{hours:02}:{minutes:02}:{seconds:02}"
        print(formatted_time)
        return formatted_time
def stat(ID):
    current_date = datetime.date.today()
    MYCUR.execute(f"Select present_status from attendance_table where employee_id = %s and Date = %s", (ID, current_date))
    result = MYCUR.fetchone()
    print(result)
    return  result[0]



def fetch_role(ID):
    """
    Fetches the role for a given employee ID from the `data` table.

    Args:
    ID (str): Employee ID.

    Returns:
    str: Role of the employee.
    """
    try:
        MYCUR.execute("SELECT Role FROM data WHERE ID = %s", (ID,))
        role = MYCUR.fetchone()  # Fetch a single record
        return role[0] if role else None  # Return the role if found, otherwise None
    except sql.MySQLError as e:
        messagebox.showerror("Error", f"Error fetching role: {str(e)}")
        return None
def update_task(id, deadline, task):
    """
    Updates the task for a given employee. Inserts or updates the task table.

    Args:
    id (str): Employee ID.
    deadline (str): Task deadline in YYYY-MM-DD format.
    task (str): Description of the task.
    """
    try:
        current_date = datetime.date.today()
        role = fetch_role(id)

        if not role:
            messagebox.showerror("Error", "ID not found.")
            return

        # Insert or update task
        MYCUR.execute(
            """
            INSERT INTO task (Emp_ID, Role, Assign_date, Given_task, deadline,Within_deadline,rate,complete)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                Given_task = VALUES(Given_task),
                deadline = VALUES(deadline)
            """,
            (id, role, current_date, task, deadline,"No","","No")
        )
        conn.commit()
        print("Task updated successfully.")
    except sql.MySQLError as e:
        messagebox.showerror("Error", f"Error updating task: {str(e)}")
def fetch_task_data():
    current_date = datetime.date.today()
    MYCUR.execute("Select Emp_ID, Role, Deadline,Within_Deadline,Rate,complete from task where Assign_date = %s",(current_date,))
    info = MYCUR.fetchall()
    return info
def fetch_today_task(emp_id):
    """
    Fetches a task assigned to the specified employee for the current day.

    Args:
    emp_id (str): The Employee ID for which to fetch the task.

    Returns:
    tuple: A tuple containing the task details, or None if no task is found.
    """
    try:
        current_date = datetime.date.today()

        # Query to fetch one task for the current day
        MYCUR.execute(
            """
            SELECT Given_task FROM task
            WHERE Emp_ID = %s AND Assign_date = %s
            LIMIT 1
            """,
            (emp_id, current_date)
        )
        task = MYCUR.fetchone()
        return task
    except sql.MySQLError as e:
        messagebox.showerror("Error", f"Error fetching today's task: {str(e)}")
        return None
def complete(id,withindeadline,ratebox):
    # withindeadline = "Yes" or "NO" and ratebox = from * to *****
    current_date = datetime.date.today()
    MYCUR.execute(
        """
        UPDATE task
        SET Within_deadline = %s, rate = %s, complete = %s
        WHERE Emp_ID = %s AND Assign_date = %s
        """,
        (withindeadline, ratebox, "YES", id, current_date)
    )
    conn.commit()
# def check_comp(id):
#     current_date = datetime.date.today()
#     MYCUR.execute("select complete from task where EMP_ID=%s and Assign_date = %s",(id,current_date))
#     result = MYCUR.fetchone()
#     print(result[0])
#     messagebox.showerror("Error", "Previous task is incomplete.")
#     return result[0]
def check_comp(id):
    """
    Checks if the previous task is complete for the given employee ID.

    Args:
        id (str): Employee ID.

    Returns:
        str: "Yes" if the task is complete, "No" if incomplete, or None if no task exists for today.
    """
    try:
        current_date = datetime.date.today()
        MYCUR.execute(
            "SELECT complete FROM task WHERE Emp_ID = %s AND Assign_date = %s",
            (id, current_date)
        )
        result = MYCUR.fetchone()

        if result is None:
            # No task exists for today
            return None

        # Return the completion status: "Yes" or "No"
        return result[0]
    except sql.MySQLError as e:
        messagebox.showerror("Error", f"Database error: {str(e)}")
        return None
def id_count():
    MYCUR.execute('select count(ID) from data;')
    result = MYCUR.fetchone()
    return result
def Attend_count():
    current_date = datetime.date.today()
    MYCUR.execute('''
        SELECT COUNT(employee_Id)
        FROM attendance_table
        WHERE date = %s AND present_status = %s;
        ''',(current_date, "present"))
    result = MYCUR.fetchone()
    return result
def task_count():
    MYCUR.execute('select count(Given_task) from task;')
    result = MYCUR.fetchone()
    return result
def complete_count():
    """
    Returns the count of completed tasks from the task table.
    """
    MYCUR.execute("SELECT COUNT(Given_task) FROM task WHERE Complete = %s;", ('Yes'))
    result = MYCUR.fetchone()

    return result[0] if result else 0  # Handle possible None result

def due_count():
    """
    Returns the count of completed tasks from the task table.
    """
    MYCUR.execute("SELECT COUNT(Given_task) FROM task WHERE Complete = %s;", ('No'))
    result = MYCUR.fetchone()

    return result[0] if result else 0  # Handle possible None result




connect_db()