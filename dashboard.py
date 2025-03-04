from tkinter import *
from datetime import datetime
from employees import employee_form 



#GUI PART 

# Initialize main window
window = Tk()
window.title("Dashboard")
window.geometry("1366x768+0+0")
window.resizable(0, 0)
window.config(bg="white") 

# Dashboard Title with Logo
soultechlogo = PhotoImage(file="soultechlogo.png")
title = Label(window, image=soultechlogo, compound=LEFT, text=" Soultech Pakistan",
              font=("ms sans serif", 25, "bold"), bg="white", fg="black", bd=5) 
title.place(x=0, y=0, relwidth=1)

# Function to change logout button color on hover
def on_enter(e):
    logout.config(bg="#FC2E2E", fg="white") 

def on_leave(e):
    logout.config(bg="#47eb00", fg="black") 

# Logout Button
logout = Button(window, text="Log Out", font=("times new roman", 15, "bold"),
                bg="#47eb00", fg="white", bd=0, cursor="hand2")
logout.place(x=1200, y=12)
logout.bind("<Enter>", on_enter)
logout.bind("<Leave>", on_leave)

# Subtitle with Date and Time
def update_datetime():
    now = datetime.now().strftime("%d/%m/%Y  %I:%M:%S %p")  # Format: DD/MM/YYYY HH:MM:SS AM/PM
    subtitle.config(text=f"Welcome: Admin\t\tDate: {now.split()[0]}\t\tTime: {now.split()[1]} {now.split()[2]}")
    subtitle.after(1000, update_datetime)  # Update every second
# Create a Label
subtitle =Label(window, text="", font=("Helvetica", 15, "bold"), bg="black", fg="white")
subtitle.place(x=0, y=60, relwidth=1) 
# Start updating time
update_datetime()

# Left Frame for Menu
leftframe = Frame(window)
leftframe.place(x=0, y=90, width=210, height=700) 

# Menu Label 
menulabel = Label(leftframe, text="Menu", font=("ms sans serif", 15, "bold"),bg="#47eb00",fg="black")
menulabel.pack(fill=X)

# Employee Button
empolyee_icon = PhotoImage(file="employee.png")
employee_button = Button(leftframe, image=empolyee_icon, text="Employees", compound=LEFT,
                         font=("times new roman", 20, "bold"), anchor="w", padx=10,command=lambda :employee_form(window))
employee_button.pack(fill=X,pady=(25,20))

# Supplier Button
supplier_icon = PhotoImage(file="supplier.png")
supplier_button = Button(leftframe, image=supplier_icon, text=" Suppliers", compound=LEFT,
                          font=("times new roman", 20, "bold"), anchor="w", padx=10)
supplier_button.pack(fill=X,pady=20)

# Category Button
caetgory_icon = PhotoImage(file="category.png")
category_button = Button(leftframe, image=caetgory_icon, text=" Categories", compound=LEFT,
                          font=("times new roman", 20, "bold"), anchor="w", padx=10)
category_button.pack(fill=X,pady=20)

# Product Button
product_icon = PhotoImage(file="product.png")
product_button = Button(leftframe, image=product_icon, text=" Products", compound=LEFT,
                         font=("times new roman", 20, "bold"), anchor="w", padx=10)
product_button.pack(fill=X,pady=20)

# Sales Button
sales_icon = PhotoImage(file="sales.png")
sales_button = Button(leftframe, image=sales_icon, text=" Sales", compound=LEFT,
                       font=("times new roman", 20, "bold"), anchor="w", padx=10)
sales_button.pack(fill=X,pady=20)

# Exit Button
exit_icon = PhotoImage(file="exit.png")
exit_button = Button(leftframe, image=exit_icon, text=" Exit", compound=LEFT,
                      font=("times new roman", 20, "bold"), anchor="w", padx=10)
exit_button.pack(fill=X,pady=20)

# Employee Statistics Frame
emp_frame = Frame(window, bg="#007bff", bd=5, relief=RIDGE)
emp_frame.place(x=400, y=125, width=300, height=200)

