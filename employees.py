from tkinter import *
from tkinter import ttk ,messagebox 
from tkcalendar import DateEntry
from datetime import date,datetime 
import pyodbc 

def connect_db():
    try:
        # Connect to master to check if database exists
        con = pyodbc.connect(
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=DESKTOP-RL7IVN4;"
            "DATABASE=master;"
            "Trusted_Connection=yes;"
        )
        con.autocommit = True  # Disable transaction mode to allow CREATE DATABASE
        cur = con.cursor()
        
        # Check if the database exists and create it if not
        cur.execute("IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'alfazal_traders') CREATE DATABASE alfazal_traders")
        con.close()  # Close the first connection

        # Now connect directly to alfazal_traders
        con = pyodbc.connect(
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=DESKTOP-RL7IVN4;"
            "DATABASE=alfazal_traders;"
            "Trusted_Connection=yes;"
        )
        cur = con.cursor()

        # Create table if it does not exist
        cur.execute('''
            IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'EMPLOYEES')
            CREATE TABLE EMPLOYEES (
                EMP_ID INT PRIMARY KEY NOT NULL,
                EMP_NAME VARCHAR(50) NOT NULL,
                EMP_EMAIL VARCHAR(50) NOT NULL,
                EMP_DOB DATE NOT NULL,
                EMP_CONTACT VARCHAR(15) NOT NULL,
                EMP_EDUCATION VARCHAR(20) NOT NULL,
                EMP_DOJ DATE NOT NULL,
                EMP_ADDRESS VARCHAR(100) NOT NULL,
                EMP_SALARY INT NOT NULL,
                EMP_USERTYPE VARCHAR(20) NOT NULL,
                EMP_PASSWORD VARCHAR(20) NOT NULL
            ) 
        ''') 
        con.commit()
        
        return con , cur 
    
    except Exception as e:
        messagebox.showerror("Error: Database Connection Error. Try Again", str(e)) 


def treeview_data():
    con, cur = connect_db()
    if not con or not cur:
        return

    # Clear existing data in Treeview
    for row in employee_tree_view.get_children():
        employee_tree_view.delete(row)

    cur.execute("SELECT * FROM EMPLOYEES")
    rows = cur.fetchall()

    for row in rows:
        employee_tree_view.insert("", END, values=list(row))  # Unpacking the tuple

    con.close()
