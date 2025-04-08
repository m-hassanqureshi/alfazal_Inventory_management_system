from tkinter import *
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import date, datetime
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
            IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'SUPPLIERS')
            CREATE TABLE SUPPLIERS (
                INVOICE_NO INT PRIMARY KEY NOT NULL,
                SUPPLIER_NAME VARCHAR(50) NOT NULL,
                CONTACT VARCHAR(15) NOT NULL,
                DESCRIPTION VARCHAR(200) NOT NULL
            ) 
        ''') 
        con.commit()
        
        return con, cur 
    
    except Exception as e:
        messagebox.showerror("Error: Database Connection Error. Try Again", str(e)) 

def treeview_data():
    con, cur = connect_db()
    if not con or not cur:
        return

    # Clear existing data in Treeview
    for row in supplier_tree.get_children():
        supplier_tree.delete(row)

    cur.execute("SELECT * FROM SUPPLIERS")
    rows = cur.fetchall()

    for row in rows:
        supplier_tree.insert("", END, values=list(row))  # Unpacking the tuple

    con.close()

def add_supplier(invoice_no, name, contact, description):
    if not all([invoice_no, name, contact, description]): 
        messagebox.showerror("Error", "All fields are required.")
        return  
    elif len(contact) != 11: 
        messagebox.showerror("Error", "Please enter a valid contact number of 11 digits.") 
        return  

    try:
        con, cur = connect_db()
        invoice_no = int(invoice_no)  # Convert to integer

        cur.execute("INSERT INTO SUPPLIERS VALUES (?, ?, ?, ?)", 
                    invoice_no, name, contact, description)

        con.commit()
        treeview_data() 
        messagebox.showinfo("Success", "Supplier added successfully.")  
        con.close()
        
    except ValueError:
        messagebox.showerror("Error", "Invoice No must be a number.")
    except pyodbc.IntegrityError:
        messagebox.showerror("Error", "Invoice No already exists. Choose a unique Invoice No.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def clear_fields(invoice_entry, name_entry, contact_entry, description_entry, check): 
    invoice_entry.delete(0, END)
    name_entry.delete(0, END)
    contact_entry.delete(0, END)
    description_entry.delete("1.0", END) 
    if check: 
        supplier_tree.selection_remove(supplier_tree.selection()) 

def select_data(event, invoice_entry, name_entry, contact_entry, description_entry):
    index = supplier_tree.selection()

    if not index:  # Check if selection is empty
        messagebox.showerror("Error", "No row selected")
        return

    content = supplier_tree.item(index)
    data = content["values"]

    if not data:  # Ensure data is not empty
        messagebox.showerror("Error", "No data present")
        return

    clear_fields(invoice_entry, name_entry, contact_entry, description_entry, False)  # No need to remove selection 

    invoice_entry.insert(0, data[0])
    name_entry.insert(0, data[1])
    contact_value = str(data[2]).zfill(11) if data[2] else ""
    contact_entry.insert(0, contact_value)
    description_entry.insert("1.0", data[3])

def update_supplier(invoice_no, name, contact, description):
    selected = supplier_tree.selection()
    
    if not selected:
        messagebox.showerror("Error", "No row selected")
        return  
    elif not all([invoice_no, name, contact, description]): 
        messagebox.showerror("Error", "All fields are required.")
        return 
    elif len(contact) != 11:
        messagebox.showerror("Error", "Please enter a valid contact number of 11 digits.")
        return    

    try:
        con, cur = connect_db()
        if not con or not cur:
            messagebox.showerror("Error", "Failed to connect to database")
            return 

        # Fetch the current data from the database
        cur.execute("SELECT SUPPLIER_NAME, CONTACT, DESCRIPTION FROM SUPPLIERS WHERE INVOICE_NO = ?", (invoice_no,))
        existing_data = cur.fetchone()

        # Normalize fetched data for proper comparison
        if existing_data:
            existing_data = (
                existing_data[0],  # Name (string)
                existing_data[1],  # Contact (string)
                existing_data[2]   # Description (string)
            )

        # Prepare new data in the same format
        new_data = (name, contact, description)

        # Check if any changes exist
        if existing_data == new_data:
            messagebox.showinfo("Information", "No changes detected. Cannot Update.")
            con.close()
            return 

        # Execute the update query
        cur.execute("""
            UPDATE SUPPLIERS 
            SET SUPPLIER_NAME = ?, CONTACT = ?, DESCRIPTION = ?
            WHERE INVOICE_NO = ?
        """, (name, contact, description, invoice_no))

        con.commit()
        treeview_data()
        messagebox.showinfo("Success", f"Supplier {name} info updated successfully.")  
        con.close()

    except Exception as e:
        messagebox.showerror("Error", str(e))

def delete_supplier(invoice_no):
    selection = supplier_tree.selection()
    if not selection: 
        messagebox.showerror("Error", "Please select a supplier to delete")
    else:
        result = messagebox.askyesno("Do you really want to delete this supplier")
        if result:
            try:
                con, cur = connect_db() 
                if not con or not cur:
                    messagebox.showerror("Error", "Failed to connect to database")
                    return 
                cur.execute("DELETE FROM SUPPLIERS WHERE INVOICE_NO = ?", (invoice_no,))
                con.commit()
                treeview_data()
                messagebox.showinfo("Success", f"Supplier {invoice_no} deleted successfully.")
            except Exception as e:
                messagebox.showerror("Error", str(e))
            finally:
                con.close() 

# Mapping UI column names to database column names
column_mapping = {
    "Invoice No.": "INVOICE_NO",
    "Supplier Name": "SUPPLIER_NAME",
    "Contact": "CONTACT",
    "Description": "DESCRIPTION"
}

def search_supplier(search_option, value):
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
            cur.execute(f"SELECT * FROM SUPPLIERS WHERE {db_column} LIKE ?", ('%' + value + '%',))
            records = cur.fetchall()

            # Clear the tree view and insert new records
            supplier_tree.delete(*supplier_tree.get_children())
            for record in records:
                supplier_tree.insert("", "end", values=list(record)) 
            
            con.close()
        except Exception as e:
            messagebox.showerror("Error", str(e))

def showall(search_combo_box, search_entry):
    search_combo_box.set("Search by")
    search_entry.delete(0, END)
    treeview_data()

def suppliers_form(window):
    global back_image, supplier_tree
    # Supplier frame
    suppliers_frame = Frame(window, bg="white", width=1154, height=750)
    suppliers_frame.place(x=212, y=90)
    
    suppliers_label = Label(suppliers_frame, text="Manage Suppliers Detail", font=("ms sans serif", 15, "bold"), bg="#47eb00", fg="black")
    suppliers_label.place(x=0, y=0, relwidth=1)
    
    # Back button
    back_image = PhotoImage(file="back.png")
    back_button = Button(suppliers_frame, image=back_image, bd=0, cursor="hand2", bg="white", command=lambda: suppliers_frame.destroy())
    back_button.place(x=0, y=34)
    
    # Left frame
    left_frame = Frame(suppliers_frame, bg="white", width=550, height=550, bd=2, relief="ridge")
    left_frame.place(x=0, y=70)
    left_frame.grid_propagate(False)  # Prevents resizing of frame
    
    # Invoice label and entry
    invoice_label = Label(left_frame, text="Invoice No.", font=("Times New Roman", 13, "bold"), bg="white")
    invoice_label.grid(row=0, column=0, padx=10, pady=10, sticky='w')
    invoice_entry = Entry(left_frame, width=30, bg="light yellow", font=("Times New Roman", 12, "bold"))
    invoice_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")
    
    # Supplier name label and entry
    supplier_name_label = Label(left_frame, text="Supplier Name", font=("Times New Roman", 13, "bold"), bg="white")
    supplier_name_label.grid(row=1, column=0, padx=10, pady=10, sticky='w')
    supplier_name_entry = Entry(left_frame, width=30, bg="light yellow", font=("Times New Roman", 12, "bold"))
    supplier_name_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")
    
    # Contact label and entry
    contact_label = Label(left_frame, text="Contact", font=("Times New Roman", 13, "bold"), bg="white")
    contact_label.grid(row=2, column=0, padx=10, pady=10, sticky='w')
    contact_entry = Entry(left_frame, width=30, bg="light yellow", font=("Times New Roman", 12, "bold"))
    contact_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")

    # Description label and entry
    description_label = Label(left_frame, text="Description", font=("Times New Roman", 13, "bold"), bg="white")
    description_label.grid(row=3, column=0, padx=10, pady=10, sticky='w')
    
    description_entry = Text(left_frame, width=30, height=10, bg="light yellow", font=("Times New Roman", 12), wrap=WORD)
    description_entry.grid(row=3, column=1, padx=10, pady=10, sticky="w")

    # Ensuring the left frame doesn't resize based on children
    left_frame.grid_propagate(False)
    
    # Ensure columns are evenly spaced
    left_frame.grid_columnconfigure(0, weight=1)
    left_frame.grid_columnconfigure(1, weight=1)

    # Add button
    add_button = Button(left_frame, text="Add", font=("Times New Roman", 13, "bold"), width=10, 
                        bg="#47eb00", fg="black", cursor="hand2",
                        command=lambda: add_supplier(invoice_entry.get(), supplier_name_entry.get(), contact_entry.get(), description_entry.get("1.0", END)))
    add_button.grid(row=4, column=0, pady=8)

    # Update button
    update_button = Button(left_frame, text="Update", font=("Times New Roman", 13, "bold"), width=10, 
                        bg="yellow", fg="black", cursor="hand2",
                        command=lambda: update_supplier(invoice_entry.get(), supplier_name_entry.get(), contact_entry.get(), description_entry.get("1.0", END)))
    update_button.grid(row=4, column=1, pady=8)

    # Clear button
    clear_button = Button(left_frame, text="Clear", font=("Times New Roman", 13, "bold"), width=10, 
                        bg="#008ECC", fg="white", cursor="hand2",
                        command=lambda: clear_fields(invoice_entry, supplier_name_entry, contact_entry, description_entry, True))
    clear_button.grid(row=5, column=0, pady=8)

    # Delete button
    delete_button = Button(left_frame, text="Delete", font=("Times New Roman", 13, "bold"), width=10, 
                        bg="#FC2E2E", fg="white", cursor="hand2",
                        command=lambda: delete_supplier(invoice_entry.get()))
    delete_button.grid(row=5, column=1, pady=8)
    
    # Right frame
    right_frame = Frame(suppliers_frame, bg="white", width=600, height=550, bd=2, relief="ridge")
    right_frame.place(x=550, y=70)
    right_frame.grid_propagate(False)  # Prevents resizing of frame

    # Search combobox 
    search_combo_box = ttk.Combobox(
        right_frame, values=("Invoice No.","Supplier Name","Contact"),
        font=("Times New Roman", 12, "bold"), 
        state="readonly", justify=CENTER, width=15)
    search_combo_box.grid(row=0, column=0, padx=10, pady=5)
    # Set default value  
    search_combo_box.set("Search by") 
    # Search entry 
    search_entry = Entry(right_frame, width=20, bg="light yellow", font=("Times New Roman", 12, "bold"))
    search_entry.grid(row=0, column=1, padx=10, pady=5)
    # Search button
    search_button = Button(right_frame, text="Search", font=("Times New Roman", 13, "bold"), width=10, bg="#47eb00", fg="black", cursor="hand2", command=lambda: search_supplier(search_combo_box.get(), search_entry.get())) 
    search_button.grid(row=0, column=2, padx=10, pady=5) 
    # Show all button
    show_all_button = Button(right_frame, text="Show All", font=("Times New Roman", 13, "bold"), width=8, bg="#47eb00", fg="black", cursor="hand2", command=lambda: showall(search_combo_box, search_entry)) 
    show_all_button.grid(row=0, column=3, padx=10, pady=5) 
    # Supplier treeview
    supplier_tree = ttk.Treeview(right_frame, columns=("Invoice No.", "Supplier Name", "Contact", "Description"), 
                                show="headings", height=22) # Headings only
    supplier_tree.heading("Invoice No.", text="Invoice No.")
    supplier_tree.heading("Supplier Name", text="Supplier Name")
    supplier_tree.heading("Contact", text="Contact")
    supplier_tree.heading("Description", text="Description")

    supplier_tree.column("Invoice No.", width=100)
    supplier_tree.column("Supplier Name", width=150)
    supplier_tree.column("Contact", width=100)
    supplier_tree.column("Description", width=200)

    supplier_tree.grid(row=1, column=0, padx=10, pady=10, columnspan=4)

    # Scrollbar
    vertical_scrollbar = Scrollbar(right_frame, orient="vertical", command=supplier_tree.yview)
    vertical_scrollbar.grid(row=1, column=4, sticky="ns")
    horizontal_scrollbar = Scrollbar(right_frame, orient="horizontal", command=supplier_tree.xview)
    horizontal_scrollbar.grid(row=2, column=0, sticky="ew", columnspan=4)

    supplier_tree.configure(yscrollcommand=vertical_scrollbar.set, xscrollcommand=horizontal_scrollbar.set)

    # Bind the select event
    supplier_tree.bind("<ButtonRelease-1>", lambda event: select_data(event, invoice_entry, supplier_name_entry, contact_entry, description_entry))

    treeview_data()