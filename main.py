import tkinter as tk
from tkinter import messagebox
import product_management as pm
import sqlconnect as sql
import Sales_Tracking as st
import File_IO as IO


def Load_Product_Management():
    def On_Closing():
        confirmation=messagebox.askyesno("Confirm Quit", "Are you sure you want to quit?")
        if confirmation :
            Product_Management.destroy()
            Load_Main_Window()      

    main_window.destroy()
    Product_Management=tk.Tk()
    Product_Management.config(bg="white")
    Product_Management.title("Product Management")
    Product_Management.protocol("WM_DELETE_WINDOW",On_Closing)
    Product_Management.iconphoto(False,tk.PhotoImage(file="./Image/tag.png"))
    pm.ProductManagement(Product_Management)
    Product_Management.mainloop()

def Load_Sales_Tracking():
    def On_Closing():
        confirmation=messagebox.askyesno("Confirm Quit", "Are you sure you want to quit?")
        if confirmation :
            Sales_Tracking.destroy()
            Load_Main_Window()      

    main_window.destroy()
    Sales_Tracking=tk.Tk()
    Sales_Tracking.config(bg="white")
    Sales_Tracking.title("Sales Tracking")
    Sales_Tracking.iconphoto(False,tk.PhotoImage(file="./Image/id card.png"))

    st.Sales_Tracking(Sales_Tracking)
    Sales_Tracking.protocol("WM_DELETE_WINDOW",On_Closing)
    Sales_Tracking.mainloop()

def Load_Reporting():
    def On_Closing():
        FileIO.destroy()
        Load_Main_Window()      

    main_window.destroy()
    FileIO=tk.Tk()
    FileIO.config(bg="white")
    FileIO.title("FileIO")
    FileIO.iconphoto(False,tk.PhotoImage(file="./Image/file.png"))

    IO.FileIO(FileIO)
    FileIO.protocol("WM_DELETE_WINDOW",On_Closing)
    FileIO.mainloop()

def Load_About():
    messagebox.showinfo("About", "Inventory Management System v1.0")


def Load_Main_Window():
    def On_Closing():
        confirmation = messagebox.askyesno("Confirm Quit", "Are you sure you want to quit?")
        if confirmation:
            main_window.destroy()

    def Load_Botton():
        Buttons[0].place_forget()
        Buttons[0].place(x=150,y=125,width=250,height=150)
        Buttons[1].place_forget()
        Buttons[1].place(x=600,y=125,width=250,height=150)
        Buttons[2].place_forget()
        Buttons[2].place(x=150,y=375,width=250,height=150)
        Buttons[3].place_forget()
        Buttons[3].place(x=600,y=375,width=250,height=150)

    global main_window
    main_window=tk.Tk()
    Buttons = [tk.Button(main_window,text="Product Management",command=Load_Product_Management),
    tk.Button(main_window,text="Sales Tracking",command=Load_Sales_Tracking),
    tk.Button(main_window,text="Import/Export File",command=Load_Reporting),
    tk.Button(main_window,text="About",command=Load_About)]

    main_window.resizable(False,False)
    main_window.config(bg="white")
    text=tk.Label(main_window,text="Welcome to Inventory Management System",bg="white",fg="black",font=("Times New Roman",20,"bold"))
    text.pack()
    main_window.iconphoto(False,tk.PhotoImage(file="./Image/home.png"))
    main_window.title("Inventory Management System")
    main_window.minsize(1000,600)
    main_window.protocol("WM_DELETE_WINDOW", On_Closing)
    Load_Botton()
    main_window.mainloop()

def Log_In_System():
    def On_Closing():
        confirmation = messagebox.askyesno("Confirm Quit", "Are you sure you want to quit?")
        if confirmation:
            exit()
    def Submit():
        information=[str(entry.get()) for entry in entries.values()]
        global _flag
        _flag=sql.ConnectTodb(information[0],information[1],information[2],information[3])
        if not _flag:
            messagebox.showinfo("Remind","Can not access to the SQL, please check your information.")
        log_in_window.destroy()
    
    defult=['85.239.52.190','testuser','testpasswd','test']
    log_in_window = tk.Tk()
    log_in_window.title("Please log in your SQL")
    log_in_window.iconphoto(False,tk.PhotoImage(file="./Image/login.png"))
    log_in_window.minsize(300,180)
    labels=["Host","User","Password","Database"]
    entries={}
    for i,label in enumerate(labels):
        tk.Label(log_in_window, text=label).grid(row=i, column=0, padx=10, pady=5)
        entry = tk.Entry(log_in_window)
        entry.grid(row=i, column=1, padx=10, pady=5)
        entries[label]=entry
        entry.insert(0,defult[i])
    tk.Button(log_in_window, text="Submit", command=Submit).grid(row=len(labels), column=1, padx=10, pady=10)
    log_in_window.protocol("WM_DELETE_WINDOW", On_Closing)
    log_in_window.mainloop()

def Main():
    while not _flag:
        Log_In_System()
    # sql.ConnectTodb('85.239.52.190','testuser','testpasswd','test')
    # sql.ConnectTodb('localhost','root','123456','TESTDB')
    Load_Main_Window()

_flag=False
Main()