def add_employee(empid, name, email, dob, contact, education, doj, address, salary, usertype, password):
    if not all([empid, name, email, dob, contact, education, doj, address, salary, usertype, password]): 
        messagebox.showerror("Error", "All fields are required.")
        return 
    elif education == "Select Education":
        messagebox.showerror("Error","Please select a valid Education.")
        return 
    elif usertype == "Select User Type":
        messagebox.showerror("Error","Please select a valid User Type.")
        return  
    elif len(contact)>11 or len(contact)<11: 
        messagebox.showerror("Error","Please enter a valid contact number of 11 digits.") 
        return  
    elif len(password)>20 or len(password)<8:
        messagebox.showerror("Error","Please enter a valid password of 8-20 characters.")
        return    

    try:
        con, cur = connect_db()
        empid, salary = int(empid), int(salary)  # Convert to integer

        # Convert date format to YYYY-MM-DD
        dob = datetime.strptime(dob, "%d/%m/%Y").strftime("%Y-%m-%d")
        doj = datetime.strptime(doj, "%d/%m/%Y").strftime("%Y-%m-%d")

        cur.execute("INSERT INTO EMPLOYEES VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                    empid, name, email, dob, contact, education, doj, address, salary, usertype, password)

        con.commit()
        treeview_data() 
        messagebox.showinfo("Success", "Employee added successfully.")  
        con.close()
        
    except ValueError:
        messagebox.showerror("Error", "Employee ID and Salary must be numbers.")
    except pyodbc.IntegrityError:
        messagebox.showerror("Error", "Employee ID already exists. Choose a unique ID.")
    except Exception as e:
        messagebox.showerror("Error", str(e))
def clear_fields(empid_entry, name_entry, email_entry, dob_entry, contact_entry, education_combobox,doj_entry, address_entry, salary_entry, usertype_combobox, password_entry,check): 
    empid_entry.delete(0, END)
    name_entry.delete(0, END)
    email_entry.delete(0, END)
    dob_entry.set_date(date.today())
    contact_entry.delete(0, END)
    education_combobox.set("Select Education")
    doj_entry.set_date(date.today())
    address_entry.delete("1.0", END) 
    salary_entry.delete(0, END)
    usertype_combobox.set("Select User Type")
    password_entry.delete(0, END) 
    if check: 
        employee_tree_view.selection_remove(employee_tree_view.selection()) 
def select_data(event, empid_entry, name_entry, email_entry, dob_entry, contact_entry, 
                education_combobox, doj_entry, address_entry, salary_entry, 
                usertype_combobox, password_entry):

    index = employee_tree_view.selection()

    if not index:  # Check if selection is empty
        messagebox.showerror("Error","No row selected")
        return

    content = employee_tree_view.item(index)
    data = content["values"]

    if not data:  # Ensure data is not empty
        messagebox.showerror("Error","No data present")
        return

    clear_fields(empid_entry, name_entry, email_entry, dob_entry, contact_entry, 
                 education_combobox, doj_entry, address_entry, salary_entry, 
                 usertype_combobox, password_entry, False)  # No need to remove selection 

    empid_entry.insert(0, data[0])
    name_entry.insert(0, data[1])
    email_entry.insert(0, data[2])

    # Convert date only if data exists
    if data[3]:
        dob_entry.set_date(datetime.strptime(data[3], "%Y-%m-%d").date())  

    contact_value = str(data[4]).zfill(11) if data[4] else ""
    contact_entry.insert(0, contact_value)  

    education_combobox.set(data[5]) 

    if data[6]:
        doj_entry.set_date(datetime.strptime(data[6], "%Y-%m-%d").date())

    address_entry.insert("1.0", data[7])
    salary_entry.insert(0, data[8])
    usertype_combobox.set(data[9])
    password_entry.insert(0, data[10])

def normalize_text(text):
    """Remove excessive spaces and newlines from text fields like address"""
    return ' '.join(text.split()).strip() 

def update_employee(empid, name, email, dob, contact, education, doj, address, salary, usertype, password):
    selected = employee_tree_view.selection()
    
    if not selected:
        messagebox.showerror("Error", "No row selected")
        return  
    elif not all([empid, name, email, dob, contact, education, doj, address, salary, usertype, password]): 
        messagebox.showerror("Error", "All fields are required.")
        return 
    elif education == "Select Education":
        messagebox.showerror("Error", "Please select a valid Education.")
        return 
    elif usertype == "Select User Type":
        messagebox.showerror("Error", "Please select a valid User Type.")
        return 
    elif len(contact) != 11:
        messagebox.showerror("Error", "Please enter a valid contact number of 11 digits.")
        return 
    elif len(password) < 8 or len(password) > 20:
        messagebox.showerror("Error", "Please enter a valid password of 8-20 characters.")
        return    

    try:
        con, cur = connect_db()
        if not con or not cur:
            messagebox.showerror("Error", "Failed to connect to database")
            return 

        # Convert input date formats
        dob = datetime.strptime(dob, "%d/%m/%Y").strftime("%Y-%m-%d")
        doj = datetime.strptime(doj, "%d/%m/%Y").strftime("%Y-%m-%d")

        # Normalize input address
        address = normalize_text(address)

        # Convert salary to string for uniform comparison
        salary = str(salary)

        # Fetch the current data from the database
        cur.execute("SELECT EMP_NAME, EMP_EMAIL, EMP_DOB, EMP_CONTACT, EMP_EDUCATION, EMP_DOJ, EMP_ADDRESS, EMP_SALARY, EMP_USERTYPE, EMP_PASSWORD FROM EMPLOYEES WHERE EMP_ID = ?", (empid,))
        existing_data = cur.fetchone()

        # Normalize fetched data for proper comparison
        if existing_data:
            existing_data = (
                existing_data[0],  # Name (string)
                existing_data[1],  # Email (string)
                existing_data[2].strftime("%Y-%m-%d"),  # Convert date object to string
                existing_data[3],  # Contact (string)
                existing_data[4],  # Education (string)
                existing_data[5].strftime("%Y-%m-%d"),  # Convert date object to string
                normalize_text(existing_data[6]),  # Normalize address
                str(existing_data[7]),  # Convert salary to string for uniformity
                existing_data[8],  # User Type (string)
                existing_data[9]   # Password (string)
            )

        # Prepare new data in the same format
        new_data = (name, email, dob, contact, education, doj, address, salary, usertype, password)

        # Check if any changes exist
        if existing_data == new_data:
            messagebox.showinfo("Information ", "No changes detected. Cannot  Update .")
            con.close()
            return 

        # Execute the update query
        cur.execute("""
            UPDATE EMPLOYEES 
            SET EMP_NAME = ?, EMP_EMAIL = ?, EMP_DOB = ?, EMP_CONTACT = ?, EMP_EDUCATION = ?, 
                EMP_DOJ = ?, EMP_ADDRESS = ?, EMP_SALARY = ?, EMP_USERTYPE = ?, EMP_PASSWORD = ?
            WHERE EMP_ID = ?
        """, (name, email, dob, contact, education, doj, address, salary, usertype, password, empid))

        con.commit()
        treeview_data()
        messagebox.showinfo("Success", f"Employee {name} info updated successfully.")  
        con.close()

    except Exception as e:
        messagebox.showerror("Error", str(e))
def delete_employee(empid):
    selection=employee_tree_view.selection()
    if not selection: 
        messagebox.showerror("Error", "Please select an employee to delete")
    else:
        result=messagebox.askyesno("Do you really want to delete this employee")
        if result:
            try:
                con,cur=connect_db() 
                if not con or not cur:
                    messagebox.showerror("Error", "Failed to connect to database")
                    return 
                cur.execute("DELETE FROM EMPLOYEES WHERE EMP_ID=?",(empid,))
                con.commit()
                treeview_data()
                messagebox.showinfo("Success", f"Employee {empid} deleted successfully.")
            except Exception as e:
                messagebox.showerror("Error", str(e))
            finally:
                con.close() 
# Mapping UI column names to database column names
column_mapping = {
    "ID": "EMP_ID",
    "Name": "EMP_NAME",
    "Email": "EMP_EMAIL",
    "Date of Birth": "EMP_DOB",
    "Contact": "EMP_CONTACT",
    "Education": "EMP_EDUCATION",
    "Date of Joining": "EMP_DOJ",
    "Address": "EMP_ADDRESS",
    "Salary": "EMP_SALARY",
    "User Type": "EMP_USERTYPE",
    "Password": "EMP_PASSWORD"
}

def search_employee(search_option, value):
    if search_option == "Search by":
        messagebox.showerror("Error", "No Option is Selected")
    elif value == '':
        messagebox.showerror("Error", "Please enter a value to search") 
    else:
        try:
            con, cur = connect_db()
            if not con or not cur:
                messagebox.showerror("Error", "Failed to connect to database")
                return
            
            # Convert search_option to the corresponding database column name
            db_column = column_mapping.get(search_option)

            if not db_column:
                messagebox.showerror("Error", "Invalid search option")
                return

            # Execute the query with correct column name
            cur.execute(f"SELECT * FROM EMPLOYEES WHERE {db_column} LIKE ?", ('%' + value + '%',))
            records = cur.fetchall()

            # Clear the tree view and insert new records
            employee_tree_view.delete(*employee_tree_view.get_children())
            for record in records:
                employee_tree_view.insert("", "end", values=list(record)) 
            
            con.close()
        except Exception as e:
            messagebox.showerror("Error", str(e))
def showall(search_combo_box,search_entry):
    search_combo_box.set("Search by")
    search_entry.delete(0,END)
    treeview_data()
def employee_form(window):
    global back_image , employee_tree_view
    #employee frame
    employee_frame=Frame(window,bg="white",width=1154,height=750) 
    employee_frame.place(x=212,y=90) 
    #employee label
    employee_label=Label(employee_frame,text="Manage Employees Detail",font=("ms sans serif", 15, "bold"),bg="#47eb00",fg="black") 
    employee_label.place(x=0,y=0,relwidth=1)
    #back button 
    back_image=PhotoImage(file="back.png")
    back_button=Button(employee_frame,image=back_image,bd=0,cursor="hand2", bg="white",command=lambda:employee_frame.destroy())
    back_button.place(x=0,y=34) 
    #top frame
    top_frame=Frame(employee_frame,bg="#FAF9F6")
    top_frame.place(x=0,y=60,relwidth=1,height=235) 
    #search frame
    search_frame=Frame(top_frame,bg="#FAF9F6")
    search_frame.pack() 
    #search combobox 
    search_combo_box = ttk.Combobox(
    search_frame, values=("ID","Name","Email","Date of Birth","Contact", "Education", 
                "Date of Joining","Adress", "Salary", "User Type", "Password"),
    font=("Times New Roman", 12, "bold"), 
    state="readonly", justify=CENTER, width=15)
    search_combo_box.grid(row=0, column=0, padx=30, pady=10)
    # Set default value 
    search_combo_box.set("Search by") 
    #search entry
    search_entry=Entry(search_frame,width=20,bg="light yellow",font=("Times New Roman", 12, "bold"))
    search_entry.grid(row=0,column=1,padx=30,pady=10)
    #search button
    search_button=Button(search_frame,text="Search",font=("Times New Roman", 13, "bold"),width=10,bg="#47eb00",fg="black",cursor="hand2",command=lambda :search_employee(search_combo_box.get(),search_entry.get())) 
    search_button.grid(row=0,column=2,padx=30,pady=10) 
    #showall button
    show_all_button=Button(search_frame,text="Show All",font=("Times New Roman", 13, "bold"),width=10,bg="#47eb00",fg="black",cursor="hand2",command=lambda:showall(search_combo_box,search_entry)) 
    show_all_button.grid(row=0,column=3,padx=30,pady=10) 
    #scrolbars 
    horizonal_scrolbar=Scrollbar(top_frame,orient=HORIZONTAL)
    vertical_scrolbar=Scrollbar(top_frame,orient=VERTICAL)
    #Treeview
    employee_tree_view= ttk.Treeview(top_frame,columns=("empid","name","email","dob","contact","education","doj","address","salary","usertype","password"),show="headings",yscrollcommand=vertical_scrolbar.set,xscrollcommand=horizonal_scrolbar.set) 
    #Treeview Scrollbars
    horizonal_scrolbar.pack(side=BOTTOM,fill=X)
    vertical_scrolbar.pack(side=RIGHT,fill=Y,pady=(10,0))
    horizonal_scrolbar.config(command=employee_tree_view.xview)
    vertical_scrolbar.config(command=employee_tree_view.yview)
    #Treeview Heading
    employee_tree_view.heading("empid",text="ID")
    employee_tree_view.heading("name",text="Name")
    employee_tree_view.heading("email",text="Email")
    employee_tree_view.heading("dob",text="Date of Birth")
    employee_tree_view.heading("contact",text="Contact")
    employee_tree_view.heading("education",text="Education")
    employee_tree_view.heading("doj",text="Date of Joining")
    employee_tree_view.heading("address",text="Address")
    employee_tree_view.heading("salary",text="Salary") 
    employee_tree_view.heading("usertype",text="User Type")
    employee_tree_view.heading("password",text="Password")
    #Treeview column width
    employee_tree_view.column("empid",width=60)
    employee_tree_view.column("name",width=140)
    employee_tree_view.column("email",width=180)
    employee_tree_view.column("dob",width=100)
    employee_tree_view.column("contact",width=100)
    employee_tree_view.column("education",width=120)
    employee_tree_view.column("doj",width=100)
    employee_tree_view.column("address",width=200)
    employee_tree_view.column("salary",width=140)
    employee_tree_view.column("usertype",width=100)
    employee_tree_view.column("password",width=200)
    #Treeview Pack
    employee_tree_view.pack(pady=(10,0))
    treeview_data() 
    #detail frame
    detail_frame=Frame(employee_frame,bg="#FAF9F6")
    detail_frame.place(x=0,y=300,relwidth=1,height=340)
    #details label
    empid_label=Label(detail_frame,text="Employee ID",font=("Times New Roman", 13, "bold"),bg="#FAF9F6") 
    empid_label.grid(row=0,column=0,padx=10,pady=10,sticky='w')
    empid_entry=Entry(detail_frame,width=20,bg="light yellow",font=("Times New Roman", 12, "bold"))
    empid_entry.grid(row=0,column=1,padx=10,pady=10)
    #name label 
    name_label=Label(detail_frame,text="Name",font=("Times New Roman", 13, "bold"),bg="#FAF9F6")
    name_label.grid(row=0,column=2,padx=10,pady=10,sticky='w')
    name_entry=Entry(detail_frame,width=20,bg="light yellow",font=("Times New Roman", 12, "bold"))
    name_entry.grid(row=0,column=3,padx=10,pady=10)
    #email label    
    email_label=Label(detail_frame,text="Email",font=("Times New Roman", 13, "bold"),bg="#FAF9F6")
    email_label.grid(row=0,column=4,padx=10,pady=10,sticky='w')
    email_entry=Entry(detail_frame,width=20,bg="light yellow",font=("Times New Roman", 12, "bold"))
    email_entry.grid(row=0,column=5,padx=10,pady=10)
    #dob label
    dob_label=Label(detail_frame,text="Date of Birth",font=("Times New Roman", 13, "bold"),bg="#FAF9F6")
    dob_label.grid(row=1,column=0,padx=10,pady=10,sticky='w')
    dob_entry=DateEntry(detail_frame,width=20,state='readonly',date_pattern='dd/mm/yyyy')
    dob_entry.grid(row=1,column=1,padx=10,pady=10)
    #contact label  
    contact_label=Label(detail_frame,text="Contact",font=("Times New Roman", 13, "bold"),bg="#FAF9F6")
    contact_label.grid(row=1,column=2,padx=10,pady=10,sticky='w')
    contact_entry=Entry(detail_frame,width=20,bg="light yellow",font=("Times New Roman", 12, "bold"))
    contact_entry.grid(row=1,column=3,padx=10,pady=10)
    #education label
    education_label=Label(detail_frame,text="Education",font=("Times New Roman", 13, "bold"),bg="#FAF9F6")
    education_label.grid(row=1,column=4,padx=10,pady=10,sticky='w')
    education_combobox=ttk.Combobox(detail_frame, values=["Matric","Inter","Diploma","Bachelors","Masters","PHD"],width=20,font=("Times New Roman", 12, "bold"))
    education_combobox.grid(row=1,column=5,padx=10,pady=10)
    education_combobox.set("Select Education")
    #doj label
    doj_label=Label(detail_frame,text="Date of Joining",font=("Times New Roman", 13, "bold"),bg="#FAF9F6")
    doj_label.grid(row=2,column=0,padx=10,pady=10,sticky='w')
    doj_entry=DateEntry(detail_frame,width=20,state='readonly',date_pattern='dd/mm/yyyy') 
    doj_entry.grid(row=2,column=1,padx=10,pady=10) 
    #adress label 
    address_label=Label(detail_frame,text="Adress",font=("Times New Roman", 13,"bold"),bg="#FAF9F6")
    address_label.grid(row=2,column=2,padx=10,pady=10,sticky='w')
    address_entry = Text(detail_frame, width=20, height=4, bg="light yellow", font=("Times New Roman", 12 ))
    address_entry.grid(row=2, column=3, padx=10, pady=10)
    #salary label 
    salary_label=Label(detail_frame,text="Salary",font=("Times New Roman", 13, "bold"),bg="#FAF9F6") 
    salary_label.grid(row=2,column=4,padx=10,pady=10,sticky='w')
    salary_entry=Entry(detail_frame,width=20,bg="light yellow",font=("Times New Roman", 12, "bold"))
    salary_entry.grid(row=2,column=5,padx=10,pady=10)
    #Usertype label
    usertype_label=Label(detail_frame,text="User Type",font=("Times New Roman", 13, "bold"),bg="#FAF9F6") 
    usertype_label.grid(row=3,column=0,padx=10,pady=10,sticky='w')
    usertype_combobox=ttk.Combobox(detail_frame, values=["Admin","Employee"],width=15,font=("Times New Roman", 12, "bold"))
    usertype_combobox.grid(row=3,column=1,padx=10,pady=10)
    usertype_combobox.set("Select User Type") 
    #password label
    password_label=Label(detail_frame,text="Password",font=("Times New Roman", 13, "bold"),bg="#FAF9F6") 
    password_label.grid(row=3,column=2,padx=10,pady=10,sticky='w')
    password_entry=Entry(detail_frame,width=20,bg="light yellow",font=("Times New Roman", 12, "bold"))
    password_entry.grid(row=3,column=3,padx=10,pady=10)
    #Buttons 
    add_button = Button(detail_frame, text="Add", font=("Times New Roman", 13, "bold"), width=10, 
                    bg="#47eb00", fg="black", cursor="hand2",
                    command=lambda: add_employee(empid_entry.get(), name_entry.get(), email_entry.get(), 
                                                 dob_entry.get(), contact_entry.get(), education_combobox.get(), 
                                                 doj_entry.get(), address_entry.get("1.0", END), salary_entry.get(), 
                                                 usertype_combobox.get(), password_entry.get()))
    add_button.grid(row=4, column=1, padx=30, pady=10) 
 
    update_button=Button(detail_frame,text="Update",font=("Times New Roman", 13,"bold"),width=10,bg="yellow",fg="black",cursor="hand2",command=lambda :update_employee(empid_entry.get(), name_entry.get(), email_entry.get(), 
                                                 dob_entry.get(), contact_entry.get(), education_combobox.get(), 
                                                 doj_entry.get(), address_entry.get("1.0", END), salary_entry.get(), 
                                                 usertype_combobox.get(), password_entry.get()))  

    update_button.grid(row=4,column=2,padx=30,pady=10) 
    clear_button=Button(detail_frame,text="Clear",font=("Times New Roman", 13, "bold"),width=10,bg="#008ECC",fg="white",cursor="hand2",command=lambda: clear_fields(empid_entry, name_entry, email_entry, 
                                                 dob_entry, contact_entry, education_combobox, 
                                                 doj_entry, address_entry, salary_entry, 
                                                 usertype_combobox, password_entry,True) ) 
    clear_button.grid(row=4,column=3,padx=60,pady=60)
    delete_button=Button(detail_frame,text="Delete",font=("Times New Roman", 13, "bold"),width=10,bg="#FC2E2E",fg="white",cursor="hand2",command=lambda:delete_employee(empid_entry.get())) 
    delete_button.grid(row=4,column=4,padx=30,pady=10)
    #Data Selection call 
    employee_tree_view.bind("<ButtonRelease-1>",lambda event:select_data(event,empid_entry, name_entry, email_entry, dob_entry, contact_entry, education_combobox,doj_entry, address_entry, salary_entry, usertype_combobox, password_entry))    