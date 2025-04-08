from tkinter import *
from datetime import datetime
from employees import employee_form
from suppliers import suppliers_form 
class Dashboard:
    def __init__(self, window):
        self.window = window
        self.window.title("Dashboard")
        self.window.geometry("1366x768+0+0")
        self.window.resizable(0, 0)
        self.window.config(bg="white")
        
        self.setup_ui()
        self.update_datetime() 
    
    def setup_ui(self):
        # Dashboard Title with Logo
        self.soultechlogo = PhotoImage(file="soultechlogo.png")
        title = Label(self.window, image=self.soultechlogo, compound=LEFT, text="Al-Fazal Traders", 
                      font=("ms sans serif", 25, "bold"), bg="white", fg="black", bd=5)
        title.place(x=0, y=0, relwidth=1)
        
        # Logout Button
        self.logout = Button(self.window, text="Log Out", font=("times new roman", 15, "bold"),
                             bg="#47eb00", fg="white", bd=0, cursor="hand2")
        self.logout.place(x=1200, y=12)
        self.logout.bind("<Enter>", self.on_enter)
        self.logout.bind("<Leave>", self.on_leave)
        
        # Subtitle with Date and Time
        self.subtitle = Label(self.window, text="", font=("Helvetica", 15, "bold"), bg="black", fg="white")
        self.subtitle.place(x=0, y=60, relwidth=1)
        
        # Left Frame for Menu
        self.leftframe = Frame(self.window)
        self.leftframe.place(x=0, y=90, width=210, height=700)
        
        menulabel = Label(self.leftframe, text="Menu", font=("ms sans serif", 15, "bold"), bg="#47eb00", fg="black")
        menulabel.pack(fill=X)
        
        self.create_menu_buttons()
        self.create_statistics_frames() 
    
    def create_menu_buttons(self):
        # Buttons with Icons
        buttons = [
            ("employee.png", "Employees", lambda: employee_form(self.window)),
            ("supplier.png", "Suppliers", lambda :suppliers_form(window)),
            ("category.png", "Categories", None),
            ("product.png", "Products", None),
            ("sales.png", "Sales", None),
            ("exit.png", "Exit", self.window.quit)
        ]
        
        for icon, text, cmd in buttons:
            img = PhotoImage(file=icon)
            button = Button(self.leftframe, image=img, text=f" {text}", compound=LEFT, font=("times new roman", 20, "bold"),
                            anchor="w", padx=10, command=cmd)
            button.image = img  # Prevent garbage collection
            button.pack(fill=X, pady=20)
    
    def create_statistics_frames(self):
        stats = [
            ("total_emp.png", "Total Employees", "#007bff", 400, 110),
            ("total_sup.png", "Total Suppliers", "#6610f2", 800, 110),
            ("total_cat.png", "Total Categories", "#28a745", 400, 325),
            ("total_prod.png", "Total Products", "#ffc107", 800, 325),
            ("total_sales.png", "Total Sales", "#dc3545", 600, 540)
        ] 
        
        for icon, label, color, x, y in stats:
            self.create_statistic_frame(icon, label, color, x, y)
    
    def create_statistic_frame(self, icon_file, label_text, bg_color, x, y):
        frame = Frame(self.window, bg=bg_color, bd=5, relief=RIDGE)
        frame.place(x=x, y=y, width=300, height=180)
        
        icon = PhotoImage(file=icon_file)  
        icon_label = Label(frame, image=icon, bg=bg_color)
        icon_label.image = icon  # Prevent garbage collection
        icon_label.pack(pady=10)
        
        text_label = Label(frame, text=label_text, font=("times new roman", 20, "bold"), bg=bg_color, fg="white")
        text_label.pack()
        
        count_label = Label(frame, text="0", font=("times new roman", 30, "bold"), bg=bg_color, fg="white")
        count_label.pack()
    
    def update_datetime(self):
        now = datetime.now().strftime("%d/%m/%Y  %I:%M:%S %p")
        self.subtitle.config(text=f"Welcome: Admin\t\tDate: {now.split()[0]}\t\tTime: {now.split()[1]} {now.split()[2]}")
        self.subtitle.after(1000, self.update_datetime)
    
    def on_enter(self, event):
        self.logout.config(bg="#FC2E2E", fg="white")
    
    def on_leave(self, event):
        self.logout.config(bg="#47eb00", fg="black")

if __name__ == "__main__":
    window = Tk() 
    app = Dashboard(window) 
    window.mainloop()