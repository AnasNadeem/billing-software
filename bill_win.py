from tkinter import * 
import tkinter.ttk as ttk
from tkinter import messagebox
import psycopg2
from all_prod_list import AllProdDash
from cus_list import CusDash
from pay_mode import PayDash
from check_inv import CheckInvDash
from all_bill_list import BillCheckDash
from datetime import date, datetime
from constants import *
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from num2words import num2words

class BillDash:
    def __init__(self, window):
        self.window = window
        self.window.geometry("1366x720+0+0")
        self.main_black_color = '#0f0f0f'
        self.main_white_color = '#f8f8f8'
        self.window['bg'] = self.main_black_color
        self.window.title("Billing Software")
        # self.window.iconbitmap("")
        self.window.resizable(False, False)

        # Defining Variable 
        self.var_cus_id = IntVar()
        self.var_cus_name = StringVar()
        self.var_cus_num = StringVar()
        self.var_cus_add = StringVar()

        self.var_invoice_num = StringVar()

        self.var_search_prod_by = StringVar()
        self.var_search_prd_text = StringVar()
        self.var_search_cus_text = StringVar()

        self.var_pr_id = IntVar()
        self.var_pr_name = StringVar()
        self.var_pr_price = StringVar()
        self.var_pr_stocks = IntVar()
        self.var_quantity_prd = IntVar()

        self.var_pur_mode = StringVar()
        # Billing Software Text 
        self.admin_dash_text = Label(window, text='Billing Software',font=("Roboto Regular", 36), fg=self.main_white_color,bg=self.main_black_color)
        self.admin_dash_text.place(x=0,y=0)

        # Check Bill Btn 
        check_bill_btn = Button(self.window, text='Check Bill',
                                cursor='hand2',fg=self.main_black_color, 
                                command=self.go_to_bill_func,                  
                                bg='white', font=('Roboto Regular', 14, "bold"),width=14)
        check_bill_btn.place(x=370, y=10)

        # AddPayment Btn 
        add_payment_btn = Button(self.window, text='Payment Mode',
                                cursor='hand2',fg=self.main_black_color, 
                                command=self.go_to_paymode_func,                  
                                bg='white', font=('Roboto Regular', 14, "bold"),width=14)
        add_payment_btn.place(x=570, y=10)

        # Search Invoices Btn 
        search_inv_btn = Button(self.window, text='Search Invoices',
                                cursor='hand2',fg=self.main_black_color, 
                                command=self.go_to_search_inv,                  
                                bg='white', font=('Roboto Regular', 14, "bold"),width=14)
        search_inv_btn.place(x=770, y=10)

        # Dashboard Btn 
        main_win_btn = Button(self.window, text='Dashboard',
                                cursor='hand2',fg=self.main_black_color, 
                                command=self.go_to_dashboard_func,                  
                                bg='white', font=('Roboto Regular', 14, "bold"),width=14)
        main_win_btn.place(x=970, y=10)

        # Refresh Btn 
        refresh_btn = Button(self.window, text='Refresh',
                                cursor='hand2',fg=self.main_black_color, 
                                command=self.refresh_func,                  
                                bg='white', font=('Roboto Regular', 14, "bold"),width=14)
        refresh_btn.place(x=1170, y=10)

        # Product DETAILS FORM FRAME 
        self.prod_frame = LabelFrame(self.window,bd=2,text='Product Details', relief=FLAT)        
        self.prod_frame.place(x=20, y=60, width=780, height=440)

        self.search_prod_select = ttk.Combobox(self.prod_frame,
                                values=("Select By","Product Name", "IMEI","Stocks Availability"),
                                state='readonly', justify=CENTER,
                                font=('Roboto Regular', 14, "normal"),
                                textvariable=self.var_search_prod_by
                                )
        self.search_prod_select.grid(row=0, column=0,padx=40,pady=10)
        self.search_prod_select.current(0)

        self.search_prod_txt_entry = Entry(self.prod_frame,relief=SUNKEN,
                                    bg="white", fg="#6b6a69",
                                    font=("yu gothic ui semibold", 12),
                                    textvariable=self.var_search_prd_text
                                    )
        self.search_prod_txt_entry.grid(row=0,column=1,padx=0,pady=10)

        self.search_prod_btn = Button(self.prod_frame, text='Search Product',
                                cursor='hand2',fg=self.main_white_color,
                                command=self.show_search_prod_func,                
                                bg=self.main_black_color, font=('Roboto Regular', 14, "normal"))
        self.search_prod_btn.grid(row=0,column=2,padx=10,pady=10)

        self.show_all_prod_btn = Button(self.prod_frame, text='Show All',
                                cursor='hand2',fg=self.main_white_color,
                                command=self.show_all_prod_func,                
                                bg=self.main_black_color, font=('Roboto Regular', 14, "normal"))
        self.show_all_prod_btn.grid(row=0,column=3,padx=0,pady=10)

        #Treeview
        self.frame_for_tree = Frame(self.prod_frame, bd=2, relief=RIDGE)
        self.frame_for_tree.place(x=0, y=60,width=760, height=210)

        self.scrolly = Scrollbar(self.frame_for_tree, orient=VERTICAL)
        self.scrollx = Scrollbar(self.frame_for_tree, orient=HORIZONTAL)

        self.prod_list_tree = ttk.Treeview(self.frame_for_tree,
                columns=("id","pr_name","sell_price","stocks"), show='headings', yscrollcommand=self.scrolly.set,xscrollcommand=self.scrollx.set)

        self.prod_list_tree['selectmode'] = 'browse'

        self.scrolly.pack(side=RIGHT, fill=Y)
        self.scrollx.pack(side=BOTTOM, fill=X)

        self.scrolly.config(command=self.prod_list_tree.yview)
        self.scrollx.config(command=self.prod_list_tree.xview)

        self.prod_list_tree.heading('id', text="IMEI")
        self.prod_list_tree.heading('pr_name', text="Product Name")
        self.prod_list_tree.heading('sell_price', text="Sell Price")
        self.prod_list_tree.heading('stocks', text="Stocks")
        
        self.prod_list_tree.pack(fill=BOTH, expand=1)

        self.prod_list_tree.column('id', width=100)
        self.prod_list_tree.column('pr_name', width=100)
        self.prod_list_tree.column('sell_price', width=100)
        self.prod_list_tree.column('stocks',width=20)

        self.prod_list_tree.bind("<ButtonRelease-1>", self.get_prod_fun)
        self.show_all_prod_func()

        # Product Name Label
        prod_name_label_txt = Label(self.prod_frame, text='Product Name: ',bg="white", fg="#4f4e4d",
                                    font=("yu gothic ui", 14, "bold"))
        
        prod_name_label_txt.place(x=40, y=280)

        # Product Name Dynamic Input
        self.prod_name_dyn = Label(self.prod_frame,textvariable=self.var_pr_name,fg="#4f4e4d",
                                    font=("Roboto Regular", 14, "bold"))
        
        self.prod_name_dyn.place(x=220, y=280)

        # Special ID Label
        imd_label_txt = Label(self.prod_frame, text='IMEI: ',bg="white", fg="#4f4e4d",
                                    font=("yu gothic ui", 14, "bold"))
        
        imd_label_txt.place(x=40, y=330)

        # Special ID Dynamic Input
        self.imd_dyn = Label(self.prod_frame,textvariable=self.var_pr_id, fg="#4f4e4d",
                                    font=("Roboto Regular", 14, "bold"))
        self.imd_dyn.place(x=160, y=330)
        
        # Stocks Label 
        stocks_txt_label = Label(self.prod_frame, text='Stocks: ',bg="white", fg="#4f4e4d",
                                    font=("yu gothic ui", 14, "bold"))
        
        stocks_txt_label.place(x=380, y=330)

        # Stocks Dynamic Input
        self.stocks_txt_entry = Label(self.prod_frame,textvariable=self.var_pr_stocks, fg="#4f4e4d",
                                    font=("Roboto Regular", 14, "bold"))
        self.stocks_txt_entry.place(x=460, y=330)

        # Quantity Label 
        quantity_txt_label = Label(self.prod_frame, text='Quantity: ',bg="white", fg="#4f4e4d",
                                    font=("yu gothic ui", 14, "bold"))
        
        quantity_txt_label.place(x=40, y=380)

        # Quantity Dynamic Input
        self.quantity_txt_entry = Entry(self.prod_frame,relief=SUNKEN,
                                    bg="white", fg="#6b6a69",
                                    font=("yu gothic ui semibold", 14),
                                    textvariable=self.var_quantity_prd
                                    )
        self.quantity_txt_entry.place(x=160, y=380, width=140)

        # Price Label 
        price_txt_label = Label(self.prod_frame, text='Price: ',bg="white", fg="#4f4e4d",
                                    font=("yu gothic ui", 14, "bold"))
        
        price_txt_label.place(x=380, y=380)

        self.price_txt_entry = Label(self.prod_frame,textvariable=self.var_pr_price, fg="#4f4e4d",
                                    font=("Roboto Regular", 14, "bold"))
        self.price_txt_entry.place(x=460, y=380)

        # Add To Cart Button
        self.add_to_cart_btn = Button(self.prod_frame, text='Add To Cart',
                                cursor='hand2',fg=self.main_white_color,
                                command=self.add_to_cart_func,                
                                bg=self.main_black_color, font=('Roboto Regular', 14, "normal"))
        self.add_to_cart_btn.place(x=600, y=276, width=160)

        # Update Cart Btn 
        self.update_to_cart_btn = Button(self.prod_frame, text='Update Cart',
                                cursor='hand2',fg=self.main_white_color,
                                command=self.update_cart_func,                
                                bg=self.main_black_color, font=('Roboto Regular', 14, "normal"))
        self.update_to_cart_btn.place(x=600, y=326, width=160)

        # Delete From Cart Btn 
        self.del_fr_cart_btn = Button(self.prod_frame, text='Delete From Cart',
                                cursor='hand2',fg=self.main_white_color,
                                command=self.delete_cart_func,                
                                bg=self.main_black_color, font=('Roboto Regular', 14, "normal"))
        self.del_fr_cart_btn.place(x=600, y=376, width=160)

        # Customer DETAILS FORM FRAME 
        self.cus_add_frame = LabelFrame(self.window,bd=2,text='Customer Details', relief=FLAT)        
        self.cus_add_frame.place(x=810, y=60, width=540, height=300)

        # Customer Number Label
        cus_num_label_txt = Label(self.cus_add_frame, text='Cus Number: ',bg="white", fg="#4f4e4d",
                                    font=("yu gothic ui", 14, "bold"))
        
        cus_num_label_txt.grid(row=0,column=0,padx=10,pady=10)

        self.search_cus_num_entry = Entry(self.cus_add_frame,relief=SUNKEN,
                                    bg="white", fg="#6b6a69",
                                    font=("yu gothic ui semibold", 14),
                                    textvariable=self.var_search_cus_text
                                    )
        self.search_cus_num_entry.grid(row=0,column=1,padx=0,pady=10)

        self.search_cus_num_btn = Button(self.cus_add_frame, text='Search Customer',
                                cursor='hand2',fg=self.main_white_color,
                                command=self.show_search_cus_func,                
                                bg=self.main_black_color, font=('Roboto Regular', 14, "normal"))
        self.search_cus_num_btn.grid(row=0,column=2,padx=5,pady=10)

        # Customer ID Label
        cus_id_label_txt = Label(self.cus_add_frame, text='Customer Id: ',bg="white", fg="#4f4e4d",
                                    font=("yu gothic ui", 14, "bold"))
        
        cus_id_label_txt.place(x=10,y=60)

        # Customer ID Dynamic Label
        cus_id_dyn_label_txt = Label(self.cus_add_frame, 
                                    textvariable=self.var_cus_id,
                                    fg="#4f4e4d",
                                    font=("yu gothic ui", 14, "bold"))
        
        cus_id_dyn_label_txt.place(x=160,y=60)
        # Customer Name Label
        cus_name_label_txt = Label(self.cus_add_frame, text='Customer Name: ',bg="white", fg="#4f4e4d",
                                    font=("yu gothic ui", 14, "bold"))
        
        cus_name_label_txt.place(x=10,y=100)

        # Customer Name Dynamic Label
        cus_name_dyn_label_txt = Label(self.cus_add_frame, 
                                    textvariable=self.var_cus_name,
                                    fg="#4f4e4d",
                                    font=("yu gothic ui", 14, "bold"))
        
        cus_name_dyn_label_txt.place(x=200,y=100)

        # Customer Number Label
        cus_number_label_txt = Label(self.cus_add_frame, text='Customer Number: ',bg="white", fg="#4f4e4d",
                                    font=("yu gothic ui", 14, "bold"))
        
        cus_number_label_txt.place(x=10,y=140)

        # Customer Number Dynamic Label
        cus_num_dyn_label_txt = Label(self.cus_add_frame, 
                                    textvariable=self.var_cus_num,
                                    fg="#4f4e4d",
                                    font=("yu gothic ui", 14, "bold"))
        
        cus_num_dyn_label_txt.place(x=200,y=140)

        # Customer Address Label
        cus_add_label_txt = Label(self.cus_add_frame, text='Customer Address: ',bg="white", fg="#4f4e4d",
                                    font=("yu gothic ui", 14, "bold"))
        
        cus_add_label_txt.place(x=10,y=180)

        # Customer Address Dynamic Label
        cus_add_dyn_label_txt = Label(self.cus_add_frame, 
                                    textvariable=self.var_cus_add,
                                    fg="#4f4e4d",
                                    font=("yu gothic ui", 14, "bold"))
        
        cus_add_dyn_label_txt.place(x=200,y=180)

        clear_cus_det_button = Button(self.cus_add_frame, text='Clear',
                                cursor='hand2',fg=self.main_white_color,
                                command=self.clear_cus_func,                
                                bg=self.main_black_color, font=('Roboto Regular', 14, "normal"),width=10)
        clear_cus_det_button.place(x=140,y=230)

        add_cus_button = Button(self.cus_add_frame, text='Add Customer',
                                cursor='hand2',fg=self.main_white_color,
                                command=self.go_to_cus_func,                
                                bg=self.main_black_color, font=('Roboto Regular', 14, "normal"),width=10)
        add_cus_button.place(x=280,y=230, width=140)


        # Buttons Lots of Buttons Frame
        self.buttons_lots_buttons = Frame(self.window, bd=0, relief=RIDGE)
        self.buttons_lots_buttons.place(x=810,y=380, width=540, height=120)
        
        self.total_button_button = Button(self.buttons_lots_buttons, text='Total Price',
                                cursor='hand2',fg=self.main_white_color,
                                command=self.total_price_func,                
                                bg=self.main_black_color, font=('Roboto Regular', 14, "normal"),width=8)
        self.total_button_button.place(x=20,y=10, width=120)

        self.total_button_button = Button(self.buttons_lots_buttons, text='Generate Bill',
                                cursor='hand2',fg=self.main_white_color,
                                command=self.generate_bill_func,                
                                bg=self.main_black_color, font=('Roboto Regular', 14, "normal"),width=12)
        self.total_button_button.place(x=180,y=10, width=160)

        self.total_button_button = Button(self.buttons_lots_buttons, text='Print',
                                cursor='hand2',fg=self.main_white_color,
                                command=self.print_bill_func,                
                                bg=self.main_black_color, font=('Roboto Regular', 14, "normal"),width=8)
        self.total_button_button.place(x=380,y=10, width=120)

        self.pur_mode_select = ttk.Combobox(self.buttons_lots_buttons,
                                state='readonly', justify=CENTER,
                                font=('Roboto Regular', 14, "normal"),
                                textvariable=self.var_pur_mode
                                )
        self.add_pur_mode_combobox()
        self.pur_mode_select.current(0)
        self.pur_mode_select.place(x=20,y=70, width=200)
        self.total_button_button = Button(self.buttons_lots_buttons, text='Clear All',
                                cursor='hand2',fg=self.main_white_color,
                                command=self.clear_all_func,                
                                bg=self.main_black_color, font=('Roboto Regular', 14, "normal"),width=8)
        self.total_button_button.place(x=260,y=60, width=120)

        # CART Frame
        self.cart_frame = Frame(self.window, bd=2, relief=FLAT)
        self.cart_frame.place(x=20, y=520, width=1330, height=180)

        self.scrolly_cart = Scrollbar(self.cart_frame, orient=VERTICAL)
        self.scrollx_cart = Scrollbar(self.cart_frame, orient=HORIZONTAL)

        self.add_to_cart_tree = ttk.Treeview(self.cart_frame,
                columns=("imei","pr_name","price","quantity","total","cus_name","cus_num"), show='headings', yscrollcommand=self.scrolly_cart.set,xscrollcommand=self.scrollx_cart.set)

        self.add_to_cart_tree['selectmode'] = 'browse'

        self.scrolly_cart.pack(side=RIGHT, fill=Y)
        self.scrollx_cart.pack(side=BOTTOM, fill=X)

        self.scrolly_cart.config(command=self.add_to_cart_tree.yview)
        self.scrollx_cart.config(command=self.add_to_cart_tree.xview)

        self.add_to_cart_tree.heading('imei', text="IMEI")
        self.add_to_cart_tree.heading('pr_name', text="Product Name")
        self.add_to_cart_tree.heading('price', text="Price")
        self.add_to_cart_tree.heading('quantity', text="Quantity")
        self.add_to_cart_tree.heading('total', text="Total Amount")
        self.add_to_cart_tree.heading('cus_name', text="Customer Name")
        self.add_to_cart_tree.heading('cus_num', text="Customer Number")
        
        self.add_to_cart_tree.pack(fill=BOTH, expand=1)

        self.add_to_cart_tree.column('imei', width=100)
        self.add_to_cart_tree.column('pr_name', width=100)
        self.add_to_cart_tree.column('price', width=100)
        self.add_to_cart_tree.column('quantity',width=20)
        self.add_to_cart_tree.column('total',width=100)
        self.add_to_cart_tree.column('cus_name',width=100)
        self.add_to_cart_tree.column('cus_num',width=100)

        self.add_to_cart_tree.bind("<ButtonRelease-1>", self.get_cart_func)

    def go_to_cus_func(self):
        self.newWindow = Toplevel(self.window)
        self.app = CusDash(self.newWindow)
        
    def go_to_search_inv(self):
        self.newWindow = Toplevel(self.window)
        self.app = CheckInvDash(self.newWindow)

    def go_to_paymode_func(self):
        self.newWindow = Toplevel(self.window)
        self.app = PayDash(self.newWindow)

    def go_to_bill_func(self):
        self.newWindow = Toplevel(self.window)
        self.app = BillCheckDash(self.newWindow)

    def refresh_func(self):
        self.show_all_prod_func()
        self.add_pur_mode_combobox()

    def go_to_dashboard_func(self):
        self.window.destroy()

    def get_prod_fun(self, ev):
        f = self.prod_list_tree.focus()
        content = (self.prod_list_tree.item(f))
        row = content['values']
        self.var_pr_id.set(row[0])
        self.var_pr_name.set(row[1])
        self.var_pr_price.set(row[2])
        self.var_pr_stocks.set(row[3])
        self.var_quantity_prd.set(1)
        self.quantity_txt_entry.focus()
        self.deselect_tree_item(self.add_to_cart_tree)

    def show_all_prod_func(self):
        con = psycopg2.connect(host=DB_HOST,database=DB_NAME, user=DB_USER, password=DB_PASS)
        cur = con.cursor()
        try:
            cur.execute('SELECT * FROM inventory WHERE stocks>0')
            rows_db = cur.fetchall()
            self.prod_list_tree.delete(*self.prod_list_tree.get_children())
            for row in rows_db: 
                self.prod_list_tree.insert('', END, values=(row[0], row[1],row[4] ,row[2]))
            
        except Exception as ex:
            messagebox.showerror('Error', f'Error due to {str(ex)}', parent=self.window)

    def show_search_prod_func(self):
        con = psycopg2.connect(host=DB_HOST,database=DB_NAME, user=DB_USER, password=DB_PASS)
        cur = con.cursor()
        try:
            if self.var_search_prod_by.get()=='Select By':
                messagebox.showwarning('Please Select', "Select an option", parent=self.window)
            elif self.var_search_prod_by.get()=='Product Name':
                cur.execute('SELECT * FROM inventory WHERE pr_name=%s', (self.var_search_prd_text.get(),))
                rows_db = cur.fetchall()
                if rows_db!=[]:
                    self.prod_list_tree.delete(*self.prod_list_tree.get_children())
                    for row in rows_db:
                        self.prod_list_tree.insert('', END, values=(row[0], row[1],row[4] ,row[2]))
                else:
                    messagebox.showinfo('No Matching Results', f'Nothing Matched With Product Name: {self.var_search_prd_text.get()}.', parent=self.window)
                    self.show_all_prod_func()
            elif self.var_search_prod_by.get()=='IMEI':
                cur.execute('SELECT * FROM inventory WHERE id=%s', (self.var_search_prd_text.get(),))
                rows_db = cur.fetchall()
                if rows_db!=[]:
                    self.prod_list_tree.delete(*self.prod_list_tree.get_children())
                    for row in rows_db:
                        self.prod_list_tree.insert('', END, values=(row[0], row[1],row[4] ,row[2]))
                else:
                    messagebox.showinfo('No Matching Results', f'Nothing Matched With Product Name: {self.var_search_prd_text.get()}.', parent=self.window)
                    self.show_all_prod_func()
            elif self.var_search_prod_by.get()=='Stocks Availability':
                cur.execute('SELECT * FROM inventory WHERE stocks > %s', (self.var_search_prd_text.get(),))
                rows_db = cur.fetchall()
                if rows_db!=[]:
                    self.prod_list_tree.delete(*self.prod_list_tree.get_children())
                    for row in rows_db:
                        self.prod_list_tree.insert('', END, values=(row[0], row[1],row[4] ,row[2]))
                else:
                    messagebox.showinfo('No Matching Results', f'Nothing Matched With Stocks availability of {self.var_search_prd_text.get()}.', parent=self.window)
                    self.show_all_prod_func()
        except Exception as ex:
            messagebox.showerror('Error', f'Error due to {str(ex)}', parent=self.window)
        
    def clear_prod_fun(self):
        self.var_search_prod_by.set('Search By')
        self.var_search_prd_text.set('')
        self.var_pr_id.set(0)
        self.var_pr_name.set('')
        self.var_pr_price.set('')
        self.var_pr_price.set(0.0)
        self.var_quantity_prd.set(0)
        self.var_pr_stocks.set(0)

    def show_search_cus_func(self):
        con = psycopg2.connect(host=DB_HOST,database=DB_NAME, user=DB_USER, password=DB_PASS)
        cur = con.cursor()
        try:
            if self.var_search_cus_text.get()=="":
                messagebox.showerror('Error', f'Please enter Mobile number', parent=self.window)
            else:
                cur.execute('SELECT * FROM customer WHERE num= %s', (self.var_search_cus_text.get(),))
                rows_db = cur.fetchall()
                if rows_db!=[]:
                    for data in rows_db:
                        self.var_cus_id.set(data[0])
                        self.var_cus_name.set(data[1])
                        self.var_cus_num.set(data[2])
                        self.var_cus_add.set(data[3])
                else:
                    messagebox.showerror('Nothing Found', f'No Customers Found. Check the number', parent=self.window)
        except Exception as ex:
            messagebox.showerror('Error', f'Error due to {str(ex)}', parent=self.window)

    def clear_cus_func(self):
        self.var_cus_id.set(0)
        self.var_cus_name.set('')
        self.var_cus_num.set('')
        self.var_cus_add.set('')
        self.var_search_cus_text.set('')

    def get_cart_func(self, ev):
        f = self.add_to_cart_tree.focus()
        content = (self.add_to_cart_tree.item(f))
        row = content['values']
        con = psycopg2.connect(host=DB_HOST,database=DB_NAME, user=DB_USER, password=DB_PASS)
        cur = con.cursor()
        try:
            cur.execute("""SELECT * FROM inventory WHERE id=%s""",(content['values'][0],))
            fetch_row = cur.fetchone()
            self.var_pr_stocks.set(fetch_row[2])
            self.var_pr_id.set(row[0])
            self.var_pr_name.set(row[1])
            self.var_pr_price.set(row[2])
            self.var_quantity_prd.set(row[3])
            self.quantity_txt_entry.focus_set()
            self.deselect_tree_item(self.prod_list_tree)
        except Exception as ex:
                messagebox.showerror('Error', f'Error due to {str(ex)}', parent=self.window)

    def add_to_cart_func(self):
        if self.var_pr_name.get()=='' or self.var_cus_name.get()=='':
            messagebox.showerror('Empty Input','Please Select Customer', parent=self.window)
        elif self.var_quantity_prd.get()==0 or self.var_quantity_prd.get()=='':
            messagebox.showerror('Empty Input','Please Select Quantity', parent=self.window)
        else:
            con = psycopg2.connect(host=DB_HOST,database=DB_NAME, user=DB_USER, password=DB_PASS)
            cur = con.cursor()
            try:
                # Inserting into Cart 
                if self.var_pr_stocks.get()>=self.var_quantity_prd.get():
                    total_amount_pr = (float(self.var_pr_price.get()) * float(self.var_quantity_prd.get()))
                    self.add_to_cart_tree.insert('', END, values=(
                    self.var_pr_id.get(),
                    self.var_pr_name.get(),
                    self.var_pr_price.get(),
                    self.var_quantity_prd.get(),
                    total_amount_pr,
                    self.var_cus_name.get(),
                    self.var_cus_num.get()
                    ))
                    self.deselect_tree_item(self.prod_list_tree)
                    self.deselect_tree_item(self.add_to_cart_tree)
                    # Inserting into Bill
                    current_date = datetime.now().strftime('%x')
                    cur.execute("""
                    INSERT into bill (cus_id,pr_id,paid,date,quantity)
                    VALUES (%s,%s,%s,%s,%s)
                    """,(
                        self.var_cus_id.get(),
                        self.var_pr_id.get(),
                        'no',
                        current_date,
                        self.var_quantity_prd.get()
                        )
                    )
                    con.commit() 
                    # Updating the inventory 
                    cur.execute("""
                    UPDATE inventory SET stocks=%s 
                    WHERE pr_name = %s AND sell_price=%s
                    """,(
                        self.var_pr_stocks.get() - self.var_quantity_prd.get(),
                        self.var_pr_name.get(),
                        self.var_pr_price.get()
                    ))
                    con.commit() 
                    self.clear_prod_fun()
                    self.show_all_prod_func()
                else:
                    messagebox.showerror('Too much Quantity','Not much quantity left in stocks.', parent=self.window)
            except Exception as ex:
                messagebox.showerror('Error', f'Error due to {str(ex)}', parent=self.window)

    def delete_cart_func(self):
        focused_item_in_cart = self.add_to_cart_tree.focus()
        if focused_item_in_cart:
            content = (self.add_to_cart_tree.item(focused_item_in_cart))
            con = psycopg2.connect(host=DB_HOST,database=DB_NAME, user=DB_USER, password=DB_PASS)
            cur = con.cursor()
            try:
                # Select the particular inventory product 
                cur.execute("""SELECT * FROM inventory WHERE id=%s""",(content['values'][0],))
                fetch_row = cur.fetchone()
                #Update the inventory
                cur.execute("""
                    UPDATE inventory SET stocks=%s 
                    WHERE pr_name = %s AND sell_price=%s
                    """,(
                        fetch_row[2] + content['values'][3],
                        content['values'][1],
                        content['values'][2]
                    ))
                con.commit() 
                #Delete the bill
                cur.execute("""
                DELETE FROM bill WHERE (cus_id=%s AND pr_id=%s) AND paid=%s
                """,(
                    self.var_cus_id.get(),
                    content['values'][0],
                    'no'
                ))
                con.commit()
                self.show_all_prod_func()
            except Exception as ex:
                messagebox.showerror('Error', f'Error due to {str(ex)}', parent=self.window)
            self.add_to_cart_tree.delete(focused_item_in_cart)
            self.deselect_tree_item(self.prod_list_tree)
            self.deselect_tree_item(self.add_to_cart_tree)
        else:
            messagebox.showerror('Select from Cart','Please select something from the cart.', parent=self.window)
        self.clear_prod_fun()

    def update_cart_func(self):
        focused_item_in_cart = self.add_to_cart_tree.focus()
        if focused_item_in_cart:
            content = (self.add_to_cart_tree.item(focused_item_in_cart))
            if self.var_quantity_prd.get()==0 or self.var_quantity_prd.get()=='':
                messagebox.showerror('Empty Input','Please Select Quantity', parent=self.window)
            elif self.var_pr_stocks.get()<self.var_quantity_prd.get():
                messagebox.showerror('Too much Quantity','Not much quantity left in stocks.', parent=self.window)
            else:
                con = psycopg2.connect(host=DB_HOST,database=DB_NAME, user=DB_USER, password=DB_PASS)
                cur = con.cursor()
                try:
                    #Update the inventory
                    cur.execute("""
                        UPDATE inventory SET stocks=%s 
                        WHERE pr_name = %s AND sell_price=%s
                        """,(
                            (self.var_pr_stocks.get() + content['values'][3]) - self.var_quantity_prd.get(),
                            self.var_pr_name.get(),
                            self.var_pr_price.get()
                        ))
                    con.commit()
                    # Get the bill 
                    cur.execute("""
                        SELECT * FROM bill
                        WHERE (cus_id=%s AND pr_id=%s) AND paid=%s 
                    """,(
                        self.var_cus_id.get(),
                        content['values'][0],
                        'no'
                    ))
                    fetch_row = cur.fetchone()
                    #Update the bill
                    cur.execute("""
                        UPDATE bill SET 
                        quantity=%s
                        WHERE id=%s
                        """,(
                            self.var_quantity_prd.get(),
                            fetch_row[0]
                        ))
                    con.commit()
                    # Update the cart items
                    total_amount_pr = (float(self.var_pr_price.get()) * float(self.var_quantity_prd.get()))
                    self.add_to_cart_tree.insert('', END, values=(
                    self.var_pr_id.get(),
                    self.var_pr_name.get(),
                    self.var_pr_price.get(),
                    self.var_quantity_prd.get(),
                    total_amount_pr,
                    self.var_cus_name.get(),
                    self.var_cus_num.get()
                    ))
                    self.deselect_tree_item(self.prod_list_tree)
                    self.deselect_tree_item(self.add_to_cart_tree)
                    self.show_all_prod_func()
                    self.clear_prod_fun()
                    self.add_to_cart_tree.delete(focused_item_in_cart)
                except Exception as ex:
                    messagebox.showerror('Error', f'Error due to {str(ex)}', parent=self.window)
        else:
            messagebox.showerror('Select from Cart','Please select something from the cart.', parent=self.window)
             
    def total_price_func(self):
        all_cart_items = self.add_to_cart_tree.get_children()
        if len(all_cart_items)==0:
            messagebox.showerror('Error', 'Add some product to the cart.',parent=self.window)
        else:
            total_price_pr = 0
            for rows in all_cart_items:
                total_price_pr = total_price_pr + float(self.add_to_cart_tree.item(rows)['values'][4])
            messagebox.showinfo('Total Price', f'Total Price: {total_price_pr}',parent=self.window)
        
    def add_pur_mode_combobox(self):
        con = psycopg2.connect(host=DB_HOST,database=DB_NAME, user=DB_USER, password=DB_PASS)
        cur = con.cursor()
        try:
            cur.execute("""SELECT * FROM paymode""")
            fetch_row = cur.fetchall()
            # Declaring the list and appending paymode name in it 
            pur_mode_data = ['Purchase Mode']
            for row in fetch_row:
                pur_mode_data.append(f'{row[0]}-{row[1]}')
            # Changing the list back to tuple and appending it to values
            pur_mode_tup = tuple(pur_mode_data)
            self.pur_mode_select['values'] = pur_mode_tup
        except Exception as ex:
            messagebox.showerror('Error', f'Error due to {str(ex)}', parent=self.window)

    def generate_bill_func(self):
        if self.var_pur_mode.get() == 'Purchase Mode':
            messagebox.showerror('Select Purchase Mode', f'Please select the purchase mode', parent=self.window)
        else:
            current_date = datetime.now().strftime('%x')
            con = psycopg2.connect(host=DB_HOST,database=DB_NAME, user=DB_USER, password=DB_PASS)
            cur = con.cursor()
            try:
                # Fetch all the bill with the cus_id and paid='no' with today's date 
                cur.execute("""
                    SELECT * FROM bill WHERE (cus_id=%s AND paid=%s) AND date=%s
                """,(
                    self.var_cus_id.get(),
                    'no',
                    current_date
                ))
                get_all_fetched_data = cur.fetchall()
                # Updating the bill to paid='yes' and pur_mode='paymode selected'
                all_bill_id = []
                pur_mode_id = self.var_pur_mode.get().split('-')[0]
                for bill_data in get_all_fetched_data:
                    cur.execute("""
                        UPDATE bill SET 
                        paid=%s,
                        pur_mode=%s 
                        WHERE (cus_id = %s AND date=%s) AND pr_id=%s
                        """,(
                            'yes',
                            pur_mode_id,
                            bill_data[1],
                            current_date,
                            bill_data[2]
                    ))
                    con.commit()
                    all_bill_id.append(bill_data[0])
                # Creating the billfile and inserting all the bill
                all_prd_list = []
                s_no = 1
                total_price = 0
                for bill_id in all_bill_id:
                    cur.execute("""SELECT * FROM bill WHERE id=%s""",(bill_id,))
                    bill_list = cur.fetchone()
                    cur.execute('SELECT * FROM inventory WHERE id=%s',(bill_list[2],))
                    prod = cur.fetchone()
                    cgst_with_amount = f"{prod[5]}%: {(prod[4]*prod[5])/100}"
                    sgst_with_amount = f"{prod[5]}%: {(prod[4]*prod[6])/100}"
                    prd_list = [s_no, prod[1],prod[0],f"{prod[4]}",bill_list[5],cgst_with_amount,sgst_with_amount]
                    total_price+=prod[4]*bill_list[5]
                    all_prd_list.append(prd_list)
                    s_no+=1 
                
                total_price_int = int(total_price)
                price_in_words = num2words(total_price_int)
                current_date_without_bs = current_date.replace('/', '-')
                file_name = f'bill_invoice/{self.var_cus_name.get()}_{total_price_int}_{current_date_without_bs}'
                # Create and Insert into billdetails datails
                cur.execute("""
                INSERT into billdetails
                (cus_id, date, total_amount, bill_file_name)
                VALUES (%s, %s, %s, %s)
                """,(
                    self.var_cus_id.get(),
                    current_date,
                    total_price,
                    file_name
                    )
                )
                con.commit()
                cur.execute("""
                SELECT * FROM billdetails
                WHERE (cus_id=%s AND total_amount=%s) AND date=%s
                """,(
                    self.var_cus_id.get(),
                    total_price,
                    current_date
                ))
                bill_row_details = cur.fetchone()
                invoice_id = bill_row_details[0]
                for bill_id in all_bill_id:
                    cur.execute("UPDATE bill SET inv_id=%s WHERE id=%s",(invoice_id, bill_id))
                    con.commit()
                # Creating PDF File 
                full_datetime = datetime.now()
                today_date = full_datetime.strftime('%d')
                this_month = full_datetime.strftime('%m')
                this_year = full_datetime.strftime('%Y')
                date_to_pass_in_pdf = f'{today_date}-{this_month}-{this_year}'

                self.create_inv(
                    file_name,
                    self.var_cus_name.get().capitalize(),
                    self.var_cus_num.get(), 
                    self.var_cus_add.get().capitalize(),
                    invoice_id,
                    date_to_pass_in_pdf,
                    all_prd_list,
                    total_price,
                    price_in_words.capitalize()
                )
                messagebox.showinfo('Congratulations', f'Bill has been generated for {self.var_cus_name.get()}', parent=self.window)
                self.clear_all_func()
            except Exception as ex:
                messagebox.showerror('Error', f'Error due to {str(ex)}', parent=self.window)
    
    # Creating PDF CODE 
    def create_inv(self,file_name, cus_name, cus_num, cus_add,invoice_id,crnt_date, prd_list,total_price,price_in_words):
        # Checking if the folder exists
        import os
        crnt_path = os.getcwd()
        bill_fol = 'bill_invoice'
        full_path = os.path.join(crnt_path, bill_fol)
        check_if_exists = os.path.exists(full_path)
        if check_if_exists==False:
            os.mkdir(bill_fol)

        # Main Pdf Code started
        my_canvas = canvas.Canvas(f'{file_name}.pdf',pagesize=A4)
        styles = getSampleStyleSheet()
        
        # Invoice Title 
        invoice_title = '<font size=14><b>Invoice Details</b></font>'
        invoice_title_style = styles["Normal"]
        inv_title_para = Paragraph(invoice_title, style=invoice_title_style)
        inv_title_para.wrapOn(my_canvas, 200, 40)
        inv_title_para.drawOn(my_canvas, 250,820)

        # Company Desc 
        company_desc = """
            <font size=16><b>MOBILE ADDA</b></font><br/>
            <font size=14 textColor = Color(0,0,0,0.8)>
                Ground G-02, Near BMP-16<br/>
                Khagaul Road Phulwari Sharif<br/>
                Patna, Bihar - 801505 <br/>
                +91 8709203550 <br/>
                +91 9504819561
            </font>
        """
        company_desc_style = styles["Normal"]
        company_desc_style.leading=16
        company_desc_para = Paragraph(company_desc,style=company_desc_style)
        company_desc_para.wrapOn(my_canvas, 350, 140)
        company_desc_para.drawOn(my_canvas, 40,710)

        # Invoice Num
        inv_no_text = f'<font size=14>Invoice No: <b>{invoice_id}</b></font>'
        inv_no_style = styles["Normal"]
        inv_no_para = Paragraph(inv_no_text,style=inv_no_style)
        inv_no_para.wrapOn(my_canvas, 140,20)
        inv_no_para.drawOn(my_canvas, 430,790)
        
        # Date 
        crnt_date_text = f'<font size=14>Date: <b>{crnt_date}</b></font>'
        crnt_date_style = styles["Normal"]
        crnt_date_para = Paragraph(crnt_date_text,style=crnt_date_style)
        crnt_date_para.wrapOn(my_canvas, 140,20)
        crnt_date_para.drawOn(my_canvas, 430,770)

        # GSTIN 
        gst_num = '10BPBPA0505D1Z9'
        comp_gst_num = f"""
        <font size=14 textColor = Color(0,0,0,0.8)><b>GSTIN:</b> {gst_num}</font>"""
        comp_gst_num_style = styles["Normal"]
        comp_gst_para = Paragraph(comp_gst_num,style=comp_gst_num_style)
        comp_gst_para.wrapOn(my_canvas, 400,50)
        comp_gst_para.drawOn(my_canvas, 40,680)

        # Customer Desc  
        customer_desc = f"""
            <font size=16><b>Bill To:</b></font><br/>
            <font size=14 textColor = Color(0,0,0,0.8)>Customer Name: <b>{cus_name}</b></font><br/>
            <font size=14 textColor = Color(0,0,0,0.8)>Customer Number: <b>{cus_num}</b></font><br/>
            <font size=14 textColor = Color(0,0,0,0.8)>Customer Address: <b>{cus_add}</b></font><br/>
        """
        customer_desc_style = styles["Normal"]
        customer_desc_style.leading=16
        customer_para = Paragraph(customer_desc,style=customer_desc_style)
        customer_para.wrapOn(my_canvas, 500, 240)
        customer_para.drawOn(my_canvas, 40,610)

        # Product Description 
        colWidths = [40, 120, 100, 100, 50, 70, 70]
        b_data = [
                    self.create_bold_text('S.No'),
                    self.create_bold_text('Product Name'),
                    self.create_bold_text('IMEI'),
                    self.create_bold_text('Rate'),
                    self.create_bold_text('Qty'),
                    self.create_bold_text('CGST'),
                    self.create_bold_text('SGST'),
                ]
        data = []
        data.append(b_data)
        for prd in prd_list:
            data.append(prd)
            
        tblstyle = TableStyle([('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                                ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                                ])

        table = Table(data, colWidths=colWidths)
        table.setStyle(tblstyle)
        table.wrapOn(my_canvas, 620, 400)
        table.drawOn(my_canvas, 20, 400)

        # Total Price     
        my_canvas.line(20,300,570,300)
        total_price_text = f'<font size=16>Total Price: {price_in_words}- <b>{total_price}</b></font>'
        total_price_style = styles["Normal"]
        total_price_para = Paragraph(total_price_text,style=total_price_style)
        total_price_para.wrapOn(my_canvas, 560,30)
        total_price_para.drawOn(my_canvas, 60,280)
        my_canvas.line(20,270,570,270)

        # Signature
        signature_text = f'<font size=12>Authorised Signature:</font>'
        signature_style = styles["Normal"]
        signature_para = Paragraph(signature_text,style=signature_style)
        signature_para.wrapOn(my_canvas,140,20)
        signature_para.drawOn(my_canvas, 400,190)
        my_canvas.rect(400,150,160,40,stroke=1,fill=0)

        # Note
        note = """
            <font size=14 textColor = Color(0,0,0,0.8)><b>NOTE:</b></font><br/>
            <font size=12 textColor = Color(0,0,0,0.6)>Goods once sold will not be taken back.</font><br/>
            <font size=12 textColor = Color(0,0,0,0.6)>All dispute subject to Patna Jurisdiction only.</font><br/>
            <font size=12 textColor = Color(0,0,0,0.6)>After sales, services will be provided only by related Authorised Service Center .</font>
        """
        note_desc_style = styles["Normal"]
        note_desc_style.leading=16
        note_desc_para = Paragraph(note,style=note_desc_style)
        note_desc_para.wrapOn(my_canvas, 500, 200)
        note_desc_para.drawOn(my_canvas, 40,25)

        my_canvas.showPage()
        my_canvas.save()

    def create_bold_text(self, text, size=12):
        return Paragraph(f"""
        <font size={size}>
        <b>{text}</b>
        </font>
        """)

    def clear_all_func(self):
        self.clear_cus_func()
        self.clear_prod_fun()
        self.deselect_tree_item(self.prod_list_tree)
        self.add_to_cart_tree.delete(*self.add_to_cart_tree.get_children())
        self.var_pur_mode.set('Purchase Mode')

    def print_bill_func(self):
        con = psycopg2.connect(host=DB_HOST,database=DB_NAME, user=DB_USER, password=DB_PASS)
        cur = con.cursor()
        try:
            cur.execute('SELECT * FROM billdetails ORDER BY id DESC LIMIT 1;')
            latest_bill = cur.fetchone()
            import os
            import webbrowser
            cwd = f'{os.getcwd()}'
            pdf = f'{latest_bill[4]}.pdf'
            full_path = os.path.join(cwd, pdf)
            webbrowser.open_new(f'file://{full_path}')
        except Exception as ex:
            messagebox.showerror('Error', f'Error due to {str(ex)}', parent=self.window)

    def deselect_tree_item(self, tree_name):
        tree_name.selection_remove(tree_name.selection())