# Employee Statistics Icon
total_emp_icon = PhotoImage(file="total_emp.png")
total_emp_icon_label = Label(emp_frame, image=total_emp_icon, bg="#007bff")
total_emp_icon_label.pack(pady=10) 

# Employee Statistics Labels
total_emp_label = Label(emp_frame, text="Total Employees", font=("times new roman", 20, "bold"),
                         bg="#007bff", fg="white")
total_emp_label.pack()

total_emp_count_label = Label(emp_frame, text="0", font=("times new roman", 30, "bold"),
                              bg="#007bff", fg="white")
total_emp_count_label.pack()

#Supplier Statistic Frame

supplier_frame = Frame(window, bg="#6610f2", bd=5, relief=RIDGE)
supplier_frame.place(x=800, y=125, width=300, height=200)

# Supplier Statistics Icon

total_supplier_icon = PhotoImage(file="total_sup.png")
total_supplier_icon_label = Label(supplier_frame, image=total_supplier_icon, bg="#6610f2")
total_supplier_icon_label.pack(pady=10)
# Supplier Statistics Labels

total_supplier_label = Label(supplier_frame, text="Total Suppliers", font=("times new roman", 20, "bold"),
                             bg="#6610f2", fg="white")
total_supplier_label.pack()

# Supplier Statistics Count Labels

total_supplier_count_label = Label(supplier_frame, text="0", font=("times new roman", 30, "bold"),
                                   bg="#6610f2", fg="white")
total_supplier_count_label.pack() 

#Total Categories Frame
categories_frame = Frame(window, bg="#28a745", bd=5, relief=RIDGE)
categories_frame.place(x=400, y=340, width=300, height=200)

# Categories Statistics Icon
total_categories_icon = PhotoImage(file="total_cat.png")
total_categories_icon_label = Label(categories_frame, image=total_categories_icon, bg="#28a745")
total_categories_icon_label.pack(pady=10)
# Categories Statistics Labels
total_categories_label = Label(categories_frame, text="Total Categories", font=("times new roman", 20, "bold"),
                               bg="#28a745", fg="white")
total_categories_label.pack()
# Categories Statistics Count Labels
total_categories_count_label = Label(categories_frame, text="0", font=("times new roman", 30, "bold"),
                                     bg="#28a745", fg="white")
total_categories_count_label.pack() 

#Total Products Frame
products_frame = Frame(window, bg="#ffc107", bd=5, relief=RIDGE)
products_frame.place(x=800, y=340, width=300, height=200) 
# Products Statistics Icon
total_products_icon = PhotoImage(file="total_prod.png")
total_products_icon_label = Label(products_frame, image=total_products_icon, bg="#ffc107")
total_products_icon_label.pack(pady=10)
# Products Statistics Labels
total_products_label = Label(products_frame, text="Total Products", font=("times new roman", 20, "bold"),
                             bg="#ffc107", fg="white")
total_products_label.pack()
# Products Statistics Count Labels
total_products_count_label = Label(products_frame, text="0", font=("times new roman", 30, "bold"),
                                   bg="#ffc107", fg="white")
total_products_count_label.pack() 

# Total Sales Frame
sales_frame = Frame(window, bg="#dc3545", bd=5, relief=RIDGE)
sales_frame.place(x=600, y=550, width=300, height=180)
# Sales Statistics Icon
total_sales_icon = PhotoImage(file="total_sales.png") 
total_sales_icon_label = Label(sales_frame, image=total_sales_icon, bg="#dc3545")
total_sales_icon_label.pack(pady=10)
# Sales Statistics Labels 
total_sales_label = Label(sales_frame, text="Total Sales", font=("times new roman", 20, "bold"),
                          bg="#dc3545", fg="white")
total_sales_label.pack()
# Sales Statistics Count Labels
total_sales_count_label = Label(sales_frame, text="0", font=("times new roman", 30, "bold"),
                                bg="#dc3545", fg="white")
total_sales_count_label.pack() 
# Run the main loop
window.mainloop()
