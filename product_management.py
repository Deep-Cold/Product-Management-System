import tkinter as tk
from tkinter import messagebox, ttk
import sqlconnect as sql
from copy import deepcopy

class Command:
    def __init__(self, action, data,addition=None):
        self.action = action
        self.data = data
        self.addition=addition

class ProductManagement:
    def __init__(self, root):
        self.root = root
        self.setup_toolbar()
        self.setup_treeview()
        self.products = []
        self.history = []
        self.sort_by = "ID"
        self.ascending = True
        self.bind_shortcuts()
        self.show_product_management()

    def setup_toolbar(self):
        self.toolbar_frame = tk.Frame(self.root)
        self.toolbar_frame.pack(fill='x', anchor='nw')

        self.add_button = tk.Button(self.toolbar_frame, text="Add", command=self.add_product)
        self.add_button.pack(side='left', padx=10, pady=5)

        self.remove_button = tk.Button(self.toolbar_frame, text="Remove", command=self.remove_selected_products)
        self.remove_button.pack(side='left', padx=10, pady=5)

        self.update_button = tk.Button(self.toolbar_frame, text="Update", command=self.update_product_shortcut)
        self.update_button.pack(side='left', padx=10, pady=5)

        self.filter_button = tk.Button(self.toolbar_frame, text="Filter", command=self.filter_product)
        self.filter_button.pack(side='left', padx=10, pady=5)

        self.sort_button = tk.Button(self.toolbar_frame, text="Sort", command=self.sort_products)
        self.sort_button.pack(side='left', padx=10, pady=5)

        self.undo_button = tk.Button(self.toolbar_frame, text="Undo", command=self.undo_last_action)
        self.undo_button.pack(side='left', padx=10, pady=5)

        self.select_all_button = tk.Button(self.toolbar_frame, text="Select All", command=self.select_all_products)
        self.select_all_button.pack(side='left', padx=10, pady=5)


    def setup_treeview(self):
        columns = ("ID", "Name", "Price($)", "Profit($)", "Quantities", "Supplier details")
        self.tree = ttk.Treeview(self.root, columns=columns, show='headings')
        for col in columns:
            self.tree.heading(col, text=col)
        self.tree.pack(fill='both', expand=True)
        self.tree.bind("<Button-3>", self.on_treeview_click)  
        self.tree.bind("<Button-1>", self.on_treeview_click_press)
        self.tree.bind("<B1-Motion>", self.on_treeview_click_drag)
        self.tree.bind("<ButtonRelease-1>", self.on_treeview_click_release)
    
    def bind_shortcuts(self):
        self.root.bind(f"<Control-z>", lambda event: self.undo_last_action())
        self.root.bind("<Delete>", lambda event: self.remove_selected_products())
        self.root.bind(f"<Control-n>", lambda event: self.add_product())
        self.root.bind(f"<Control-f>", lambda event: self.filter_product())

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
                popup_menu.add_command(label="Remove", command=lambda: self.remove_selected_products())
                popup_menu.tk_popup(event.x_root, event.y_root)
            else:
                if item_id:
                    event.widget.selection_set(item_id)
                    popup_menu = tk.Menu(self.root, tearoff=0)
                    popup_menu.add_command(label="Remove", command=lambda: self.remove_selected_products())
                    popup_menu.add_command(label="Update", command=lambda: self.update_product(item_id))
                    popup_menu.tk_popup(event.x_root, event.y_root)

    def show_product_management(self):
        self.products = sql.ShowAllProd()
        self.tree.delete(*self.tree.get_children())
        self.implement_sort()
        for product in self.products:
            self.tree.insert("", tk.END, values=product)
    
    def add_product(self):
        add_window = tk.Toplevel(self.root)
        add_window.title("Add Product")
        add_window.iconphoto(False,tk.PhotoImage(file="./Image/plus.png"))

        labels = ["ID", "Name", "Price($)", "Profit($)", "Quantities", "Supplier details"]
        entries = {}

        for i, label in enumerate(labels):
            tk.Label(add_window, text=label).grid(row=i, column=0, padx=10, pady=5)
            entry = tk.Entry(add_window)
            entry.grid(row=i, column=1, padx=10, pady=5)
            entries[label] = entry

        def submit_product():
            new_product = [str(entry.get()) for entry in entries.values()]
            pk=deepcopy(new_product)
            flag=sql.AddNewProd(pk)
            if flag:
                command = Command(action="add", data=new_product)
                self.history.append(command)
            else:
                messagebox.showerror("Error","Add Operation Fail")
            self.show_product_management()
            add_window.destroy()

        tk.Button(add_window, text="Cancel", command=add_window.destroy).grid(row=len(labels), column=0, padx=10, pady=10)
        tk.Button(add_window, text="Submit", command=submit_product).grid(row=len(labels), column=1, padx=10, pady=10)

    def remove_selected_products(self):
        if not self.tree.selection():
            return
        item_ids = self.tree.selection()
        confirmation = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete the selected product(s)?")
        if confirmation:
            products_details = []
            stk=[]
            for item_id in item_ids:
                product_details = self.tree.item(item_id)['values']
                tmp_list=sql.ShowSearchSale("name",'"'+product_details[1]+'"')
                for itm in tmp_list:
                    tmp=deepcopy(itm)
                    stk.append(tmp)
                    sql.DelSaleInfo(itm)
                product_details=sql.ShowSearchProd("id",int(product_details[0]))[0]
                products_details.append(product_details)
                sql.DeleteProd(product_details[0])
            command = Command(action="remove", data=products_details,addition=stk)
            self.history.append(command)
            self.show_product_management()

    def update_product_shortcut(self):
        item_ids = self.tree.selection()
        if len(item_ids) == 1:
            self.update_product(item_ids[0])
        else :
            messagebox.showinfo("Alarm","You can only choose ONE item")

    def update_product(self, item_id):
        selected_product = self.tree.item(item_id)['values']
        update_window = tk.Toplevel(self.root)
        update_window.title("Update Product")
        update_window.iconphoto(False,tk.PhotoImage(file="./Image/arrowup.png"))

        labels = ["ID", "Name", "Price($)", "Profit($)", "Quantities", "Supplier details"]
        entries = {}

        for i, label in enumerate(labels):
            tk.Label(update_window, text=label).grid(row=i, column=0, padx=10, pady=5)
            if label == "Name":
                entry = tk.Label(update_window, text=selected_product[1])
            elif label == "ID":
                entry = tk.Label(update_window, text=selected_product[0])
            else :
                entry = tk.Entry(update_window)
            entry.grid(row=i, column=1, padx=10, pady=5)
            if label != "Name" and label != "ID":
                entry.insert(0, selected_product[i])
            entries[label] = entry

        def submit_update():
            updated_product = deepcopy(selected_product)
            for i,entry in enumerate(entries.values()):
                if i > 1:
                    updated_product[i]=str(entry.get())
            flag=sql.UpdateProd(updated_product)
            if flag:
                command = Command(action="update", data=selected_product)
                self.history.append(command)
            else :
                messagebox.showerror("Error","Update Operation Fail")
            self.show_product_management()
            update_window.destroy()

        tk.Button(update_window, text="Cancel", command=update_window.destroy).grid(row=len(labels), column=0, padx=10, pady=10)
        tk.Button(update_window, text="Submit", command=submit_update).grid(row=len(labels), column=1, padx=10, pady=10)               
    
    def filter_product(self):
        filter_window = tk.Toplevel(self.root)
        filter_window.title("Filter Products")
        filter_window.iconphoto(False,tk.PhotoImage(file="./Image/filter.png"))

        labels = ["ID", "Name", "Price($)", "Profit($)", "Quantities", "Supplier details"]
        filter_entries = {}
        range_fields = {"Price($)", "Profit($)", "Quantities"}

        for i, label in enumerate(labels):
            tk.Label(filter_window, text=label).grid(row=i, column=0, padx=10, pady=5, sticky='w')

            if label in range_fields:
                range_frame = tk.Frame(filter_window)
                range_frame.grid(row=i, column=1, columnspan=4, sticky='w', padx=10, pady=5)

                from_entry = tk.Entry(range_frame, width=12)
                from_entry.pack(side='left', padx=3)

                tk.Label(range_frame, text='~').pack(side='left', padx=1)

                to_entry = tk.Entry(range_frame, width=12)
                to_entry.pack(side='left', padx=3)
                filter_entries[label] = (from_entry, to_entry)
            else:
                entry = tk.Entry(filter_window, width=15)
                entry.grid(row=i, column=1, columnspan=3, padx=10, pady=5, sticky='ew')
                filter_entries[label] = entry


        def submit_filter():
            try:
                filter_criteria = {}
                for label, entry in filter_entries.items():
                    if label in range_fields:
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
                apply_filters(self,filter_criteria)
            except ValueError:
                messagebox.showerror("Error","Filter Operation Fail")
            filter_window.destroy()

        tk.Button(filter_window, text="Filter", command=submit_filter).grid(row=len(labels), column=2, padx=10, pady=10)

        def apply_filters(self, criteria):
            self.products = []
            cur_itm = sql.ShowAllProd()
            for product in cur_itm:
                match = True
                for i, label in enumerate(labels):
                    if label not in criteria.keys():
                        continue
                    filter_criteria = criteria[label]
                    if label in range_fields:
                        try:
                            product_value = float(product[i])
                            if not filter_criteria[0] <= product_value <= filter_criteria[1]:
                                match = False
                                break
                        except ValueError:
                            match = False
                            break
                    elif i:
                        if filter_criteria.lower() not in product[i].lower():
                            match = False
                            break
                    else:
                        if product[i] != int(filter_criteria):
                            match = False
                            break
                if match:
                    self.products.append(product)
            self.implement_sort()
            self.tree.delete(*self.tree.get_children())
            for product in self.products:
                self.tree.insert("", tk.END, values=product)

    def implement_sort(self):
        sort_options = ["ID", "Name", "Price($)", "Profit($)", "Quantities", "Supplier details"]
        self.products.sort(key=lambda x: x[sort_options.index(self.sort_by)], reverse=not self.ascending)

    def sort_products(self):
        sort_window = tk.Toplevel(self.root)
        sort_window.title("Sort Products")
        sort_window.iconphoto(False,tk.PhotoImage(file="./Image/sort-ascending.png"))

        sort_options = ["ID", "Name", "Price($)", "Profit($)", "Quantities", "Supplier details"]
        sort_var = tk.StringVar(sort_window)
        sort_var.set(self.sort_by)  

        tk.Label(sort_window, text="Sort by").pack(side="left", padx=10, pady=10)
        sort_menu = tk.OptionMenu(sort_window, sort_var, *sort_options)
        sort_menu.pack(side="left", padx=10, pady=10)

        order_var = tk.BooleanVar(sort_window)
        order_var.set(self.ascending)  
        tk.Radiobutton(sort_window, text="Ascending", variable=order_var, value=True).pack(side="left", padx=10, pady=10)
        tk.Radiobutton(sort_window, text="Descending", variable=order_var, value=False).pack(side="left", padx=10, pady=10)

        def submit_sort():
            self.sort_by = sort_var.get()
            self.ascending = order_var.get()
            self.show_product_management()
            sort_window.destroy()

        tk.Button(sort_window, text="Sort", command=submit_sort).pack(side="right", padx=10, pady=10)

    def undo_last_action(self):
        if self.history:
            last_command = self.history.pop()
            if last_command.action == "add":
                sql.DeleteProd(int(last_command.data[0]))
            elif last_command.action == "remove":
                for product_to_add_back in last_command.data:
                    sql.AddNewProd(product_to_add_back)
                for itm in last_command.addition:
                    sql.AddSaleInfo(itm)
            elif last_command.action == "update":
                sql.UpdateProd(last_command.data)
            self.show_product_management()

    def select_all_products(self):
        self.tree.selection_set(self.tree.get_children())