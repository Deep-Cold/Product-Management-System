import tkinter as tk
from tkinter import messagebox,ttk
import sqlconnect as sql
from copy import deepcopy

class Command:
    def __init__(self,action,data,addition=None):
        self.action=action
        self.data=data
        self.addition=addition

class Sales_Tracking:
    def __init__(self,root):
        self.root=root
        self.Toolbar()
        self.Treeview()
        self.labels=["ID","Name","Quantities","Client","Date"]
        self.messages=[]
        self.history=[]
        self.sort_by="ID"
        self.ascending=True
        self.Shortcuts()
        self.Show()
    def Toolbar(self):
        self.toolbar_frame = tk.Frame(self.root)
        self.toolbar_frame.pack(fill='x', anchor='nw')
        self.add_button = tk.Button(self.toolbar_frame, text="Add", command=self.Add)
        self.add_button.pack(side='left', padx=10, pady=5)
        self.remove_button = tk.Button(self.toolbar_frame, text="Remove", command=self.Remove)
        self.remove_button.pack(side='left', padx=10, pady=5)
        self.update_button = tk.Button(self.toolbar_frame, text="Update", command=self.Update_Shortcut)
        self.update_button.pack(side='left', padx=10, pady=5)
        self.filter_button = tk.Button(self.toolbar_frame, text="Filter", command=self.Filter)
        self.filter_button.pack(side='left', padx=10, pady=5)
        self.sort_button = tk.Button(self.toolbar_frame, text="Sort", command=self.Sort)
        self.sort_button.pack(side='left', padx=10, pady=5)
        self.undo_button = tk.Button(self.toolbar_frame, text="Undo", command=self.Undo)
        self.undo_button.pack(side='left', padx=10, pady=5)
        self.select_all_button = tk.Button(self.toolbar_frame, text="Select All", command=self.Select_All)
        self.select_all_button.pack(side='left', padx=10, pady=5)
    def Treeview(self):
        columns=("ID","Name","Quantities","Client","Date")
        self.tree = ttk.Treeview(self.root, columns=columns, show='headings')
        for col in columns:
            self.tree.heading(col, text=col)
        self.tree.pack(fill='both', expand=True)
        self.tree.bind("<Button-3>", self.on_treeview_click)  
        self.tree.bind("<Button-1>", self.on_treeview_click_press)
        self.tree.bind("<B1-Motion>", self.on_treeview_click_drag)
        self.tree.bind("<ButtonRelease-1>", self.on_treeview_click_release)
    def Shortcuts(self):
        self.root.bind(f"<Control-z>", lambda event: self.Undo())
        self.root.bind("<Delete>", lambda event: self.Remove())
        self.root.bind(f"<Control-n>", lambda event: self.Add())
        self.root.bind(f"<Control-f>", lambda event: self.Filter())
    def on_treeview_click_press(self, event):
        self.dragging = True
        self.tree.selection_remove(self.tree.selection())
    def on_treeview_click_drag(self, event):
        if self.dragging:
            row_id = self.tree.identify_row(event.y)
            if row_id:
                self.tree.selection_add(row_id)
    def on_treeview_click_release(self, event):
        self.dragging = False
    def on_treeview_click(self, event):
        region = event.widget.identify_region(event.x, event.y)
        item_id = event.widget.identify_row(event.y)
        if region == "cell" or region == "tree":
            if len(self.tree.selection()) > 1:  
                popup_menu = tk.Menu(self.root, tearoff=0)
                popup_menu.add_command(label="Remove", command=lambda: self.Remove())
                popup_menu.tk_popup(event.x_root, event.y_root)
            else:
                if item_id:
                    event.widget.selection_set(item_id)
                    popup_menu = tk.Menu(self.root, tearoff=0)
                    popup_menu.add_command(label="Remove", command=lambda: self.Remove())
                    popup_menu.add_command(label="Update", command=lambda: self.Update(item_id))
                    popup_menu.tk_popup(event.x_root, event.y_root)
    def Show(self):
        self.messages = sql.ShowAllSale()
        self.tree.delete(*self.tree.get_children())
        self.Sort_Launch()
        for items in self.messages:
            self.tree.insert("", tk.END, values=items)
    def Add(self):
        add_window = tk.Toplevel(self.root)
        add_window.title("Add Sale Info")
        add_window.iconphoto(False,tk.PhotoImage(file="./Image/plus.png"))
        entries={}
        for i,label in enumerate(self.labels):
            tk.Label(add_window, text=label).grid(row=i, column=0, padx=10, pady=5)
            entry = tk.Entry(add_window)
            entry.grid(row=i, column=1, padx=10, pady=5)
            entries[label] = entry
        def Submit():
            nw = [str(entry.get()) for entry in entries.values()]
            pk=deepcopy(nw)
            flag=sql.AddSaleInfo(pk)
            if flag:
                command = Command(action="add", data=nw)
                self.history.append(command)
            else:
                messagebox.showerror("Error","Add Operation Fail")
            self.Show()
            add_window.destroy()
        tk.Button(add_window, text="Cancel", command=add_window.destroy).grid(row=len(self.labels), column=0, padx=10, pady=10)
        tk.Button(add_window, text="Submit", command=Submit).grid(row=len(self.labels), column=1, padx=10, pady=10)
    def Remove(self):
        if not self.tree.selection():
            return
        tot=self.tree.selection()
        confirmation = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete the selected sale(s)?")
        if confirmation:
            sales_details = []
            for id in tot:
                sale_details = self.tree.item(id)['values']
                pk=deepcopy(sale_details)
                sales_details.append(pk)
                sql.DelSaleInfo(sale_details)
            command = Command(action="remove", data=sales_details)
            self.history.append(command)
            self.Show()
    def Update_Shortcut(self):
        item_ids = self.tree.selection()
        if len(item_ids) == 1:
            self.Update(item_ids[0])
        else :
            messagebox.showinfo("Alarm","You can only choose ONE item")
    def Update(self,id):
        item = self.tree.item(id)['values']
        update_window = tk.Toplevel(self.root)
        update_window.title("Update Sale Info")
        update_window.iconphoto(False,tk.PhotoImage(file="./Image/arrowup.png"))
        entries = {}
        for i, label in enumerate(self.labels):
            tk.Label(update_window, text=label).grid(row=i, column=0, padx=10, pady=5)
            if label == "Name":
                entry = tk.Label(update_window, text=item[1])
            elif label == "ID":
                entry = tk.Label(update_window,text=item[0])
            else :
                entry = tk.Entry(update_window)
            entry.grid(row=i, column=1, padx=10, pady=5)
            if label != "Name" and label != "ID":
                entry.insert(0, item[i])
            entries[label] = entry
        def Submit():
            updated = deepcopy(item)
            for i,entry in enumerate(entries.values()):
                if i > 1:
                    updated[i]=str(entry.get())
            pk=deepcopy(item)
            sql.DelSaleInfo(pk)
            pk=deepcopy(updated)
            flag=sql.AddSaleInfo(pk)
            if flag:
                command = Command(action="update", data=item , addition=updated)
                self.history.append(command)
            else :
                sql.AddSaleInfo(item)
                messagebox.showerror("Error","Update Operation Fail")
            self.Show()
            update_window.destroy()
        tk.Button(update_window, text="Cancel", command=update_window.destroy).grid(row=len(self.labels), column=0, padx=10, pady=10)
        tk.Button(update_window, text="Submit", command=Submit).grid(row=len(self.labels), column=1, padx=10, pady=10)               
    def Filter(self):
        filter_window = tk.Toplevel(self.root)
        filter_window.title("Filter Sales")
        filter_window.iconphoto(False,tk.PhotoImage(file="./Image/filter.png"))
        entries={}
        for i, label in enumerate(self.labels):
            tk.Label(filter_window, text=label).grid(row=i, column=0, padx=10, pady=5, sticky='w')
            if label == "Quantities":
                range_frame = tk.Frame(filter_window)
                range_frame.grid(row=i, column=1, columnspan=4, sticky='w', padx=10, pady=5)
                from_entry = tk.Entry(range_frame, width=12)
                from_entry.pack(side='left', padx=3)
                tk.Label(range_frame, text='~').pack(side='left', padx=1)
                to_entry = tk.Entry(range_frame, width=12)
                to_entry.pack(side='left', padx=3)
                entries[label] = (from_entry, to_entry)
            else:
                entry = tk.Entry(filter_window, width=15)
                entry.grid(row=i, column=1, columnspan=3, padx=10, pady=5, sticky='ew')
                entries[label] = entry
        def Submit():
            try:
                filter_criteria = {}
                for label, entry in entries.items():
                    if label == "Quantities":
                        from_value, to_value = entry[0].get(), entry[1].get()
                        if (from_value, to_value) != ("",""):
                            if not from_value:
                                from_value=float("-inf")
                            else:
                                from_value=float(from_value)
                            if not to_value:
                                to_value=float("inf")
                            else:
                                to_value=float(to_value)
                            filter_criteria[label] = (from_value, to_value)
                    else :
                        val = entry.get()
                        if val :
                            filter_criteria[label] = entry.get()
                Apply(self,filter_criteria)
            except ValueError:
                messagebox.showerror("Error","Filter Operation Fail")
            filter_window.destroy()
        tk.Button(filter_window, text="Filter", command=Submit).grid(row=len(self.labels), column=2, padx=10, pady=10)
        def Apply(self,criteria):
            self.messages=[]
            cur_itm = sql.ShowAllSale()
            for itm in cur_itm:
                match = True
                for i, label in enumerate(self.labels):
                    if label not in criteria.keys():
                        continue
                    filter_criteria = criteria[label]
                    if label == "Quantities":
                        try:
                            itm_value = float(itm[i])
                            if not filter_criteria[0] <= itm_value <= filter_criteria[1]:
                                match = False
                                break
                        except ValueError:
                            match = False
                            break
                    elif i:
                        if filter_criteria.lower() not in itm[i].lower():
                            match = False
                            break
                    else:
                        if itm[i] != int(filter_criteria):
                            match = False
                            break
                if match:
                    self.messages.append(itm)
            self.Sort_Launch()
            self.tree.delete(*self.tree.get_children())
            for itm in self.messages:
                self.tree.insert("", tk.END, values=itm)
    def Sort_Launch(self):
        self.messages.sort(key=lambda x: x[self.labels.index(self.sort_by)], reverse=not self.ascending)
    def Sort(self):
        sort_window = tk.Toplevel(self.root)
        sort_window.title("Sort Sales")
        sort_window.iconphoto(False,tk.PhotoImage(file="./Image/sort-ascending.png"))
        sort_var = tk.StringVar(sort_window)
        sort_var.set(self.sort_by)
        tk.Label(sort_window, text="Sort by").pack(side="left", padx=10, pady=10)
        sort_menu = tk.OptionMenu(sort_window, sort_var, *self.labels)
        sort_menu.pack(side="left", padx=10, pady=10)
        order_var = tk.BooleanVar(sort_window)
        order_var.set(self.ascending)  
        tk.Radiobutton(sort_window, text="Ascending", variable=order_var, value=True).pack(side="left", padx=10, pady=10)
        tk.Radiobutton(sort_window, text="Descending", variable=order_var, value=False).pack(side="left", padx=10, pady=10)
        def Submit():
            self.sort_by = sort_var.get()
            self.ascending = order_var.get()
            self.Show()
            sort_window.destroy()
        tk.Button(sort_window, text="Sort", command=Submit).pack(side="right", padx=10, pady=10)
    def Undo(self):
        if self.history:
            last_command = self.history.pop()
            if last_command.action == "add":
                sql.DelSaleInfo(last_command.data)
            elif last_command.action == "remove":
                for itm_to_add_back in last_command.data:
                    sql.AddSaleInfo(itm_to_add_back)
            elif last_command.action == "update":
                sql.DelSaleInfo(last_command.addition)
                sql.AddSaleInfo(last_command.data)
            self.Show()
    def Select_All(self):
        self.tree.selection_set(self.tree.get_children())