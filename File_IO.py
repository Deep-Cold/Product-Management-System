from tkinter import messagebox
import tkinter as tk
from tkinter import filedialog
import sqlconnect as sql
from fpdf import FPDF

class FileIO:
    def __init__(self,root):
        self.root=root
        self.root.minsize(600, 400)
        self.Set_Button()
        self.ProdLabel=["ID", "Name", "Price($)", "Profit($)", "Quantities", "Supplier details"]
        self.SalesLabel=["ID","Name","Quantities","Client","Date","Profit($)"]
    def Set_Button(self):
        for i in range(4):
            self.root.grid_rowconfigure(i, weight=1)
            self.root.grid_columnconfigure(0, weight=1)
        buttons = {
            "Inventory Report": self.Inv_Rep,
            "Sales Report": self.Sal_Rep,
            "Import Products Information": self.Imp_Prod,
            "Import Sales Information": self.Imp_Sal
        }
        for i, (button_name, action) in enumerate(buttons.items()):
            button = tk.Button(self.root, text=button_name, command=action)
            button.grid(row=i, column=0, sticky="nsew", padx=50, pady=10)
    def Inv_Rep(self):
        lst=sql.ShowAllProd()
        _path=filedialog.askdirectory(initialdir="./",title="Select A Folder")
        if not _path:
            messagebox.showerror("Error","Export Fail")
            return
        _file=FPDF()
        _file.add_page()
        _file.set_font("Times", size=16)
        with _file.table() as table:
            row=table.row()
            for data in self.ProdLabel:
                row.cell(data)
            for i in lst:
                row=table.row()
                for data in i:
                    row.cell(str(data))
        _path+="/Inventory Report.pdf"
        _file.output(_path)
        messagebox.showinfo("Remind","Export Succeed")
    def Sal_Rep(self):
        lst=sql.ShowAllSale()
        _path=filedialog.askdirectory(initialdir="./",title="Select A Folder")
        if not _path:
            messagebox.showerror("Error","Export Fail")
            return
        _file=FPDF()
        _file.add_page()
        _file.set_font("Times", size=16)
        for i in lst:
            tmp_list=sql.ShowSearchProd("name",'"'+str(i[1])+'"')
            i.append(tmp_list[0][3]*i[2])
        with _file.table() as table:
            row=table.row()
            for data in self.SalesLabel:
                row.cell(data)
            for i in lst:
                row=table.row()
                for data in i:
                    row.cell(str(data))
        _path+="/Sales Report.pdf"
        _file.output(_path)
        messagebox.showinfo("Remind","Export Succeed")
    def Imp_Prod(self):
        try:
            _file=open(filedialog.askopenfilename(initialdir='./',title="Select A File",filetypes=(("txt files","*.txt"),)),"r")
        except:
            messagebox.showerror("Error","Import Fail")
            return
        lst=_file.readlines()
        fil,suc=0,0
        for i in lst:
            seq=i.split(sep=',')
            if len(seq) != 6:
                fil+=1
                continue
            flag=sql.AddNewProd(seq)
            if flag:
                suc+=1
            else:
                fil+=1
        messagebox.showinfo("Remind",f"Import {suc} Line(s) Succeed, {fil} Line(s) Fail")
        
    def Imp_Sal(self):
        try:
            _file=open(filedialog.askopenfilename(initialdir='./',title="Select A File",filetypes=(("txt files","*.txt"),)),"r")
        except:
            messagebox.showerror("Error","Import Fail")
            return
        lst=_file.readlines()
        fil,suc=0,0
        for i in lst:
            seq=i.split(sep=',')
            if len(seq) != 5:
                fil+=1
                continue
            flag=sql.AddSaleInfo(seq)
            if flag:
                suc+=1
            else:
                fil+=1
        messagebox.showinfo("Remind",f"Import {suc} Line(s) Succeed, {fil} Line(s) Fail")