from tkinter import * 
import tkinter.ttk as ttk
from tkinter import messagebox
import psycopg2
from constants import *

class AllProdDash:
    def __init__(self, window):
        self.window = window
        self.window.geometry("1366x720+0+0")
        self.main_black_color = '#0f0f0f'
        self.main_white_color = '#f8f8f8'
        self.window['bg'] = self.main_black_color
        self.window.title("Product List Dashboard")
        # self.window.iconbitmap("")
        self.window.resizable(False, False)

        # Defining Variable
        self.var_search_by = StringVar()
        self.var_search_by_val = StringVar()

        self.var_pr_id = IntVar()
        self.var_pr_name = StringVar()
        self.var_stocks = IntVar()
        self.var_cost_price= DoubleVar()
        self.var_sell_price = DoubleVar()
        self.var_cgst = DoubleVar()
        self.var_sgst = DoubleVar()
        self.var_ven_name = StringVar()
        self.var_ven_num = StringVar()
        self.var_pur_mode = StringVar()
        
        # Setting some of the values 
        self.var_stocks.set(1)
        self.var_cgst.set(9.0)
        self.var_sgst.set(9.0)

        # Prod List Dashboard Text 
        admin_dash_text = Label(window, text='Product List Dashboard',font=("Roboto Regular", 36), fg=self.main_white_color,bg=self.main_black_color)
        admin_dash_text.place(x=0,y=0)

        # Frame Search 
        self.search_frame = Frame(self.window, bd=2, relief=RIDGE)
        self.search_frame.place(x=550, y=5, height=50, width=810)

        self.search_combo_select = ttk.Combobox(self.search_frame,
                                values=("Select By","Product Id","Product Name", "Vendor Name", "Vendor Number", "Stocks Availability"),
                                state='readonly', justify=CENTER,
                                font=('Roboto Regular', 14, "normal"),
                                textvariable=self.var_search_by
                                )
        # self.search_combo_select.place(x=10, y=10, width=180)
        self.search_combo_select.grid(row=0, column=0,padx=40,pady=10)
        self.search_combo_select.current(0)

        self.search_txt_entry = Entry(self.search_frame,relief=SUNKEN, bg="white", fg="#6b6a69",
                                        textvariable=self.var_search_by_val,font=("yu gothic ui semibold", 12))
        self.search_txt_entry.grid(row=0,column=1,padx=0,pady=10)

        self.search_btn_search =Button(self.search_frame, text='Search',
                                cursor='hand2',fg=self.main_white_color,
                                command=self.search_prod_fun,                   
                                bg=self.main_black_color, font=('Roboto Regular', 14, "normal"),width=12)
        self.search_btn_search.grid(row=0, column=2,padx=20)

        self.show_all_btn_search =Button(self.search_frame, text='Show All',
                                cursor='hand2',fg=self.main_white_color,
                                command=self.show_prod_fun,                   
                                bg=self.main_black_color, font=('Roboto Regular', 14, "normal"),width=12)
        self.show_all_btn_search.grid(row=0, column=3,padx=0)

        # Frame 
        self.frame_for_tree = Frame(self.window, bd=2, relief=RIDGE)
        self.frame_for_tree.place(x=10, y=60,relwidth=1, height=340)

        self.scrolly = Scrollbar(self.frame_for_tree, orient=VERTICAL)
        self.scrollx = Scrollbar(self.frame_for_tree, orient=HORIZONTAL)
        #Treeview
        self.main_list_tree = ttk.Treeview(self.frame_for_tree,
                columns=("pr_id","pr_name","stocks","cost_price","sell_price","c_gst","s_gst","ven_name", "ven_num", "ven_purchase_mode"), show='headings', yscrollcommand=self.scrolly.set, xscrollcommand=self.scrollx.set )

        self.main_list_tree['selectmode'] = 'browse'

        self.scrolly.pack(side=RIGHT, fill=Y)
        self.scrollx.pack(side=BOTTOM, fill=X)

        self.scrolly.config(command=self.main_list_tree.yview)
        self.scrollx.config(command=self.main_list_tree.xview)

        self.main_list_tree.heading('pr_id', text="Pr Id")
        self.main_list_tree.heading('pr_name', text="Product Name")
        self.main_list_tree.heading('stocks', text="Stocks")
        self.main_list_tree.heading('cost_price', text="Cost Price")
        self.main_list_tree.heading('sell_price', text="Sell Price")
        self.main_list_tree.heading('c_gst', text="CGST")
        self.main_list_tree.heading('s_gst', text="SGST")
        self.main_list_tree.heading('ven_name', text="Vendor Name")
        self.main_list_tree.heading('ven_num', text="Vendor Number")
        self.main_list_tree.heading('ven_purchase_mode', text="Purchase Mode")
        
        self.main_list_tree.pack(fill=BOTH, expand=1)

        self.main_list_tree.column('pr_id', width=100)
        self.main_list_tree.column('pr_name', width=100)
        self.main_list_tree.column('stocks',width=100)
        self.main_list_tree.column('cost_price', width=100)
        self.main_list_tree.column('sell_price', width=100)
        self.main_list_tree.column('c_gst', width=20)
        self.main_list_tree.column('s_gst', width=20)
        self.main_list_tree.column('ven_name',width=100)
        self.main_list_tree.column('ven_num',width=100)
        self.main_list_tree.column('ven_purchase_mode',width=100)

        self.main_list_tree.bind("<ButtonRelease-1>", self.get_data_fun)
        self.show_prod_fun()
        # UPDATE Products 

        self.frame_for_update = Frame(self.window, bd=2, relief=RIDGE)
        self.frame_for_update.place(x=10, y=420,relwidth=1, height=280)

        # ============================Product Id====================================
        prod_id_label = Label(self.frame_for_update, text="Product Id: ", bg="white", fg="#4f4e4d",
                                    font=("yu gothic ui", 13, "bold"))
        prod_id_label.grid(row=0,column=0,padx=40,pady=20)

        self.prod_id_entry = Entry(self.frame_for_update,relief=SUNKEN, bg="white", fg="#6b6a69",
                                    font=("yu gothic ui semibold", 12),
                                    textvariable=self.var_pr_id)
        self.prod_id_entry.grid(row=0,column=1,padx=0,pady=20)

        # ============================Product Name====================================
        prod_name_label = Label(self.frame_for_update, text="Product Name: ", bg="white", fg="#4f4e4d",
                                    font=("yu gothic ui", 13, "bold"))
        prod_name_label.grid(row=0,column=2,padx=40,pady=20)

        self.prod_name_entry = Entry(self.frame_for_update,relief=SUNKEN, bg="white", fg="#6b6a69",
                                    font=("yu gothic ui semibold", 12),textvariable=self.var_pr_name)
        self.prod_name_entry.grid(row=0,column=3,padx=0,pady=20)

        # ============================Product Stocks====================================
        prod_stock_label = Label(self.frame_for_update, text="Product Stocks: ", bg="white", fg="#4f4e4d",
                                    font=("yu gothic ui", 13, "bold"))
        prod_stock_label.grid(row=0,column=4,padx=40,pady=20)

        self.prod_stock_entry = Entry(self.frame_for_update, relief=SUNKEN, bg="white", fg="#6b6a69",
                                    font=("yu gothic ui semibold", 12),textvariable=self.var_stocks)
        self.prod_stock_entry.grid(row=0,column=5,padx=0,pady=20)

        # ============================Cost Price====================================
        cost_price_label = Label(self.frame_for_update, text="Cost Price: ", bg="white", fg="#4f4e4d",
                                    font=("yu gothic ui", 13, "bold"))
        cost_price_label.grid(row=1,column=0,padx=40,pady=20)

        self.cost_price_entry = Entry(self.frame_for_update, relief=SUNKEN, bg="white", fg="#6b6a69",
                                    font=("yu gothic ui semibold", 12),textvariable=self.var_cost_price)
        self.cost_price_entry.grid(row=1,column=1,padx=0,pady=20)

        # ============================Selling Price====================================
        sell_price_label = Label(self.frame_for_update, text="Selling Price: ", bg="white", fg="#4f4e4d",
                                    font=("yu gothic ui", 13, "bold"))
        sell_price_label.grid(row=1,column=2,padx=40,pady=20)

        self.sell_price_entry = Entry(self.frame_for_update, relief=SUNKEN, bg="white", fg="#6b6a69",
                                    font=("yu gothic ui semibold", 12),textvariable=self.var_sell_price)
        self.sell_price_entry.grid(row=1,column=3,padx=0,pady=20)

        # ============================CGST====================================
        self.cgst_label = Label(self.frame_for_update, text="CGST: ", bg="white", fg="#4f4e4d",
                                    font=("yu gothic ui", 13, "bold"))
        self.cgst_label.grid(row=1,column=4,padx=40,pady=20)

        self.cgst_entry = Entry(self.frame_for_update, relief=SUNKEN, bg="white", fg="#6b6a69",
                                    font=("yu gothic ui semibold", 12),textvariable=self.var_cgst)
        self.cgst_entry.grid(row=1,column=5,padx=0,pady=20)

        # ============================SGST====================================
        self.sgst_label = Label(self.frame_for_update, text="SGST: ", bg="white", fg="#4f4e4d",
                                    font=("yu gothic ui", 13, "bold"))
        self.sgst_label.grid(row=2,column=0,padx=40,pady=20)

        self.sgst_entry = Entry(self.frame_for_update, relief=SUNKEN, bg="white", fg="#6b6a69",
                                    font=("yu gothic ui semibold", 12),textvariable=self.var_sgst)
        self.sgst_entry.grid(row=2,column=1,padx=0,pady=20)

        # ============================Vendor Name====================================
        self.prod_stock_label = Label(self.frame_for_update, text="Vendor Name: ", bg="white", fg="#4f4e4d",
                                    font=("yu gothic ui", 13, "bold"))
        self.prod_stock_label.grid(row=2,column=2,padx=40,pady=20)

        self.prod_stock_entry = Entry(self.frame_for_update, relief=SUNKEN, bg="white", fg="#6b6a69",
                                    font=("yu gothic ui semibold", 12),textvariable=self.var_ven_name)
        self.prod_stock_entry.grid(row=2,column=3,padx=0,pady=20)
        # ============================Vendor Number====================================
        self.prod_stock_label = Label(self.frame_for_update, text="Vendor Number: ", bg="white", fg="#4f4e4d",
                                    font=("yu gothic ui", 13, "bold"))
        self.prod_stock_label.grid(row=2,column=4,padx=40,pady=20)

        self.prod_stock_entry = Entry(self.frame_for_update, relief=SUNKEN, bg="white", fg="#6b6a69",
                                    font=("yu gothic ui semibold", 12),textvariable=self.var_ven_num)
        self.prod_stock_entry.grid(row=2,column=5,padx=0,pady=20)

        # ============================Purchase Mode====================================
        self.pur_mode_label = Label(self.frame_for_update, text="Pur Mode: ", bg="white", fg="#4f4e4d",
                                    font=("yu gothic ui", 13, "bold"))
        self.pur_mode_label.grid(row=3,column=0,padx=40,pady=20)

        self.pur_mode_entry = Entry(self.frame_for_update, relief=SUNKEN, bg="white", fg="#6b6a69",
                                    font=("yu gothic ui semibold", 12),textvariable=self.var_pur_mode)
        self.pur_mode_entry.grid(row=3,column=1,padx=0,pady=20)

        # ============================Buttons Lot of Buttons ============================
        self.save_prod_btn = Button(self.frame_for_update, text='Save',
                            cursor='hand2',fg=self.main_white_color,
                            command=self.add_prod_fun,                   
                            bg=self.main_black_color, font=('Roboto Regular', 14, "normal"))
        self.save_prod_btn.place(x=450, y=220, width=120,height=40)

        self.update_prod_btn = Button(self.frame_for_update, text='Update',
                                cursor='hand2',fg=self.main_white_color,   
                                command=self.upd_prod_fun,                
                                bg=self.main_black_color, font=('Roboto Regular', 14, "normal"))
        self.update_prod_btn.place(x=600, y=220, width=120,height=40)

        self.del_prod_btn = Button(self.frame_for_update, text='Delete',
                                cursor='hand2',fg=self.main_white_color,  
                                command=self.del_prod_fun,                 
                                bg=self.main_black_color, font=('Roboto Regular', 14, "normal"))
        self.del_prod_btn.place(x=750, y=220, width=120,height=40)

        self.clear_prod_btn = Button(self.frame_for_update, text='Clear',
                                cursor='hand2',fg=self.main_white_color,
                                command=self.clear_prod_fun,                   
                                bg=self.main_black_color, font=('Roboto Regular', 14, "normal"))
        self.clear_prod_btn.place(x=900, y=220, width=120,height=40)

        self.dashboard_btn = Button(self.frame_for_update, text='Dashboard',
                                cursor='hand2',fg=self.main_white_color,
                                command=self.go_to_dashboard_func,                   
                                bg=self.main_black_color, font=('Roboto Regular', 14, "normal"))
        self.dashboard_btn.place(x=1050, y=220, width=120,height=40)
        
    def add_prod_fun(self):
        con = psycopg2.connect(host=DB_HOST,database=DB_NAME, user=DB_USER, password=DB_PASS)
        cur = con.cursor()
        try:
            if self.var_pr_name.get() == '':
                messagebox.showerror('Empty Value', "Value could not be empty", parent=self.window)
            else:
                cur.execute("""
                INSERT INTO inventory (id, pr_name, stocks,cost_price, sell_price, c_gst,s_gst, ven_name, ven_num,ven_purchase_mode)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """, (
                    self.var_pr_id.get(),
                    self.var_pr_name.get().capitalize(),
                    self.var_stocks.get(),
                    float(self.var_cost_price.get()),
                    float(self.var_sell_price.get()),
                    float(self.var_cgst.get()),
                    float(self.var_sgst.get()),
                    self.var_ven_name.get().capitalize(),
                    self.var_ven_num.get(),
                    self.var_pur_mode.get()
                    )
                )
                con.commit()
            
            messagebox.showinfo('Success', f'{self.var_pr_name.get().capitalize()} has been added', parent=self.window)
            self.clear_prod_fun()
            self.show_prod_fun()

        except Exception as ex:
            messagebox.showerror('Error', f'Error due to {str(ex)}', parent=self.window)

    def show_prod_fun(self):
        con = psycopg2.connect(host=DB_HOST,database=DB_NAME, user=DB_USER, password=DB_PASS)
        cur = con.cursor()
        try:
            cur.execute('SELECT * FROM inventory')
            rows_db = cur.fetchall()
            self.main_list_tree.delete(*self.main_list_tree.get_children())
            for row in rows_db:
                self.main_list_tree.insert('', END, values=row)

        except Exception as ex:
            messagebox.showerror('Error', f'Error due to {str(ex)}', parent=self.window)

    def get_data_fun(self, ev):
        f = self.main_list_tree.focus()
        content = (self.main_list_tree.item(f))
        row = content['values']
        self.var_pr_id.set(row[0])
        self.var_pr_name.set(row[1])
        self.var_stocks.set(row[2])
        self.var_cost_price.set(row[3])
        self.var_sell_price.set(row[4])
        self.var_cgst.set(row[5])
        self.var_sgst.set(row[6])
        self.var_ven_name.set(row[7])
        self.var_ven_num.set(row[8])
        self.var_pur_mode.set(row[9])

    def upd_prod_fun(self):
        con = psycopg2.connect(host=DB_HOST,database=DB_NAME, user=DB_USER, password=DB_PASS)
        cur = con.cursor()
        try:
            if self.var_pr_id.get() =='0' or self.var_pr_name.get() == '':
                messagebox.showerror('Empty Value', "Value could not be empty", parent=self.window)
            else:
                cur.execute('SELECT * FROM inventory where id=%s', (self.var_pr_id.get(),))
                row_db = cur.fetchone()
                if row_db == None:
                    messagebox.showerror('Error', f'Invalid Product ID.', parent=self.window)
                else:
                    cur.execute("""
                        UPDATE inventory SET 
                        pr_name=%s,
                        stocks=%s,
                        cost_price=%s,
                        sell_price=%s,
                        c_gst=%s,
                        s_gst=%s,
                        ven_name=%s,
                        ven_num=%s,
                        ven_purchase_mode=%s
                        WHERE id = %s
                        """, (
                            self.var_pr_name.get().capitalize(),
                            int(self.var_stocks.get()),
                            float(self.var_cost_price.get()),
                            float(self.var_sell_price.get()),
                            float(self.var_cgst.get()),
                            float(self.var_sgst.get()),
                            self.var_ven_name.get().capitalize(),
                            self.var_ven_num.get(),
                            self.var_pur_mode.get(),
                            int(self.var_pr_id.get())
                            )
                        )
                    con.commit()
                
                messagebox.showinfo('Success', f'Product has been updated.', parent=self.window)
                self.clear_prod_fun()
                self.show_prod_fun()

        except Exception as ex:
            messagebox.showerror('Error', f'Error due to {str(ex)}', parent=self.window)

    def del_prod_fun(self):
        con = psycopg2.connect(host=DB_HOST,database=DB_NAME, user=DB_USER, password=DB_PASS)
        cur = con.cursor()
        try:
            cur.execute('SELECT * FROM inventory where id=%s', (self.var_pr_id.get(),))
            row_db = cur.fetchone()
            if row_db == None:
                messagebox.showerror('Error', f'Invalid Product ID.', parent=self.window)
            else:
                yes_no = messagebox.askyesno('Are you Sure?', f'Sure to Delete {self.var_pr_name.get().capitalize()} of Id {self.var_pr_id.get()}?', parent=self.window)
                if yes_no:
                    cur.execute("DELETE FROM inventory where id=%s",(self.var_pr_id.get(),))
                    con.commit()
                    self.clear_prod_fun()
                    self.show_prod_fun()
                else:
                    messagebox.showinfo('Not deleted', f'{self.var_pr_name.get().capitalize()} is not deleted :)', parent=self.window)
                    self.show_prod_fun()
                
        except Exception as ex:
            messagebox.showerror('Error', f'Error due to {str(ex)}', parent=self.window)


    def clear_prod_fun(self):
        self.var_pr_id.set(0),
        self.var_pr_name.set(''),
        self.var_stocks.set(1),
        self.var_cost_price.set(0.0),
        self.var_sell_price.set(0.0),
        self.var_cgst.set(9.0),
        self.var_sgst.set(9.0),
        self.var_ven_name.set(''),
        self.var_ven_num.set('')
        self.var_pur_mode.set('')
        self.var_search_by.set('Select By')
        self.var_search_by_val.set('')
        self.deselect_tree_item(self.main_list_tree)

    def search_prod_fun(self):
        con = psycopg2.connect(host=DB_HOST,database=DB_NAME, user=DB_USER, password=DB_PASS)
        cur = con.cursor()
        try:
            if self.var_search_by.get()=='Select By':
                messagebox.showwarning('Please Select', "Select an option", parent=self.window)
            elif self.var_search_by.get()=='Product Id':
                cur.execute('SELECT * FROM inventory WHERE id=%s', (self.var_search_by_val.get(),))
                rows_db = cur.fetchall()
                if rows_db!=[]:
                    self.main_list_tree.delete(*self.main_list_tree.get_children())
                    for row in rows_db:
                        self.main_list_tree.insert('', END, values=row)
                else:
                    messagebox.showinfo('No Matching Results', f'Nothing Matched With Product Id: {self.var_search_by_val.get()}.', parent=self.window)
                    self.show_prod_fun()

            elif self.var_search_by.get()=='Product Name':
                cur.execute('SELECT * FROM inventory WHERE pr_name=%s', (self.var_search_by_val.get().capitalize(),))
                rows_db = cur.fetchall()
                if rows_db!=[]:
                    self.main_list_tree.delete(*self.main_list_tree.get_children())
                    for row in rows_db:
                        self.main_list_tree.insert('', END, values=row)
                else:
                    messagebox.showinfo('No Matching Results', f'Nothing Matched With Product Name: {self.var_search_by_val.get().capitalize()}.', parent=self.window)
                    self.show_prod_fun()

            elif self.var_search_by.get()=='Vendor Name':
                cur.execute('SELECT * FROM inventory WHERE ven_name=%s', (self.var_search_by_val.get().capitalize(),))
                rows_db = cur.fetchall()
                if rows_db!=[]:
                    self.main_list_tree.delete(*self.main_list_tree.get_children())
                    for row in rows_db:
                        self.main_list_tree.insert('', END, values=row)
                else:
                    messagebox.showinfo('No Matching Results', f'Nothing Matched With Vendor Number: {self.var_search_by_val.get().capitalize()}.', parent=self.window)
                    self.show_prod_fun()

            elif self.var_search_by.get()=='Vendor Number':
                cur.execute('SELECT * FROM inventory WHERE ven_num=%s', (self.var_search_by_val.get(),))
                rows_db = cur.fetchall()
                if rows_db!=[]:
                    self.main_list_tree.delete(*self.main_list_tree.get_children())
                    for row in rows_db:
                        self.main_list_tree.insert('', END, values=row)
                else:
                    messagebox.showinfo('No Matching Results', f'Nothing Matched With Vendor Number: {self.var_search_by_val.get()}.', parent=self.window)
                    self.show_prod_fun()

            elif self.var_search_by.get()=='Stocks Availability':
                cur.execute('SELECT * FROM inventory WHERE stocks > %s', (self.var_search_by_val.get(),))
                rows_db = cur.fetchall()
                if rows_db!=[]:
                    self.main_list_tree.delete(*self.main_list_tree.get_children())
                    for row in rows_db:
                        self.main_list_tree.insert('', END, values=row)
                else:
                    messagebox.showinfo('No Matching Results', f'Nothing Matched With Stocks availability of {self.var_search_by_val.get()}.', parent=self.window)
                    self.show_prod_fun()

           
        except Exception as ex:
            messagebox.showerror('Error', f'Error due to {str(ex)}', parent=self.window)
        
    def deselect_tree_item(self, tree_name):
        tree_name.selection_remove(tree_name.selection())

    def go_to_dashboard_func(self):
        self.window.destroy()
