from tkinter import *
from tkinter import ttk 
from tkcalendar import DateEntry
from datetime import datetime
import pymysql 

def employee_form(window):
    global back_image 
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
    search_frame, values=("ID","Name","Email","Date of Birth",
    "Contact","Education","Date of Joining","Address","Salary"),
    font=("Times New Roman", 12, "bold"), 
    state="readonly", justify=CENTER, width=15)
    search_combo_box.grid(row=0, column=0, padx=30, pady=10)
    # Set default value
    search_combo_box.set("Search by") 
    #search entry
    search_entry=Entry(search_frame,width=20,bg="light yellow",font=("Times New Roman", 12, "bold")).grid(row=0,column=1,padx=30,pady=10) 
    #search button
    search_button=Button(search_frame,text="Search",font=("Times New Roman", 13, "bold"),width=10,bg="#47eb00",fg="black",cursor="hand2").grid(row=0,column=2,padx=30,pady=10)  
    #showall button
    show_all_button=Button(search_frame,text="Show All",font=("Times New Roman", 13, "bold"),width=10,bg="#47eb00",fg="black",cursor="hand2").grid(row=0,column=3,padx=30,pady=10) 
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
    save_button=Button(detail_frame,text="Save",font=("Times New Roman", 13, "bold"),width=10,bg="#47eb00",fg="black",cursor="hand2").grid(row=4,column=1,padx=30,pady=10)
    update_button=Button(detail_frame,text="Update",font=("Times New Roman", 13,"bold"),width=10,bg="yellow",fg="black",cursor="hand2").grid(row=4,column=2,padx=30,pady=10)  
    clear_button=Button(detail_frame,text="Clear",font=("Times New Roman", 13, "bold"),width=10,bg="#008ECC",fg="white",cursor="hand2").grid(row=4,column=3,padx=60,pady=60)
    delete_button=Button(detail_frame,text="Delete",font=("Times New Roman", 13, "bold"),width=10,bg="#FC2E2E",fg="white",cursor="hand2").grid(row=4,column=4,padx=30,pady=10)